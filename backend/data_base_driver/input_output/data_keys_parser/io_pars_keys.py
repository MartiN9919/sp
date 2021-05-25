from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_KEY, DAT_OBJ_COL, DAT_OBJ_ROW, DAT_REL

DEBUG = False


###########################################
# РАСПАРСИТЬ KEYS ДЛЯ OBJ И REL (КАК ROW)
# ДЛЯ ПОСЛЕДУЮЩИХ SQL-ЗАПРОСОВ
# col_select/row_select - список аргументов SELECT
# col_key   /row_key    - список ключей
###########################################
class IO_PARS_KEYS(dict):
    # ключи dict
    COL_SELECT = 'col_select'  # [ 'name', 'ST_AsGeoJSON(location) AS location' ]
    ROW_SELECT = 'row_select'  # [ 'id', key_id', 'val', 'dat'] / ['key_id', 'dat', 'obj_id_1', 'rec_id_1', 'obj_id_2', 'rec_id_2']

    COL_KEY = 'col_key'  # [ '40301', 'location', ... ]
    ROW_KEY = 'row_key'  # [ '40304', ... ]
    ALL_KEY = 'all_key'  # BOOL все ключи

    COL_TABLE = 'col_table'
    ROW_TABLE = 'row_table'

    def __init__(self, obj, keys=[]):
        self.obj_id = DAT_SYS_OBJ.DUMP.to_id(val=obj)
        self.obj_name = DAT_SYS_OBJ.DUMP.to_name(val=obj)

        self.col_key = self[self.COL_KEY] = []
        self.row_key = self[self.ROW_KEY] = []
        self.all_key = self[self.ALL_KEY] = len(keys) == 0

        fun = self.__init_obj__ if self.obj_id != DAT_SYS_OBJ.ID_REL else self.__init_rel__
        fun(keys=keys)

    ###########################################
    # EXIST
    ###########################################
    def col_exist(self):
        return len(self.col_key) > 0

    def row_exist(self):
        return (len(self.row_key) > 0) or self.all_key

    ###########################################
    # ВНУТРЕННИЕ ФУНКЦИИ
    ###########################################
    def __init_obj__(self, keys=[]):
        self.col_table = self[self.COL_TABLE] = DAT_OBJ_COL.table_name(self.obj_name)
        self.row_table = self[self.ROW_TABLE] = DAT_OBJ_ROW.table_name(self.obj_name)

        self.col_select = self[self.COL_SELECT] = ['id']
        self.row_select = self[self.ROW_SELECT] = ['id'] + list(DAT_OBJ_ROW.LIST)

        # при отсутствии списка ключей - только col-ключи, перечислять row-ключи НЕ ЦЕЛЕСООБРАЗНО, т.к. их много и они указываются в SQL IN (...)
        if self.all_key:
            tmp = DAT_SYS_KEY.DUMP.get_rec(obj_id=self.obj_id, col=True, only_first=False)
            keys = list(map(lambda x: x[DAT_SYS_KEY.ID], tmp))

        for keys_item in keys:
            # исключение col: "name1 as name2"
            if isinstance(keys_item, str):
                lst = keys_item.lower().split(' as ', maxsplit=1)
                if len(lst) > 1:
                    self.col_select.append(keys_item)
                    self.col_key.append(lst[1])
                    continue

            rec = DAT_SYS_KEY.DUMP.get_rec(obj_id=self.obj_id, val=keys_item)

            # COL
            if rec[DAT_SYS_KEY.COL]:
                self.col_select.append(rec[DAT_SYS_OBJ.NAME])
                self.col_key.append(str(rec[DAT_SYS_OBJ.ID]))

            # ROW
            else:
                self.row_key.append(str(rec[DAT_SYS_OBJ.ID]))

    def __init_rel__(self, keys=[]):
        self.row_table = self[self.ROW_TABLE] = DAT_REL.TABLE_SHORT # изменено для работы тестов
        self.row_select = self[self.ROW_SELECT] = list(DAT_REL.LIST)

        for keys_item in keys:
            rec = DAT_SYS_KEY.DUMP.get_rec(obj_id=DAT_SYS_OBJ.ID_REL, val=keys_item)
            self.row_key.append(str(rec[DAT_SYS_OBJ.ID]))
