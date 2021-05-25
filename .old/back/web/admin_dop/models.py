from   django.db                    import models
from   lib.db.const.const_connect   import CONNECT
from   lib.db.const.const_dat       import DAT_SYS_ALERT


##################################################################################
#   РОУТЕР БАЗ ДАННЫХ
##################################################################################
class AccountRouter(object):
    TABLES_DATA = (
        DAT_SYS_ALERT.TABLE_SHORT,
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



##################################################################################
# DAT_SYS_ALERT
##################################################################################
class Model_Alerts(models.Model):
    content    = models.CharField                (verbose_name='Содержание',         unique=False, blank=False, default='', max_length=255, )
    type       = models.CharField                (verbose_name='Тип',                unique=False, blank=False, default=DAT_SYS_ALERT.TYPE_ERROR, choices=DAT_SYS_ALERT.TYPE_LIST, max_length=8)
    wait       = models.PositiveSmallIntegerField(verbose_name='Время показа, сек.', unique=False, blank=False, default=0,  help_text='0 - не ограничено')
    owner      = models.CharField                (verbose_name='Владелец',           unique=False, blank=True,  default='', max_length=5)
    users      = models.CharField                (verbose_name='Пользователи',       unique=False, blank=True,  default='', max_length=255)
    group_user = models.CharField                (verbose_name='Группы',             unique=False, blank=True,  default='', max_length=255)
    descript   = models.CharField                (verbose_name='Примечание',         unique=False, blank=True,  default='', max_length=255)
    enabled    = models.BooleanField             (verbose_name='Доступно',           unique=False, blank=False, default=True)
    #refresh   = models.DateTimeField            (                                   unique=False, blank=True,  auto_now=True)

    class Meta:
        db_table            = DAT_SYS_ALERT.TABLE_SHORT
        verbose_name        = "уведомление"
        verbose_name_plural = "уведомления"
        managed             = False								# дабы django не пытался создать эту таблицу при syncdb
