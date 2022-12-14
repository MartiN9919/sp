import os

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from classifier.models import ModelObject, ModelList
from data_base_driver.constants.const_dat import DAT_SYS_SCRIPT, DAT_SYS_TRIGGER, DAT_SYS_SCRIPT_VARIABLE, \
    DAT_SYS_TRIGGER_VARIABLE
from data_base_driver.constants.const_script import BASE_PATH_TO_USER_SCRIPTS
from data_base_driver.constants.const_trigger import BASE_PATH_TO_USER_TRIGGERS
from data_base_driver.script.script_parsec import parse_text_to_python
from data_base_driver.trigger.trigger_parser import parse_trigger_text_to_python
from authentication.models import ModelOwnerLines

class ModelScript(models.Model):
    """
    Модель таблицы sys_script для регистрирования ее на странице аднимистратора.
    Необходимо для возможности добавления скриптов со стороны администратора.
    """
    or_condition = Q()  # Создание Q объекта, для хранения допустимых инструкций для фильтрации
    for key, value in DAT_SYS_SCRIPT.ICON_CHOICES:  # Цикл, для последовательного получения допустимых значений для фильтрации
        or_condition.add(Q(**{'icon': key}), Q.OR)  # Заполнение объекта, значениями формата: {'icon': (значение ключа)}

    id = models.PositiveSmallIntegerField(
        primary_key=True,
    )

    parent = models.ForeignKey(
        to='self',
        verbose_name='Папка',
        limit_choices_to=or_condition,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
    )
    title = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='Отображаемое название скрипта',
        unique=True,
    )
    icon = models.CharField(
        max_length=25,
        verbose_name='Иконка',
        choices=DAT_SYS_SCRIPT.ICON_CHOICES,
        help_text='Устанавливается только для папки',
        blank=True,
        null=True,
        default=None,
    )
    hint = models.CharField(
        max_length=255,
        verbose_name='Подсказка',
        help_text='Всплывающая подсказка',
        blank=True,
        default='',
    )
    content = models.TextField(
        verbose_name='Скрипт',
        help_text='Текст скрипта',
        blank=True,
        default='',
    )
    descript = models.TextField(
        verbose_name='Описание',
        help_text='Описание скрипта',
    )
    variables = models.TextField(
        verbose_name='Переменные',
        help_text='Формат (name variables):(type variables)',
        blank=True,
        default='',
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name='Вкл',
        help_text='Доступность скрипта',
    )
    owner = models.ForeignKey(
        ModelOwnerLines,
        on_delete=models.CASCADE,
        verbose_name='Линия',
        blank=True,
    )
    type = models.CharField(
        max_length=20,
        choices=DAT_SYS_SCRIPT.TYPE_LIST,
        verbose_name='Тип',
    )

    def __str__(self):
        return self.title

    def clean(self, *args, **kwargs):
        """
        Функция для проверки правильности синтаксиса написанного скрипта
        @param args: стандартный список параметров
        @param kwargs: стандартный список параметров
        """
        if not self.icon:
            status, error_str, error_code, error_type = parse_text_to_python('script_test', self.content,
                                                                             ModelScriptVariable.objects.filter(
                                                                                 script_id=self.id), self.type)
            if not status:
                raise ValidationError(
                    'ошибка в синтаксисе скрипта, в строке: ' + error_str + ', ' + error_code + str(error_type))
            else:
                os.remove(BASE_PATH_TO_USER_SCRIPTS + 'script_test.py')

    def save(self, *args, **kwargs):
        """
        Функция для переопределения сохранения модели, добавлено сохранение файла в папку пользовательских скриптов
        @param args: стандартный список параметров
        @param kwargs: стандартный список параметров
        """
        super().save(*args, **kwargs)
        if not self.icon:
            parse_text_to_python('script_' + str(ModelScript.objects.get(title=self.title).id), self.content,
                                 ModelScriptVariable.objects.filter(script_id=self.id), self.type)

    def delete(self, using=None, keep_parents=False):
        """
        Функция для удаления скрипта, удаляет как из базы данных, так и из файловой системы
        @param using:
        @param keep_parents:
        """
        if not self.icon:
            os.remove(BASE_PATH_TO_USER_SCRIPTS + 'script_' + str(self.id) + '.py')
        super().delete()

    class Meta:
        managed = False
        db_table = DAT_SYS_SCRIPT.TABLE_SHORT
        verbose_name = "Скрипт"
        verbose_name_plural = "Скрипты"


class ModelScriptVariable(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название переменной',
        help_text='Будет использоваться в теле скрипта',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Имя переменной',
        help_text='Будет отображаться пользователю',
    )
    hint = models.CharField(
        max_length=255,
        verbose_name='Подсказка',
        help_text='Будет отображаться пользователю',
    )
    type = models.CharField(
        max_length=25,
        verbose_name='Тип переменной',
        choices=DAT_SYS_SCRIPT_VARIABLE.TYPE_VARIABLE_LIST,
        help_text='',
        default='text',
    )
    list = models.ForeignKey(
        ModelList,
        verbose_name='Закрепленный список',
        on_delete=models.CASCADE,
        help_text='Какой список использовать для выбора',
        blank=True,
        null=True,
    )
    obj = models.ForeignKey(
        ModelObject,
        verbose_name='Объект',
        on_delete=models.CASCADE,
        help_text='По какому объекту осуществлять поиск',
        blank=True,
        null=True,
    )
    script = models.ForeignKey(
        ModelScript,
        verbose_name='Скрипт',
        on_delete=models.CASCADE,
        help_text='По какому объекту осуществлять поиск',
    )
    necessary = models.BooleanField(
        default=True,
        verbose_name='Обязательная',
        help_text='Является ли данная переменная обязательной для данного списка',
    )

    def clean(self):
        if self.type == 'list' and not self.list_id:
            raise ValidationError('У переменной типа списка не задан список')
        elif self.type != 'list' and self.list_id:
            raise ValidationError('Данная переменная не является списком')
        elif self.type != 'search' and self.obj_id:
            raise ValidationError('Данная переменная не является поиском объекта')

    def save(self, *args, **kwargs):
        self.script_id = ModelScript.objects.get(title=self.script.title).id
        super().save(*args, **kwargs)
        script = ModelScript.objects.get(title=self.script.title)
        script.save()

    class Meta:
        managed = False
        db_table = DAT_SYS_SCRIPT_VARIABLE.TABLE_SHORT
        verbose_name = "Переменная скрипта"
        verbose_name_plural = "Переменные скриптов"


class ModelTrigger(models.Model):
    object = models.ForeignKey(
        ModelObject,
        verbose_name='объект',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=50,
        verbose_name='Название Триггера',
        help_text='Будет отображаться в меню настройки триггеров',
        unique=True,
    )
    content = models.TextField(
        verbose_name='Текст скрипта триггера',
        help_text='Поле ввода скрипта триггера',
        blank=True,
        default='',
    )
    variables = models.TextField(
        verbose_name='Переменные',
        help_text='Введите переменные формата (name variables):(type variables)',
        blank=True,
        default='',
    )
    hint = models.TextField(
        max_length=255,
        verbose_name='Всплывающая подсказка',
        help_text='Ввод текста подсказки, которая будет отображаться в меню выбора анализа',
        blank=True,
        default='',
    )

    def save(self, *args, **kwargs):
        """
        Функция для переопределения сохранения модели, добавлено сохранение файла в папку пользовательских триггеров
        @param args: стандартный список параметров
        @param kwargs: стандартный список параметров
        """
        super().save(*args, **kwargs)
        parse_trigger_text_to_python('trigger_' + str(self.id), self.content, self.variables)

    def delete(self, using=None, keep_parents=False):
        """
        Функция для удаления триггера, удаляет как из базы данных, так и из файловой системы
        @param using:
        @param keep_parents:
        """
        os.remove(BASE_PATH_TO_USER_TRIGGERS + 'trigger_' + str(self.id) + '.py')
        super().delete()

    class Meta:
        managed = False
        db_table = DAT_SYS_TRIGGER.TABLE_SHORT
        verbose_name = "Тригеры"
        verbose_name_plural = "Триггеры"


class ModelTriggerVariable(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название переменной',
        help_text='Будет использоваться в теле триггера',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Имя переменной',
        help_text='Будет отображаться пользователю',
    )
    hint = models.CharField(
        max_length=255,
        verbose_name='Всплывающая подсказка',
        help_text='Будет отображаться пользователю',
    )
    type = models.CharField(
        max_length=25,
        verbose_name='Тип переменной',
        choices=DAT_SYS_SCRIPT_VARIABLE.TYPE_VARIABLE_LIST,
        help_text='К какому типу будет относиться переменная',
        default='text',
    )
    list = models.ForeignKey(
        ModelList,
        verbose_name='Закрепленный список',
        on_delete=models.CASCADE,
        help_text='Какой список использовать для выбора',
        blank=True,
        null=True,
    )
    obj = models.ForeignKey(
        ModelObject,
        verbose_name='Объект',
        on_delete=models.CASCADE,
        help_text='По какому объекту осуществлять поиск',
        blank=True,
        null=True,
    )
    trigger = models.ForeignKey(
        ModelTrigger,
        verbose_name='Триггер',
        on_delete=models.CASCADE,
        help_text='Триггер для данной переменной',
    )
    necessary = models.BooleanField(
        default=True,
        verbose_name='Обязательная',
        help_text='Является ли данная переменная обязательной для данного списка',
    )

    def clean(self):
        if self.type == 'list' and not self.list_id:
            raise ValidationError('У переменной типа списка не задан список')
        elif self.type != 'list' and self.list_id:
            raise ValidationError('Данная переменная не является списком')
        elif self.type != 'search' and self.obj_id:
            raise ValidationError('Данная переменная не является поиском объекта')

    def save(self, *args, **kwargs):
        self.trigger_id = ModelTrigger.objects.get(title=self.trigger.title).id
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = DAT_SYS_TRIGGER_VARIABLE.TABLE_SHORT
        verbose_name = "Переменная триггера"
        verbose_name_plural = "Переменные триггеров"
