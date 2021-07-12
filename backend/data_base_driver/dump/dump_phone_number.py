import threading
import time

from data_base_driver.connect.connect_mysql import DB_sql
from data_base_driver.constants.const_dat import DAT_SYS_PHONE_NUMBER_FORMAT
from data_base_driver.dump.transform_functions import tuple_to_dict_many


class DUMP_PHONE_NUMBER_FORMAT:
    def __init__(self, refreshDelay=60 * 30):  # refreshDelay - время хранения кэша, в секундах
        self.dump = None
        self.refreshDelay = refreshDelay
        self.refreshTime = time.time() - 1
        self._lock = threading.Lock()
        self._refresh_()


    def _refresh_(self, force=False):
        if not force and (self.refreshTime > time.time()): return
        with self._lock:
            db = DB_sql()
            dat = db.execute(
                sql=
                "SELECT " +
                DAT_SYS_PHONE_NUMBER_FORMAT.ID + ", " +
                DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY + ", " +
                DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY_CODE + ", " +
                DAT_SYS_PHONE_NUMBER_FORMAT.LENGTH +
                " FROM " +
                DAT_SYS_PHONE_NUMBER_FORMAT.TABLE_SHORT + ";",
                wait=True,
                read=True
            )
            self.dump = tuple_to_dict_many(dat, [
                DAT_SYS_PHONE_NUMBER_FORMAT.ID,
                DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY,
                DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY_CODE,
                DAT_SYS_PHONE_NUMBER_FORMAT.LENGTH,
            ])

            # актуальность дампа
            self.refreshTime = time.time() + self.refreshDelay

    def get_all(self):
        self._refresh_()
        return self.dump

