from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from authentication.managers import CustomUserManager
from data_base_driver.constants.const_dat import DAT_OWNER_GROUPS, DAT_OWNER_LINES, DAT_OWNER_REGIONS, DAT_OWNER_USERS


class ModelOwnerRegions(models.Model):
    parent_id = models.IntegerField(
        verbose_name='Родительский объект',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название региона',
    )

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = DAT_OWNER_REGIONS.TABLE_SHORT
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"


class ModelOwnerLines(models.Model):
    parent_id = models.IntegerField(
        verbose_name='Родительский объект',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название линии',
    )

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = DAT_OWNER_LINES.TABLE_SHORT
        verbose_name = "Линия"
        verbose_name_plural = "Линии"


class ModelOwnerGroups(models.Model):
    owner_regions = models.ForeignKey(
        ModelOwnerRegions,
        on_delete=models.CASCADE,
        verbose_name='Регион',
        help_text='Указывает на регион, к которому относится группа.',
    )
    owner_lines = models.ForeignKey(
        ModelOwnerLines,
        on_delete=models.CASCADE,
        verbose_name='Линия',
        help_text='Указывает на линию, к которой относится группа.',
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

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = DAT_OWNER_GROUPS.TABLE_SHORT
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class ModelCustomUser(AbstractBaseUser, PermissionsMixin):
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

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
