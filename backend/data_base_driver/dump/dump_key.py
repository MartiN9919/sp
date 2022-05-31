import threading
import time
from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_KEY
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.dump.transform_functions import tuple_to_dict_many, dict_filter


##################################################################################
# DAT_SYS_KEY.DUMP
# если name==None -> name=str(id) - только dop
##################################################################################
class DUMP_KEY:
    def __init__(self, refreshDelay=60 * 30):  # refreshDelay - время хранения кэша, в секундах
        self.dump = None
        self.owners = None
        self.refreshDelay = refreshDelay
        self.refreshTime = time.time() - 1
        self._lock = threading.Lock()
        self._refresh_()

    def _refresh_(self, force=False):
        if not force and (self.refreshTime > time.time()): return
        with self._lock:
            sql = "SELECT " + \
                  DAT_SYS_KEY.ID + "," + \
                  DAT_SYS_KEY.OBJ_ID + "," + \
                  DAT_SYS_KEY.COL + "," + \
                  DAT_SYS_KEY.NEED + "," + \
                  DAT_SYS_KEY.TYPE_VAL + "," + \
                  DAT_SYS_KEY.LIST_ID + "," + \
                  DAT_SYS_KEY.NAME + "," + \
                  DAT_SYS_KEY.TITLE + "," + \
                  DAT_SYS_KEY.HINT + ", " + \
                  DAT_SYS_KEY.DESCRIPT + ", " + \
                  DAT_SYS_KEY.REL_OBJ_1_ID + ", " + \
                  DAT_SYS_KEY.REL_OBJ_2_ID + ", " + \
                  DAT_SYS_KEY.PRIORITY + ", " + \
                  DAT_SYS_KEY.VISIBLE + ", " + \
                  DAT_SYS_KEY.BLOCKED_IN_BLANK + " " + \
                  "FROM " + \
                  DAT_SYS_KEY.TABLE_SHORT + " " + \
                  "ORDER BY " + \
                  DAT_SYS_KEY.COL + " DESC, " + \
                  DAT_SYS_KEY.NEED + " DESC;"
            dat = db_sql(sql=sql, wait=True, read=True)
            dat = dat + ((0, 0, 0, 0, 'text', None, 'any', 'Примечание', 'Дополнительная информация об объекте', '',
                          0, 0, 200, 1, 1),
                         (1, 0, 0, 0, 'file_any', None, 'file_any', 'Файловое примечание',
                          'Дополнительные файлы характеризующие объект', '', 0, 0, 200, 1, 1))
            self.dump = tuple_to_dict_many(dat, [
                DAT_SYS_KEY.ID,
                DAT_SYS_KEY.OBJ_ID,
                DAT_SYS_KEY.COL,
                DAT_SYS_KEY.NEED,
                DAT_SYS_KEY.TYPE_VAL,
                DAT_SYS_KEY.LIST_ID,
                DAT_SYS_KEY.NAME,
                DAT_SYS_KEY.TITLE,
                DAT_SYS_KEY.HINT,
                DAT_SYS_KEY.DESCRIPT,
                DAT_SYS_KEY.REL_OBJ_1_ID,
                DAT_SYS_KEY.REL_OBJ_2_ID,
                DAT_SYS_KEY.PRIORITY,
                DAT_SYS_KEY.VISIBLE,
                DAT_SYS_KEY.BLOCKED_IN_BLANK
            ])
            # если name==None -> name=str(id) - только dop
            for ind, item in enumerate(self.dump):
                if item[DAT_SYS_KEY.COL] == b'\x01': continue
                if item[DAT_SYS_KEY.NAME] in (None, ''): self.dump[ind][DAT_SYS_KEY.NAME] = str(item[DAT_SYS_KEY.ID])

            # словарь индексов групп-владельцев owner_id
            self.owners = {}

            def find_element_in_list(list_element, element):
                try:
                    return list_element.index(element)
                except ValueError:
                    return -1

            for item in self.dump:
                ind = find_element_in_list(list_element=DAT_SYS_KEY.NAME_OWNER_LIST, element=item[DAT_SYS_KEY.NAME])
                if ind < 0: continue
                val = self.owners.get(item[DAT_SYS_KEY.OBJ_ID], [-1, -1, -1, -1, -1])
                val[ind] = item[DAT_SYS_KEY.ID]
                self.owners[item[DAT_SYS_KEY.OBJ_ID]] = val

            # актуальность дампа
            self.refreshTime = time.time() + self.refreshDelay

    def update(self):
        self.refreshTime = time.time() - 1

    # и/или id, и/или name, и/или val (val может быть id или name), и/или col
    def get_rec(self, obj_id=None, id=None, name=None, val=None, col=None, only_first=True, visible=True):
        self._refresh_()
        list_key_val = []
        if id != None:
            list_key_val.append((DAT_SYS_KEY.ID, id))
            return dict_filter(list_dict=self.dump, list_key_val=list_key_val, only_first=True)[0]
        if obj_id != None:        list_key_val.append((DAT_SYS_KEY.OBJ_ID, obj_id))
        if name != None:        list_key_val.append((DAT_SYS_KEY.NAME, name))
        if isinstance(val, str): list_key_val.append((DAT_SYS_KEY.NAME, val))
        if isinstance(val, int): list_key_val.append((DAT_SYS_KEY.ID, val))
        if col != None:          list_key_val.append((DAT_SYS_KEY.COL, col))
        rec = dict_filter(list_dict=self.dump, list_key_val=list_key_val, only_first=only_first) \
            if len(list_key_val) > 0 else self.dump

        if only_first:
            if len(rec) != 1: raise Exception(
                'Unknown key: ' + (str(id) if id else '') + (str(name) if name else '') + (str(val) if val else ''))
            return rec[0]
        else:
            return rec

    # val: DAT_SYS_KEY.ID или DAT_SYS_KEY.NAME (str или int)   например: 'ngg_migrate', 121
    # Error - ничего не найдено
    def to_id(self, obj_id, val):
        return self.get_rec(obj_id=obj_id, name=val)[DAT_SYS_KEY.ID] if isinstance(val, str) else val

    def to_name(self, obj_id, val):
        return self.get_rec(obj_id=obj_id, id=val)[DAT_SYS_KEY.NAME] if isinstance(val, int) else val

    # val: rel.key_id   str или int   например: 'ngg_migrate', 121
    def rel_to_id(self, val):
        return self.to_id(obj_id=DAT_SYS_OBJ.ID_REL, val=val)

    def rel_to_name(self, val):
        return self.to_name(obj_id=DAT_SYS_OBJ.ID_REL, val=val)
