from django.db import models
from django.db.models import Q
from lib.db.const.const_connect import CONNECT
from lib.db.const.const_dat import DAT_SYS_ALERT, DAT_SYS_SCRIPT, DAT_OWNER_LINES
from lib.db.script.script_exec import parse_text_to_python


class AccountRouter(object):
    """
    Рутер базы данных
    """

    TABLES_DATA = (
        DAT_SYS_ALERT.TABLE_SHORT,
        DAT_SYS_SCRIPT.TABLE_SHORT,
        DAT_OWNER_LINES.TABLE_SHORT
    )

    def db_for_read(self, model, **hints):
        return CONNECT.DATA.NAME if model._meta.db_table in self.TABLES_DATA else None

    def db_for_write(self, model, **hints):
        return CONNECT.DATA.NAME if model._meta.db_table in self.TABLES_DATA else None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.db_table in self.TABLES_DATA or \
                obj2._meta.db_table in self.TABLES_DATA:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # if app_label=='map':
        #     return db == CONNECT.SYS.NAME
        return None


class ModelAlerts(models.Model):
    """
    Модель таблицы sys_alert для регистрирования ее на странице аднимистратора
    Необходимо для возможности добавления уведомлений со стороны администратора
    """

    content = models.CharField(
        verbose_name='Содержание',
        unique=False,
        blank=False,
        max_length=255,
    )
    type = models.CharField(
        verbose_name='Тип',
        unique=False,
        blank=False,
        default=DAT_SYS_ALERT.TYPE_ERROR,
        choices=DAT_SYS_ALERT.TYPE_LIST,
        max_length=8,
    )
    wait = models.PositiveSmallIntegerField(
        verbose_name='Время показа, сек.',
        unique=False,
        blank=False,
        default=0,
        help_text='0 - не ограничено',
    )
    owner = models.CharField(
        verbose_name='Владелец',
        unique=False,
        blank=True,
        default='',
        max_length=5,
    )
    users = models.CharField(
        verbose_name='Пользователи',
        unique=False,
        blank=True,
        default='',
        max_length=255,
    )
    group_user = models.CharField(
        verbose_name='Группы',
        unique=False,
        blank=True,
        default='',
        max_length=255,
    )
    descript = models.CharField(
        verbose_name='Примечание',
        unique=False,
        blank=True,
        default='',
        max_length=255,
    )
    enabled = models.BooleanField(
        verbose_name='Доступно',
        unique=False,
        blank=False,
        default=True,
    )

    class Meta:
        db_table = DAT_SYS_ALERT.TABLE_SHORT
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        managed = False


class ModelOwnerLine(models.Model):
    """
    Модель таблицы owner_lines для связывания ее с таблицей sys_script
    Данная модель расширяет страницу создания скрипта и дает возможность
    выбирать создателя из имеющегося списка, хранящегося в owner_lines
    """

    parent_id = models.IntegerField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = DAT_OWNER_LINES.TABLE_SHORT


class ModelScript(models.Model):
    """
    Модель таблицы sys_script для регистрирования ее на странице аднимистратора
    Необходимо для возможности добавления скриптов со стороны администратора
    """

    ICON_CHOICES = [
        ('HOME', 'home_icon'),
        ('APPLE', 'apple_icon'),
        ('CELERY', 'celery_icon'),
        ('CAR', 'car_icon'),
        ('CAT', 'cat_icon'),
    ]

    or_condition = Q()  # Создание Q объекта, для хранения допустимых инструкций для фильтрации
    for key, value in ICON_CHOICES:  # Цикл, для последовательного получения допустимых значений для фильтрации
        or_condition.add(Q(**{'icon': key}), Q.OR)  # Заполнение объекта, значениями формата: {'icon': (значение ключа)}

    id = models.PositiveSmallIntegerField(
        primary_key=True,
    )

    parent = models.ForeignKey(
        to='self',
        verbose_name='Родительский id',
        limit_choices_to=or_condition,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название Скрипта',
        help_text='Данное название будет отображаться в меню выбора анализа',
        unique=True,
    )
    icon = models.CharField(
        max_length=25,
        verbose_name='Иконка',
        choices=ICON_CHOICES,
        help_text='Данная иконка будет отображаться в меню выбора анализа',
        blank=True,
        default=None,
    )
    hint = models.CharField(
        max_length=255,
        verbose_name='Всплывающая подсказка',
        help_text='Ввод тектса подсказки, которая будет отображаться в меню выбора анализа',
        blank=True,
        default='',
    )
    content = models.TextField(
        verbose_name='Текст скрипта',
        help_text='Поле ввода скрипта',
        blank=True,
        default='',
    )
    descript = models.TextField(
        verbose_name='Описание объекта',
        help_text='Введите описание данного объекта',
    )
    variables = models.CharField(
        max_length=255,
        verbose_name='Переменные',
        help_text='Введите переменные формата (name variables):(type variables)',
        blank=True,
        default='',
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name='Состояние',
        help_text='Включение/отключение скрипта',
    )
    owner = models.ForeignKey(
        ModelOwnerLine,
        on_delete=models.CASCADE,
        verbose_name='Группа владельцев',
        blank=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Парсинг поля контента в исполняемый файл"""
        super().save(*args, **kwargs)
        print(self.icon)
        if not self.icon:
            parse_text_to_python('script_' + str(ModelScript.objects.get(name=self.name).id), self.content, self.variables)



    class Meta:
        managed = False
        db_table = DAT_SYS_SCRIPT.TABLE_SHORT
        verbose_name = "Скрипт"
        verbose_name_plural = "Скрипты"
