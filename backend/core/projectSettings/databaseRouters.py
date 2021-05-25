from data_base_driver.constants.connect_db import VEC_DATA
from data_base_driver.constants.const_dat import (DAT_SYS_NOTIFY,
                                                  DAT_SYS_SCRIPT,
                                                  DAT_OWNER_LINES,
                                                  DAT_SYS_KEY,
                                                  DAT_SYS_LIST_TOP,
                                                  DAT_SYS_OBJ,
                                                  DAT_SYS_LIST_DOP,
                                                  )


class AccountRouter(object):
    """
    Рутер базы данных
    """
    TABLES_DATA = (
        DAT_SYS_NOTIFY.TABLE_SHORT,
        DAT_SYS_SCRIPT.TABLE_SHORT,
        DAT_OWNER_LINES.TABLE_SHORT,
        DAT_SYS_KEY.TABLE_SHORT,
        DAT_SYS_LIST_TOP.TABLE_SHORT,
        DAT_SYS_OBJ.TABLE_SHORT,
        DAT_SYS_LIST_DOP.TABLE_SHORT,
    )

    def db_for_read(self, model, **hints):
        return VEC_DATA['NAME'] if model._meta.db_table in self.TABLES_DATA else None

    def db_for_write(self, model, **hints):
        return VEC_DATA['NAME'] if model._meta.db_table in self.TABLES_DATA else None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.db_table in self.TABLES_DATA or \
                obj2._meta.db_table in self.TABLES_DATA:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # if app_label=='map':
        #     return db == CONNECT.SYS.NAME
        return None
