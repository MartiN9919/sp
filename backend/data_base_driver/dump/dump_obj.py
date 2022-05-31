import threading
import time
from data_base_driver.constants.const_dat import DAT_SYS_OBJ
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.dump.transform_functions import tuple_to_dict_many, dict_filter


##################################################################################
# DAT_SYS_OBJ.DUMP
##################################################################################
class DUMP_OBJ:
    def __init__(self, refreshDelay=60 * 30):  # refreshDelay - время хранения кэша, в секундах
        self.dump = None
        self.refreshDelay = refreshDelay
        self.refreshTime = time.time() - 1
        self._lock = threading.Lock()
        self._refresh_()


    def _refresh_(self, force=False):
        if not force and (self.refreshTime > time.time()): return
        with self._lock:
            dat = db_sql(
                sql=
                "SELECT " +
                DAT_SYS_OBJ.ID + ", " +
                DAT_SYS_OBJ.NAME + ", " +
                DAT_SYS_OBJ.TITLE + ", " +
                DAT_SYS_OBJ.TITLE_SINGLE + ", " +
                DAT_SYS_OBJ.ICON + ", " +
                DAT_SYS_OBJ.DESCRIPT + ", " +
                DAT_SYS_OBJ.PRIORITY + " " +
                "FROM " +
                DAT_SYS_OBJ.TABLE_SHORT + ";",
                wait=True,
                read=True
            )
            self.dump = tuple_to_dict_many(dat, [
                DAT_SYS_OBJ.ID,
                DAT_SYS_OBJ.NAME,
                DAT_SYS_OBJ.TITLE,
                DAT_SYS_OBJ.TITLE_SINGLE,
                DAT_SYS_OBJ.ICON,
                DAT_SYS_OBJ.DESCRIPT,
                DAT_SYS_OBJ.PRIORITY,
            ])

            # актуальность дампа
            self.refreshTime = time.time() + self.refreshDelay

    def get_all(self):
        self._refresh_()
        return self.dump

    def get_rec(self, id=None, name=None):
        self._refresh_()
        list_key_val = []
        if id != None: list_key_val.append((DAT_SYS_OBJ.ID, id))
        if name != None: list_key_val.append((DAT_SYS_OBJ.NAME, name))
        rec = dict_filter(list_dict=self.dump, list_key_val=list_key_val, only_first=True)
        if len(rec) != 1: raise Exception('Unknow obj: ' + (str(id) if id else '') + (str(name) if name else ''))
        return rec[0]

    # val: DAT_SYS_OBJ.ID или DAT_SYS_OBJ.NAME (str или int)   например: 'geometry', 'rel', 5
    # ret: {name: ... , id: ...}
    # Error - ничего не найдено
    def to_id(self, val):
        return self.get_rec(name=val)[DAT_SYS_OBJ.ID] if isinstance(val, str) else val

    def to_name(self, val):
        return self.get_rec(id=val)[DAT_SYS_OBJ.NAME] if isinstance(val, int) else val

