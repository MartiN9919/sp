import datetime

from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_KEY, DAT_OBJ_ROW, DAT_OBJ_COL, DAT_REL

DEBUG = False


###########################################
# РАСПАРСИТЬ DAT
# ДЛЯ ПОСЛЕДУЮЩИХ SQL-ОПЕРАЦИЙ
# (ГОТОВЫЕ СТРОКИ ДЛЯ ФОРМИРОВАНИЯ SQL)
# add={'sys_key': True} - добавить ссылки на записи классификаторов: col_key, row_key
# valid - проверка на уникальность ключей и наличие обязательных ключей (только rel)
###########################################
class IO_PARS_DATA(dict):
    FIELD_ID = 'id'
    FIELD_OBJ_1 = 'obj_1'
    FIELD_OBJ_2 = 'obj_2'

    ADD_SYS_KEY = 'sys_key'

    # ключи dict
    REC_ID = 'rec_id'  # property: str
    OBJ_ID = 'obj_id'
    OBJ_NAME = 'obj_name'

    COL_KEY = 'col_key'  # запись DAT_SYS_KEY
    ROW_KEY = 'row_key'

    COL_DIC = 'col_dic'
    ROW_DIC = 'row_dic'

    COL_TABLE = 'col_table'
    ROW_TABLE = 'row_table'

    def __init__(self, obj, data, add={}, valid=True):
        self.valid = valid
        self[self.REC_ID] = None

        # OBJ
        obj_rec = DAT_SYS_OBJ.DUMP.get_rec(id=DAT_SYS_OBJ.DUMP.to_id(obj))

        self.obj_id = self[self.OBJ_ID] = obj_rec[DAT_SYS_OBJ.ID]
        self.obj_name = self[self.OBJ_NAME] = obj_rec[DAT_SYS_OBJ.NAME]

        self.col_dic = self[self.COL_DIC] = []
        self.row_dic = self[self.ROW_DIC] = []

        fun = self.__init_obj__ if self.obj_id != DAT_SYS_OBJ.ID_REL else self.__init_rel__
        fun(data=data, add=add)

    ###########################################
    # REC_ID - PROPERTY
    ###########################################
    rec_id = property()

    @rec_id.getter
    def rec_id(self):
        return self[self.REC_ID]

    @rec_id.setter
    def rec_id(self, value):
        if (not value in [None, 0, '']) and (self[self.REC_ID] == None):
            self[self.REC_ID] = str(value)

    ###########################################
    # EXIST
    ###########################################
    def col_exist(self):
        return len(self.col_dic) > 0

    def row_exist(self):
        return len(self.row_dic) > 0

    ###########################################
    # КОРРЕКТНОЕ ЗНАЧЕНИЕ VAL ДЛЯ SQL
    ###########################################
    def val(self, type, val):
        if type in [DAT_SYS_KEY.TYPE_STR, DAT_SYS_KEY.TYPE_DATA, DAT_SYS_KEY.TYPE_PHONE_NUMBER,
                    DAT_SYS_KEY.TYPE_FILE_PHOTO, DAT_SYS_KEY.TYPE_FILE_ANY]:
            ret = "'" + str(val) + "'"
        elif type == DAT_SYS_KEY.TYPE_GEOMETRY:
            ret = "ST_GeomFromGeoJson('" + val + "')"
        else:
            ret = str(val)
        return ret

    ###########################################
    # EQU
    ###########################################
    # is_null=False: {'key_id': '40403', 'val': '255', 'dat': 'null'} ==> ['key_id=40403', 'val=255', 'dat=null']
    equ_item = lambda self, item_dic, is_null: [
        item + (('=' + item_dic[item]) if (not is_null) or item_dic[item] != 'null' else ' is null') for item in
        item_dic]

    # obj_col:                [['type=4'], ["path='tests/new2'"]]
    # obj_row, is_null=True:  [['key_id=40403', 'val=255', 'dat is null'], ['key_id=40405', "val='zzz'", "dat='2019-01-01'"], ...]
    # obj_row, is_null=False: [['key_id=40403', 'val=255', 'dat=null'],    ['key_id=40405', "val='zzz'", "dat='2019-01-01'"], ...]
    # rel,     is_null=True:  [['key_id=120'], ['obj_id_1=4'], ['obj_id_2=5', 'rec_id_2=100'], ['dat is null']]
    # rel,     is_null=False: [['key_id=120'], ['obj_id_1=4'], ['obj_id_2=5', 'rec_id_2=100'], ['dat=null'   ]]
    col_equ = lambda self, is_null=True: self.__equ__(dic=self.col_dic, is_null=is_null)
    row_equ = lambda self, is_null: self.__equ__(dic=self.row_dic, is_null=is_null)
    __equ__ = lambda self, dic, is_null: [self.equ_item(item_dic=item_dic, is_null=is_null) for item_dic in
                                          dic]  # INSERT - is_null = True

    # obj_col:                ['type=4', "path='tests/new2'"]
    # obj_row, is_null=True:  ['key_id=40403', 'val=255', 'dat is null', 'key_id=40404', "val='77777'", 'dat is null', ...]
    # obj_row, is_null=False: ['key_id=40403', 'val=255', 'dat=null',    'key_id=40404', "val='77777'", 'dat=null',    ...]
    # rel,     is_null=True:  ['key_id=120', 'obj_id_1=4', 'obj_id_2=5', 'rec_id_2=100', 'dat is null']
    # rel,     is_null=False: ['key_id=120', 'obj_id_1=4', 'obj_id_2=5', 'rec_id_2=100', 'dat=null'   ]
    col_equ_flat = lambda self, is_null=True: self.__equ_flat__(dic=self.col_dic, is_null=is_null)
    row_equ_flat = lambda self, is_null: self.__equ_flat__(dic=self.row_dic, is_null=is_null)

    def __equ_flat__(self, dic, is_null):  # INSERT - is_null = True
        ret = []
        for item_dic in dic:
            ret += self.equ_item(item_dic=item_dic, is_null=is_null)
        return ret

    ###########################################
    # KEY
    ###########################################
    row_key_flat = lambda self: self.__key_flat__(dic=self.row_dic)

    def __key_flat__(self, dic):
        ret = []
        for item_dic in dic:
            for item in item_dic: ret.append(item)
        return ret

    ###########################################
    # ВНУТРЕННИЕ ФУНКЦИИ
    ###########################################
    def __init_obj__(self, data, add):
        DATA_KEY = 0
        DATA_VAL = 1
        DATA_DAT = 2

        # data_item = [DATA_KEY, DATA_VAL, [DATA_DAT]]
        for data_item in data:
            # исключение: id
            if data_item[DATA_KEY] == self.FIELD_ID:
                self.rec_id = data_item[DATA_VAL]
                continue

            key_id = DAT_SYS_KEY.DUMP.to_id(obj_id=self.obj_id, val=data_item[DATA_KEY])
            key_name = DAT_SYS_KEY.DUMP.to_name(obj_id=self.obj_id, val=data_item[DATA_KEY])
            key_rec = DAT_SYS_KEY.DUMP.get_rec(obj_id=self.obj_id, id=key_id)
            if not key_rec: raise Exception('Unknow key: ' + str(key_id))
            val = self.val(key_rec[DAT_SYS_KEY.TYPE_VAL], data_item[DATA_VAL])

            # COL
            if key_rec[DAT_SYS_KEY.COL]:
                if add.get(self.ADD_SYS_KEY, False): self.col_key.append(key_rec)
                self.col_dic.append({key_name: val, DAT_OBJ_COL.DAT: '\'' + data_item[DATA_DAT] + '\''})
            # ROW
            else:
                if add.get(self.ADD_SYS_KEY, False): self.row_key.append(key_rec)
                self.row_dic.append({
                    DAT_OBJ_ROW.KEY_ID: str(key_id),
                    DAT_OBJ_ROW.VAL: val,
                    DAT_OBJ_ROW.DAT: '\'' + data_item[DATA_DAT] + '\'' if len(
                        data_item) > 2 else '\'' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\''
                })

        if self.valid:
            self.__valid__()

        self.col_table = self[self.COL_TABLE] = DAT_OBJ_COL.table_name(self.obj_name)
        self.row_table = self[self.ROW_TABLE] = DAT_OBJ_ROW.table_name(self.obj_name)

    def __init_rel__(self, data, add):
        DATA_KEY = 0
        DATA_VAL1 = 1
        DATA_VAL2 = 2

        vals = {}
        is_dat = False
        is_1 = False
        is_2 = False

        # data_item = [DATA_KEY/ID, DATA_VAL1, [DATA_VAL2]]
        for data_item in data:
            data_key = data_item[DATA_KEY]
            data_val1 = data_item[DATA_VAL1]

            if data_key in (self.FIELD_OBJ_1, DAT_REL.OBJ_ID_1, DAT_REL.REC_ID_1): is_1 = True
            if data_key in (self.FIELD_OBJ_2, DAT_REL.OBJ_ID_2, DAT_REL.REC_ID_2): is_2 = True

            # ['key_id',10], ['key_id','ngg_smoke'],
            if data_key == DAT_REL.KEY_ID:
                key_id = DAT_SYS_KEY.DUMP.to_id(obj_id=self.obj_id, val=data_val1)
                if add.get(self.ADD_SYS_KEY, False): self.row_key.append(
                    DAT_SYS_KEY.DUMP.get_rec(obj_id=self.obj_id, id=key_id))
                vals[DAT_REL.KEY_ID] = str(key_id)
                continue

            # ['val', 'УД'] дописать с учетом появления значения у связи
            if data_key == DAT_REL.VAL:
                if data_val1 == 0:
                    vals[DAT_REL.VAL] = '\'\''
                else:
                    vals[DAT_REL.VAL] = '\'' + str(data_val1) + '\''
                continue

            if data_key == DAT_REL.DOCUMENT_ID:
                if not data_val1 or data_val1 == 0:
                    vals[DAT_REL.DOCUMENT_ID] = '\'\''
                else:
                    vals[DAT_REL.DOCUMENT_ID] = '\'' + str(data_val1) + '\''
                continue

            # ['obj_1',5,100], ['obj_2','file']
            elif data_key in (self.FIELD_OBJ_1, self.FIELD_OBJ_2):
                obj_id = DAT_SYS_OBJ.DUMP.to_id(val=data_val1)
                key = DAT_REL.OBJ_ID_1 if data_key == self.FIELD_OBJ_1 else DAT_REL.OBJ_ID_2
                vals[key] = str(obj_id)

                if len(data_item) > 2:
                    key = DAT_REL.REC_ID_1 if data_key == self.FIELD_OBJ_1 else DAT_REL.REC_ID_2
                    vals[key] = str(data_item[DATA_VAL2])
                continue

            # ['obj_id_1','file'], ['obj_id_2',5],
            elif data_key in (DAT_REL.OBJ_ID_1, DAT_REL.OBJ_ID_2):
                obj_id = DAT_SYS_OBJ.DUMP.to_id(val=data_val1)
                vals[data_key] = str(obj_id)
                continue

            # ['rec_id_2',5],
            elif data_key in (DAT_REL.REC_ID_1, DAT_REL.REC_ID_2):
                vals[data_key] = str(data_val1)
                continue


            # ['dat','2020-09-07'],
            elif data_key == DAT_REL.DAT:
                vals[data_key] = self.val(type=DAT_SYS_KEY.TYPE_DATA, val=data_val1)
                is_dat = True
                continue

            # ['file',200], [4,200],
            else:
                if is_1 and is_2: raise Exception('Too many key: ' + data_key)
                obj_id = DAT_SYS_OBJ.DUMP.to_id(val=data_key)
                if not is_1:
                    key_obj = DAT_REL.OBJ_ID_1
                    key_rec = DAT_REL.REC_ID_1
                    is_1 = True
                else:
                    key_obj = DAT_REL.OBJ_ID_2
                    key_rec = DAT_REL.REC_ID_2
                    is_2 = True
                vals[key_obj] = str(obj_id)
                vals[key_rec] = str(data_val1)
                continue

        # dat is null
        if not is_dat:
            vals[DAT_REL.DAT] = '\'' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\''
        vals[DAT_REL.REC_ID] = '0'

        self.row_dic.append(vals)

        # проверка записи
        if self.valid:
            self.__valid__()

        # порядок следования obj/rec_1 и obj/rec_2
        item = self.row_dic[0]
        # obj_id с меньшим индексом всегда obj_id_1
        if int(item[DAT_REL.OBJ_ID_1]) > int(item[DAT_REL.OBJ_ID_2]):
            item[DAT_REL.OBJ_ID_1], item[DAT_REL.OBJ_ID_2] = item[DAT_REL.OBJ_ID_2], item[DAT_REL.OBJ_ID_1]
            item[DAT_REL.REC_ID_1], item[DAT_REL.REC_ID_2] = item[DAT_REL.REC_ID_2], item[DAT_REL.REC_ID_1]
        # если obj_id равны: rec_id с меньшим индексом всегда rec_id_1
        elif item[DAT_REL.OBJ_ID_1] == item[DAT_REL.OBJ_ID_2] and \
                int(item[DAT_REL.REC_ID_1]) > int(item[DAT_REL.REC_ID_2]):
            item[DAT_REL.REC_ID_1], item[DAT_REL.REC_ID_2] = item[DAT_REL.REC_ID_2], item[DAT_REL.REC_ID_1]
        # если obj_id и rec_id равны: ошибка - связь объекта с самим собой
        elif item[DAT_REL.OBJ_ID_1] == item[DAT_REL.OBJ_ID_2] and \
                item[DAT_REL.REC_ID_1] == item[DAT_REL.REC_ID_2]:
            raise Exception('OBJ/REC_1 == OBJ/REC_2: ' + item[DAT_REL.OBJ_ID_1] + ', ' + item[DAT_REL.REC_ID_1])

        self.col_table = self[self.COL_TABLE] = None
        self.row_table = self[self.ROW_TABLE] = DAT_REL.TABLE_SHORT

    ###########################################
    # ПРОВЕРКА ЗАПИСИ
    ###########################################
    def __valid__(self):
        # OBJ
        if self.obj_id != DAT_SYS_OBJ.ID_REL:
            self.__valid_uniq__(dic=self.col_dic, fun=self.__equ_flat__)
            self.__valid_uniq__(dic=self.row_dic, fun=self.__equ__)
        # REL
        else:
            self.__valid_uniq__(dic=self.row_dic, fun=self.__equ_flat__)
            self.__valid_key_flat__(dic=self.row_dic, keys=DAT_REL.LIST)

    # проверка на уникальность ключ-значение
    def __valid_uniq__(self, dic, fun):
        lst = fun(dic=dic, is_null=True)
        tmp = [str(item) for item in lst if item[0:3] != 'dat']
        if len(tmp) != len(set(tmp)): raise Exception('Found of dublicates key: ' + str(tmp))

    # проверка на присутствие обязательных ключей
    def __valid_key_flat__(self, dic, keys):
        keys2 = self.__key_flat__(dic=dic)
        for item_keys in keys:
            if not item_keys in keys2: raise Exception("Not found key '" + str(item_keys) + "' in " + str(keys2))
