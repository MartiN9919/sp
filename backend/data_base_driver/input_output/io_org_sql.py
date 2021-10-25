import datetime

from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_OBJ_COL, DAT_OBJ_ROW, DAT_REL
from data_base_driver.input_output.io_lib_sql import IO_LIB_SQL

DEBUG = False


###########################################
# MY_SQL: ОРГАНАЙЗЕР ВЗАИМОДЕЙСТВИЯ С БД
###########################################
class IO_ORG_SQL():
    def __init__(self):
        self.io_sql = IO_LIB_SQL()

    def __del__(self):
        del self.io_sql

    ###########################################
    # ЗАПИСАТЬ OBJ/REL
    ###########################################
    # данные ТОЛЬКО по одному объекту
    # если id не задано: ВСЕГДА INSERT
    # если id    задано: в COL UPDATE если есть
    ###########################################
    def set(self, data_pars):
        self._set_col_(data_pars)
        self._set_row_(data_pars)

    # ЗАПИСАТЬ COL - ВСТАВКА ИЛИ ОБНОВЛЕНИЕ
    def _set_col_(self, data_pars):
        if not data_pars.col_exist(): return

        # rec_id НЕ известно
        if not data_pars.rec_id:
            # создать rec_id и вставить col-запись (проверять на повтор и обновлять не нужно)
            data_pars.rec_id = self.io_sql.obj_rec_id_new(obj_id=data_pars.obj_id)
            self.io_sql.obj_insert_col_one(data_pars=data_pars)

        # rec_id известно:
        else:
            # перевести проверку на manticore
            # проверить на полный повтор повтор записи в БД
            rec = self.io_sql.select(table=data_pars.col_table, select=['1'],
                                     where=['rec_id=' + data_pars.rec_id, ] + data_pars.col_equ_flat(), only_first=True)
            if len(rec) > 0:
                if DEBUG: print('Skip set col-obj: RECORD EXIST')
                return
            self.io_sql.obj_insert_col_one(data_pars=data_pars)

    # ЗАПИСАТЬ ROW - ТОЛЬКО ВСТАВКА
    def _set_row_(self, data_pars):
        if not data_pars.row_exist(): return

        # OBJ
        if data_pars.obj_id != DAT_SYS_OBJ.ID_REL:
            # rec_id НЕ известно
            if not data_pars.rec_id:
                # создать rec_id и вставить ОДНОЙ опрацией без проверки на повторы
                data_pars.rec_id = self.io_sql.obj_rec_id_new(obj_id=data_pars.obj_id)

                # надо вернуть с учетом обработки после комита
                # if self.io_sql.obj_insert_row_all(data_pars=data_pars) != len(data_pars.row_dic):
                    # raise Exception('Error insert row: data_pars = ' + str(data_pars))

                self.io_sql.obj_insert_row_all(data_pars=data_pars)

            # rec_id известно
            else:
                # проверка на повтор и вставка КАЖДОГО ключа/записи в отдельности (обновлять не нужно)
                # row_equ: {'key_id': '40403', 'val': '255', 'dat': 'null'}
                for ind, item in enumerate(data_pars.row_equ(is_null=True)):
                    # rec = self.io_sql.select(table=data_pars.row_table, select=['1'],
                    #                          where=['rec_id=' + data_pars.rec_id, ] + item, only_first=True)
                    # if len(rec) > 0:
                    #     if DEBUG: print('Skip set row-obj: RECORD EXIST')
                    #     continue
                    self.io_sql.obj_insert_row_one(data_pars=data_pars, ind=ind)

        # REL
        else:
            rec_id = self.io_sql.obj_rec_id_new(obj_id=data_pars.obj_id)
            data_pars.row_dic[0]['rec_id'] = str(rec_id)
            data_pars.rec_id = rec_id
            # проверить на повтор записи в БД
            rec = self.io_sql.select(table=data_pars.row_table, select=['1'],
                                     where=data_pars.row_equ_flat(is_null=True), only_first=True)
            if len(rec) > 0:
                if DEBUG: print('Skip set rel: RECORD EXIST')
                return
            self.io_sql.rel_insert_one(data_pars=data_pars)

    ###########################################
    # ПРОЧИТАТЬ OBJ / ГЕНЕРАТОР
    ###########################################
    def get_obj(self, keys_pars, ids=[], ids_max_block=None, where_dop_row=[]):
        def __read__(where_ids):
            # при отсутствии списка ключей перечислять row-ключи НЕ ЦЕЛЕСООБРАЗНО, т.к. их много
            where_keys_row = [] if keys_pars.all_key else [
                DAT_OBJ_ROW.KEY_ID + ' IN (' + ','.join([str(i) for i in keys_pars.row_key]) + ')', ]

            if keys_pars.col_exist():
                for item in self.__get_obj_col__(keys_pars=keys_pars, where=where_ids): yield item
            if keys_pars.row_exist():
                for item in self.__get_obj_row__(keys_pars=keys_pars,
                                                 where=where_ids + where_keys_row + where_dop_row): yield item

        # если есть ids: читать блоками
        if len(ids) > 0:
            if ids_max_block == None: ids_max_block = 1000
            for ids_ind in range(0, len(ids), ids_max_block):
                yield from __read__(
                    where_ids=['rec_id IN (' + ','.join([str(i) for i in ids[ids_ind:ids_ind + ids_max_block]]) + ')', ])
        # если нет ids
        else:
            yield from __read__(where_ids=[])

    def __get_obj_col__(self, keys_pars, where, only_first=False):
        # rec_item - очередная col-запись ['id', 'type', 'path'],
        for rec_item in self.io_sql.select(table=keys_pars.col_table, select=keys_pars.col_select, where=where,
                                           only_first=only_first):
            # одна col-запись (один id) - несколько col-ключей
            # col_key_item - очередной ключ
            for col_key_ind, col_key_item in enumerate(keys_pars.col_key,
                                                       1):  # начать с 1 т.к. col_key[0]=id (см.select_fld)
                if rec_item[
                    col_key_ind] == None: continue  # пустые значения пропустить, т.к. в col запись читается целиком
                if col_key_item.isnumeric(): col_key_item = int(col_key_item)  # если ключ-число - перевести в int
                yield (rec_item[0], col_key_item, rec_item[col_key_ind])  # один col-ключ   - одна запись data

    def __get_obj_row__(self, keys_pars, where):
        # rec_item - очередная row-запись: ['id', 'key_id', 'val', 'dat']
        for rec_item in self.io_sql.select(table=keys_pars.row_table, select=keys_pars.row_select, where=where,
                                           only_first=False):
            yield tuple(
                map(lambda x: str(x) if isinstance(x, datetime.datetime) else x, list(rec_item)))  # дату-время в строку

    ###########################################
    # ПРОЧИТАТЬ REL / ГЕНЕРАТОР
    ###########################################
    # ПРОВЕРКА ЗАПИСЕЙ НА ПОВТОРЫ (ВАРИАНТЫ 1,2) НЕ ВЕДЕТСЯ
    ###########################################
    def get_rel(self, keys_pars, rels_pars, where_dop=[]):
        where = where_dop

        # при отсутствии списка ключей перечислять ключи НЕ ЦЕЛЕСООБРАЗНО, т.к. их много
        where += [] if keys_pars.all_key else [
            DAT_REL.KEY_ID + ' IN (' + ','.join([str(i) for i in keys_pars.row_key]) + ')', ]

        # rec_item - очередная row-запись: ['key_id', 'dat', 'obj_id_1', 'rec_id_1', 'obj_id_2', 'rec_id_2']
        # вариант 1
        for rec_item in self.io_sql.select(table=keys_pars.row_table, select=keys_pars.row_select,
                                           where=where + rels_pars.equ_1, only_first=False):
            yield tuple(
                map(lambda x: str(x) if isinstance(x, datetime.datetime) else x, list(rec_item)))  # дату-время в строку

        # вариант 2
        if len(rels_pars.equ_2) > 0:
            for rec_item in self.io_sql.select(table=keys_pars.row_table, select=keys_pars.row_select,
                                               where=where + rels_pars.equ_2, only_first=False):
                yield tuple(map(lambda x: str(x) if isinstance(x, datetime.datetime) else x,
                                list(rec_item)))  # дату-время в строку

    ###########################################
    # УДАЛИТЬ (ТОЛЬКО ТЕСТЫ)
    ###########################################
    def _del_(self, obj, rec_id):
        obj_id = str(DAT_SYS_OBJ.DUMP.to_id(obj))
        obj_name = DAT_SYS_OBJ.DUMP.to_name(obj)
        rec_id = str(rec_id)

        # удалить связи объекта
        self.io_sql._delete_(
            table=DAT_REL.TABLE,
            where= \
                "((" + DAT_REL.OBJ_ID_1 + "=" + obj_id + ") AND (" + DAT_REL.REC_ID_1 + "=" + rec_id + ")) OR " + \
                "((" + DAT_REL.OBJ_ID_2 + "=" + obj_id + ") AND (" + DAT_REL.REC_ID_2 + "=" + rec_id + "))",
            only_first=False)

        # удалить объект
        if obj_id != str(DAT_SYS_OBJ.ID_FREE):
            self.io_sql._delete_(table=DAT_OBJ_COL.table_name(obj_name), where="id=" + rec_id, only_first=True)
        self.io_sql._delete_(table=DAT_OBJ_ROW.table_name(obj_name), where="id=" + rec_id, only_first=False)
