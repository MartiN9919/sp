import os

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver

from core.projectSettings.constant import MANUAL_ROOT
from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_LIST_TOP, DAT_SYS_KEY, DAT_SYS_LIST_DOP, \
    DAT_SYS_PHONE_NUMBER_FORMAT


class ModelObject(models.Model):
    """
    Модель таблицы sys_obj содержащая объекты.
    Используется для заполнения классификатора.
    """

    title = models.CharField(
        max_length=25,
        verbose_name='Имя объекта',
    )
    title_single = models.CharField(
        max_length=25,
        verbose_name='Имя объекта ед.ч.',
    )
    name = models.CharField(
        max_length=25,
        verbose_name='Имя латиницей',
    )
    descript = models.TextField(
        max_length=1024,
        verbose_name='Дополнительные пометки',
        help_text='Дополнительная информация о объекте',
        blank=True,
        null=True,
    )
    priority = models.IntegerField(
        verbose_name='Приоритет',
        help_text=' Приоритет при именовании',
    )

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
        db_table = DAT_SYS_OBJ.TABLE_SHORT


class ModelList(models.Model):
    """
    Модель таблицы sys_list_top содержащая названия дополнительных списков.
    Используется, для добавления списков и значений в них.
    """

    name = models.CharField(
        max_length=25,
        verbose_name='Имя латиницей',
    )
    title = models.CharField(
        max_length=50,
        verbose_name='Имя списка',
    )

    def __str__(self):
        return self.title

    def clean(self):
        """
        Функция дял установи режима проверки списка
        """
        self.fl = 0  # костыль, потом изменить
        try:
            self.save()
        except Exception as e:
            raise e

    def save(self, *args, **kwargs):
        """
        Функция сохранения списка с проверкой на дублирование названия
        @param args: стандартный параметр
        @param kwargs: стандартный параметр
        """
        if len(ModelList.objects.filter(title=self.title)) != 0 and self.fl == 0 and not self.id:
            raise ValidationError('список с таким именем уже существует')
        else:
            self.fl = 1
            super().save(*args, **kwargs)

    class Meta:
        managed = False
        verbose_name = "Список"
        verbose_name_plural = "Списки"
        db_table = DAT_SYS_LIST_TOP.TABLE_SHORT


class ModelListDop(models.Model):
    """
    Модель таблицы sys_list_dop хранящая все значения списков.
    Используется, для связи с таблицей sys_list_top через поле list,
    которое связывает запись с определенным списком.
    """
    val = models.CharField(
        max_length=255,
        verbose_name="Значение",
    )
    key = models.ForeignKey(
        ModelList,
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        'ModelListDop',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.val

    def clean(self):
        """
        Функция для валидации списка
        """
        if not self.key_id:
            ModelList.save(self.key)
        self.fl = 0  # костыль, потом изменить
        if not self.id:
            try:
                self.save()
            except Exception as e:
                raise e

    def save(self, *args, **kwargs):
        """
        Функция для сохранения подсписка с проверкой на дублирование
        @param args: стандартный параметр
        @param kwargs: стандартный параметр
        """
        if len(ModelListDop.objects.filter(key=self.key).filter(val=self.val).filter(parent=self.parent)) > 0 and self.fl == 0:
            raise ValidationError('в данном списке уже есть такой элемент')
        else:
            self.fl = 1
            super().save(*args, **kwargs)
        DAT_SYS_LIST_DOP.DUMP.update()

    class Meta:
        managed = False
        verbose_name = "Поле списка"
        verbose_name_plural = "Поля списков"
        db_table = DAT_SYS_LIST_DOP.TABLE_SHORT


class ModelPhoneNumberFormat(models.Model):
    """
    Класс для модели формата телефонного номера
    """
    country = models.CharField(
        max_length=50,
        verbose_name='Страна принадлежности',
        help_text='К какой стране относится этот номер',
    )
    country_code = models.IntegerField(
        verbose_name='Код страны',
        help_text='Набор цифр составляющих код страны',
    )
    length = models.IntegerField(
        verbose_name='Длинна номера',
        help_text='С учетом кода страны',
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        DAT_SYS_PHONE_NUMBER_FORMAT.DUMP.update()

    class Meta:
        managed = False
        db_table = DAT_SYS_PHONE_NUMBER_FORMAT.TABLE_SHORT
        verbose_name = "Формат телефонный номеров"
        verbose_name_plural = "Формат телефонный номеров"


class ModelKey(models.Model):
    """
    Модель таблицы sys_key для хранения классификаторов.
    """
    obj = models.ForeignKey(
        ModelObject,
        verbose_name='Объект',
        related_name='ind_obj',
        on_delete=models.CASCADE,
        help_text='К какому объекту относится данный классификатор',
        # default=1,
    )
    col = models.BooleanField(
        default=False,
        verbose_name='Специфический параметр',
        help_text='Являются ли данные в классификаторе специфичными',
    )
    need = models.BooleanField(
        default=False,
        verbose_name='Основное поле',
        help_text='Является ли данный классификатор обязательным для объекта',
    )
    type = models.CharField(
        max_length=15,
        verbose_name='Формат',
        choices=DAT_SYS_KEY.TYPE_LIST,
        help_text='К какому типу будет относиться вносимое значение',
        default='text',
    )
    list = models.ForeignKey(
        ModelList,
        verbose_name='Закрепленный список',
        related_name='ind_list',
        on_delete=models.CASCADE,
        help_text='Подключение, при необходимости, дополнительного списка',
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=25,
        verbose_name='Имя латиницей',
        help_text='Данное сокращение будет использоваться при написании скриптов',
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=50,
        verbose_name='Имя классификатора',
    )
    hint = models.TextField(
        max_length=255,
        verbose_name='Всплывающая подсказка',
        help_text='Дополнительная информация для пользователя, который будет вносить данные',
        blank=True,
        null=True,
    )
    descript = models.TextField(
        max_length=1024,
        verbose_name='Дополнительные пометки',
        help_text='Дополнительная информация о классификаторе для администраторов',
        blank=True,
        null=True,
    )
    rel_obj_1 = models.ForeignKey(
        ModelObject,
        on_delete=models.CASCADE,
        verbose_name='Первый объект для связи',
        related_name=DAT_SYS_KEY.IND_REL_OBJ_1,
        blank=True,
        null=True,
    )
    rel_obj_2 = models.ForeignKey(
        ModelObject,
        on_delete=models.CASCADE,
        verbose_name='Второй объект для связи',
        related_name=DAT_SYS_KEY.IND_REL_OBJ_2,
        blank=True,
        null=True,
    )
    priority = models.IntegerField(
        verbose_name='Приоритет',
        help_text=' Приоритет при именовании',
    )
    visible = models.CharField(
        max_length=20,
        verbose_name='Режим отображения',
        choices=DAT_SYS_KEY.VISIBLE_LIST,
        help_text='Как будет отображаться данный классификатор в заголовках',
        default='all'
    )
    blocked_blank = models.BooleanField(
        default=False,
        verbose_name='Не использовать в бланках',
        help_text='Данное поле не включается в файл классификаторов',
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Переопределенная функция сохранения для переупорядочивания объектов в связи в зависимости от их идентификатора
        @param args: стандартный параметр
        @param kwargs: стандартный параметр
        """
        if not self.priority and self.obj_id != 1:
            return
        if self.obj_id == 1:
            if self.rel_obj_1_id > self.rel_obj_2_id:
                temp_id = self.rel_obj_1_id
                self.rel_obj_1_id = self.rel_obj_2_id
                self.rel_obj_2_id = temp_id
        super().save(*args, **kwargs)
        DAT_SYS_KEY.DUMP.update()

    class Meta:
        unique_together = (DAT_SYS_KEY.TITLE, DAT_SYS_KEY.OBJ, DAT_SYS_KEY.COL, DAT_SYS_KEY.REL_OBJ_1_ID,
                           DAT_SYS_KEY.REL_OBJ_2_ID, DAT_SYS_KEY.TYPE_VAL, DAT_SYS_KEY.LIST_ID)
        managed = False
        db_table = DAT_SYS_KEY.TABLE_SHORT
        verbose_name = "Классификатор"
        verbose_name_plural = "Классификаторы"


class Manual(models.Model):
    file = models.FileField(upload_to=MANUAL_ROOT)

    def __str__(self):
        return self.file.name.split('/')[1]

    class Meta:
        verbose_name = "Инструкцию"
        verbose_name_plural = "Инструкция"


@receiver(models.signals.post_delete, sender=Manual)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Manual)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Manual.objects.get(pk=instance.pk).file
    except Manual.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

