from django.core.exceptions import ValidationError
from django.db import models
from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_LIST_TOP, DAT_SYS_KEY, DAT_SYS_LIST_DOP


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
        if self.id == None:
            try:
                self.save()
            except Exception as e:
                raise e

    def save(self, *args, **kwargs):
        if len(ModelListDop.objects.filter(list=self.list).filter(val=self.val)) > 0:
            raise ValidationError('в данном списке уже есть такой элемент')
        else:
            super().save(*args, **kwargs)

    class Meta:
        managed = False
        verbose_name = "Поле списка"
        verbose_name_plural = "Поля списков"
        db_table = DAT_SYS_LIST_DOP.TABLE_SHORT


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
    type_val = models.CharField(
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
    descript = models.CharField(
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

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = DAT_SYS_KEY.TABLE_SHORT
        verbose_name = "Классификатор"
        verbose_name_plural = "Классификаторы"
