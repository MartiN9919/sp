from django.db import models
from authentication.models import ModelCustomUser
from official_documents.models import ModelOfficialDocument
from data_base_driver.constants.const_dat import DAT_SYS_NOTIFY
from datetime import datetime


class ModelNotification(models.Model):
    """
    Класс модели оповещений
    """
    from_user = models.ForeignKey(
        ModelCustomUser,
        on_delete=models.RESTRICT,
        verbose_name='От кого',
        related_name=DAT_SYS_NOTIFY.FROM_USER,
        help_text='Выберите пользователя, от которого будет отправлено уведомление.',
    )
    to_user = models.ForeignKey(
        ModelCustomUser,
        on_delete=models.RESTRICT,
        verbose_name='Кому',
        related_name=DAT_SYS_NOTIFY.TO_USER,
        help_text='Выберите пользователя, которому будет отправлено уведомление.',
    )
    date_time = models.CharField(
        max_length=30,
        verbose_name='Дата создания уведомления',
        help_text='Поле заполняется в автоматическом режиме.',
    )
    type = models.CharField(
        max_length=14,
        choices=DAT_SYS_NOTIFY.TYPE_LIST,
        verbose_name='Тип уведомления',
    )
    content = models.TextField(
        verbose_name='Тест сообщения',
    )
    file = models.ForeignKey(
        ModelOfficialDocument,
        on_delete=models.RESTRICT,
        verbose_name='прикрепленный для скачивания файл',
        help_text='Выберите необходимый файл из списка',
        null=True,
        blank=True,
    )
    geometry = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.type

    def save(self,  *args, **kwargs):
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return super(ModelNotification, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = DAT_SYS_NOTIFY.TABLE_SHORT
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
