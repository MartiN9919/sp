from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from authentication.managers import CustomUserManager
from data_base_driver.constants.const_dat import DAT_OWNER_GROUPS,DAT_OWNER_USERS, \
    DAT_OWNER_GROUPS_REL, DAT_OWNER_LINES, DAT_OWNER


class ModelOwnerLines(models.Model):
    """
    Класс для описания модели линии доступа по направлению деятельности
    """
    parent_id = models.IntegerField(
        verbose_name='Родитель',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        DAT_OWNER.DUMP.update()

    class Meta:
        managed = False
        db_table = DAT_OWNER_LINES.TABLE_SHORT
        verbose_name = "Линия"
        verbose_name_plural = "Линии"


class ModelOwnerGroups(models.Model):
    """
    Класс для описания модели группы доступа
    """
    id = models.CharField(
        max_length=255,
        verbose_name='ID',
        primary_key=True,
        editable = False,
        blank=False,

    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название группы',
    )
    descript = models.CharField(
        max_length=255,
        verbose_name='Дополнительное описание',
        null=True,
        blank=True,
    )
    owner_lines_id = models.CharField(
        max_length=255,
        verbose_name='Линия',
        null=True,
        blank=True,
    )
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        DAT_OWNER.DUMP.update()

    class Meta:

        managed = False
        db_table = DAT_OWNER_GROUPS.TABLE_SHORT
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class ModelOwnerGroupsRel(models.Model):
    """
    Класс для описания модели группы доступа
    """
    node_id = models.ForeignKey(
        ModelOwnerGroups,
        db_column='node_id',
        related_name='person2',
        on_delete=models.CASCADE,
        verbose_name='Группа для связи',
    )

    parent_id = models.ForeignKey(
        ModelOwnerGroups,
        db_column='parent_id',
        related_name='person2persons',
        on_delete=models.CASCADE,
        verbose_name='Узел',
    )

    read_only = models.BooleanField(
        db_index=True,
        verbose_name='Только чтение',
    )

    descript = models.CharField(
        max_length=255,
        verbose_name='Дополнительное описание',
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        DAT_OWNER.DUMP.update()

    def __str__(self):
        return str(self.node_id) +' > '+ str(self.parent_id)

    class Meta:
        managed = False
        db_table = DAT_OWNER_GROUPS_REL.TABLE_SHORT
        verbose_name = "Группу связей"
        verbose_name_plural = "Группы связей"


class ModelCustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Класс для описания модели настраиваемого пользователя
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_write = models.BooleanField(
        default=False,
        verbose_name='Право на запись',
        help_text='Имеет ли пользователь права на запись/изменеие данных'
    )
    owner_groups = models.ForeignKey(
        ModelOwnerGroups,
        on_delete=models.CASCADE,
        verbose_name='Группа доступа',
        help_text='Указывает группу, к которой относится пользователь.',
        null=True,
    )

    objects = CustomUserManager()
    USERNAME_FIELD = DAT_OWNER_USERS.USERNAME
    REQUIRED_FIELDS = [DAT_OWNER_USERS.LAST_NAME, DAT_OWNER_USERS.FIRST_NAME, DAT_OWNER_USERS.OWNER_GROUPS_ID]

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        DAT_OWNER.DUMP.update()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
