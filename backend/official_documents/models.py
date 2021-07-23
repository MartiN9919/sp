from django.db import models
from authentication.models import ModelOwnerLines, ModelOwnerRegions
from data_base_driver.constants.const_dat import DAT_SYS_FILES


class ModelOfficialDocument(models.Model):
    """
    Класс модели для представления официальных документов
    """
    path = models.CharField(
        max_length=255,
        verbose_name='Путь к файлу'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Имя файла',
    )
    owner_line = models.ForeignKey(
        ModelOwnerLines,
        on_delete=models.RESTRICT,
        verbose_name='Линия',
    )
    owner_region = models.ForeignKey(
        ModelOwnerRegions,
        on_delete=models.RESTRICT,
        verbose_name='Регион',
    )
    date_auto_remove = models.DateTimeField(
        verbose_name='Дата и время удаления файла'
    )

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = DAT_SYS_FILES.TABLE_SHORT
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
