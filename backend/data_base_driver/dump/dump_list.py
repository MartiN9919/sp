import threading
import time

from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_LIST_DOP


class DUMP_LIST:
    def __init__(self, refreshDelay=60 * 30):  # refreshDelay - время хранения кэша, в секундах
        self.dump = None
        self.refreshDelay = refreshDelay
        self.refreshTime = time.time() - 1
        self._lock = threading.Lock()
        self._refresh_()

    def _refresh_(self, force=False):
        if not force and (self.refreshTime > time.time()): return
        with self._lock:
            self.dump = {}
            dat = db_sql(sql=
                'SELECT ' + DAT_SYS_LIST_DOP.ID + ',' \
                + DAT_SYS_LIST_DOP.VAL + ' FROM ' \
                + DAT_SYS_LIST_DOP.TABLE_SHORT + ';')
            for value in dat:
                self.dump[value[0]] = value[1]
            # актуальность дампа
            self.refreshTime = time.time() + self.refreshDelay

    def get_all(self):
        self._refresh_()
        return self.dump

    def get_item_by_id(self, id):
        return self.dump.get(id)
