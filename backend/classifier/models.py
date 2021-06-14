from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_LIST_TOP, DAT_SYS_KEY, DAT_SYS_LIST_DOP, \
    DAT_SYS_KEY_GROUP


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
    descript = models.CharField(
        max_length=255,
        verbose_name='Дополнительные пометки',
        help_text='Дополнительная информация о объекте',
        blank=True,
        null=True,
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

    def save(self, *args, **kwargs):
        if ModelList.objects.filter(name=self.name):
            return
        else:
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
    list = models.ForeignKey(
        ModelList,
        on_delete=models.CASCADE,
    )

    def clean(self):
        if not self.list_id:
            ModelList.save(self.list)
        self.fl = 0  # костыль, потом изменить
        if self.id == None:
            try:
                self.save()
            except Exception as e:
                raise e

    def save(self, *args, **kwargs):
        if len(ModelListDop.objects.filter(list=self.list).filter(val=self.val)) > 0 and self.fl == 0:
            raise ValidationError('в данном списке уже есть такой элемент')
        else:
            self.fl = 1
            super().save(*args, **kwargs)


    class Meta:
        managed = False
        verbose_name = "Поле списка"
        verbose_name_plural = "Поля списков"
        db_table = DAT_SYS_LIST_DOP.TABLE_SHORT


class ModelKeyGroup(models.Model):
    obj = models.ForeignKey(
        ModelObject,
        verbose_name='Объект',
        related_name='ind_obj_пкщгз',
        on_delete=models.CASCADE,
        help_text='К какому объекту относится данная группа',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название группы',
        help_text='Название группы',
        blank=True,
        null=True,
    )
    pos = models.IntegerField(
        verbose_name='Приоритет группы',
        help_text='Необходим для сортировки',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = DAT_SYS_KEY_GROUP.TABLE_SHORT
        verbose_name = "Группа классификатора"
        verbose_name_plural = "Группа классификатора"


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
        max_length=10,
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
    hint = models.CharField(
        max_length=255,
        verbose_name='Всплывающая подсказка',
        help_text='Дополнительная информация для пользователя, который будет вносить данные',
        blank=True,
        null=True,
    )
    descript = models.TextField(
        max_length=255,
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
    path = models.CharField(
        max_length=255,
        verbose_name='Путь',
        help_text='Путь',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.obj_id == 1:
            if self.rel_obj_1_id > self.rel_obj_2_id:
                temp_id = self.rel_obj_1_id
                self.rel_obj_1_id = self.rel_obj_2_id
                self.rel_obj_2_id = temp_id
        super().save(*args, **kwargs)


    class Meta:
        unique_together = (DAT_SYS_KEY.TITLE, DAT_SYS_KEY.OBJ, DAT_SYS_KEY.COL, DAT_SYS_KEY.REL_OBJ_1_ID,
                           DAT_SYS_KEY.REL_OBJ_2_ID, DAT_SYS_KEY.TYPE_VAL, DAT_SYS_KEY.LIST_ID)
        managed = False
        db_table = DAT_SYS_KEY.TABLE_SHORT
        verbose_name = "Классификатор"
        verbose_name_plural = "Классификаторы"
