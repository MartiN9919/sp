from django.db import models
from authentication.models import ModelCustomUser
from data_base_driver.sys_notifications.get_notifications_info import get_alert_json
from sockets.consumers import send_notification
from official_documents.models import ModelOfficialDocument
from data_base_driver.constants.const_dat import DAT_SYS_NOTIFY


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
    date_time = models.DateTimeField(
        auto_now_add=True,
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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Переопределенная функция сохранения модели с добавлением отправки оповещения по каналу
        @param force_insert: стандартный параметр
        @param force_update: стандартный параметр
        @param using: стандартный параметр
        @param update_fields: стандартный параметр
        """
        super(ModelNotification, self).save()
        from_user = ModelCustomUser.objects.get(id=self.from_user_id).username
        notification = get_alert_json(
            (self.id, from_user, self.content, self.date_time.replace(tzinfo=None, microsecond=0),
             self.type, self.file_id, self.geometry,))
        send_notification(self.to_user_id, notification)

    class Meta:
        managed = False
        db_table = DAT_SYS_NOTIFY.TABLE_SHORT
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
