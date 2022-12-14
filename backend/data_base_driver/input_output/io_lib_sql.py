import datetime
from data_base_driver.connect.connect_mysql import db_sql, connect_to_data_base
from data_base_driver.constants.const_dat import DAT_SYS_ID, DAT_OBJ_ROW
from data_base_driver.input_output.add_object_http import add_row_record_http, add_relation_http, add_col_record_http, \
    update_col_record_http

DEBUG = False


###########################################
# MY_SQL: БИБЛИОТЕКА ФУНКЦИЙ ДОСТУПА К SQL
###########################################
class IO_LIB_SQL():
    def __init__(self):
        self.connection = connect_to_data_base()


    def __del__(self):
        self.connection.free_connection()
    ###########################################
    # REC_ID
    ###########################################
    # + получить rec_id для нового элемента obj
    def obj_rec_id_new(self, obj_id):
        # в одно обращение к БД без чтения с блокировкой
        ret = self.__sql_exec__(
            sql="UPDATE " + DAT_SYS_ID.TABLE + " SET id = LAST_INSERT_ID(id + 1) WHERE " + DAT_SYS_ID.OBJ_ID + "=" + str(
                obj_id), read=False)
        ret = ret[0]
        if ret == 0: raise Exception('Unknow get new id for obj.' + str(obj_id))
        return ret

    ###########################################
    # INSERT
    ###########################################
    # + запись всех col-ключей: ОДНОЙ sql-операцией => ОДНА запись
    def obj_insert_col_one(self, data_pars):
        if not data_pars.rec_id: raise Exception('Unknow rec_id: data_pars = ' + str(data_pars))
        sql = "INSERT IGNORE INTO " + data_pars.col_table + " " + \
            "SET " + ', '.join(['rec_id=' + data_pars.rec_id] + [item for item in data_pars.col_equ_flat()
                                                                 if not item.startswith('dat')] +
                               [[item for item in data_pars.col_equ_flat() if item.startswith('dat')][0]])
        add_col_record_http(data_pars.col_table, data_pars.rec_id, data_pars.col_equ_flat())
        self.__sql_exec__(sql, read=False)

    # + запись ОДНОГО row-ключа ОДНОЙ sql-операцией => ОДНА запись
    obj_insert_row_one = lambda self, data_pars, ind: self.insert_one_rec( #возможны проблемы из-за замены стандартной функции
        table=data_pars.row_table,
        equ=['rec_id=' + data_pars.rec_id, ] + data_pars.equ_item(item_dic=data_pars.row_dic[ind], is_null=False)
    )

    # + запись ВСЕХ row-ключей ОДНОЙ sql-операцией => НЕСКОЛЬКО записей
    def obj_insert_row_all(self, data_pars):
        if not data_pars.rec_id: raise Exception('Unknow rec_id: data_pars = ' + str(data_pars))
        val_list = []

        for item in data_pars.row_dic:
            val_list.append(
                "(" + \
                data_pars.rec_id + ", " + \
                item[DAT_OBJ_ROW.KEY_ID] + ", " + \
                item[DAT_OBJ_ROW.VAL] + ", " + \
                item.get(DAT_OBJ_ROW.DAT, 'null') + \
                ")"
            )
            date_time_str = item.get(DAT_OBJ_ROW.DAT, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            date_time_str = date_time_str.replace('\'', '')
            add_row_record_http(data_pars.row_table, data_pars.rec_id, date_time_str, item[DAT_OBJ_ROW.KEY_ID],
                                item[DAT_OBJ_ROW.VAL].replace('\'',''))

        sql = \
            "INSERT IGNORE " + data_pars.row_table + " (" + \
            DAT_OBJ_ROW.ID + ", " + \
            DAT_OBJ_ROW.KEY_ID + ", " + \
            DAT_OBJ_ROW.VAL + ", " + \
            DAT_OBJ_ROW.DAT + \
            ") VALUES " + ", ".join(val_list)

        self.__sql_exec__(sql=sql, read=False)
        return self.connection.get_connection().affected_rows()

    # + запись ОДНОЙ связи => ОДНА запись
    rel_insert_one = lambda self, data_pars: self.insert_one_rec(
        table=data_pars.row_table,
        equ=data_pars.row_equ_flat(is_null=False)
    )

    # + вставить ОДНУ запись, self.connection.insert_id() не читает если id присутствует в SET
    rec_insert_one = lambda self, table, equ: self.__sql_exec__(
        sql="INSERT IGNORE INTO " + table + " SET " + ', '.join(equ), read=False)

    def insert_one_rec(self, table, equ):
        sql = "INSERT IGNORE INTO " + table + " SET " + ', '.join(equ)
        if len(equ) == 4:
            add_row_record_http(table,
                                int(equ[0].split('=')[1]),
                                equ[3].split('=')[1].replace('\'', ''),
                                equ[1].split('=')[1],
                                equ[2][equ[2].find('=') + 1:].replace('\'', '')
                                )
        else:
            if not add_relation_http(int(equ[8].split('=')[1]),
                              equ[5].split('=')[1].replace('\'', ''),
                              int(equ[0].split('=')[1]),
                              int(equ[1].split('=')[1]),
                              int(equ[2].split('=')[1]),
                              int(equ[3].split('=')[1]),
                              int(equ[4].split('=')[1]),
                              equ[6].split('=')[1].replace('\'', ''),
                              equ[7].split('=')[1].replace('\'', '')
                              ):
                raise Exception(479, 'Ошибка работы manticore')
        self.__sql_exec__(sql=sql, read=False)

    ###########################################
    # UPDATE
    ###########################################
    # + обновление всех col-ключей: ОДНОЙ sql-операцией
    def obj_update_col_all(self, data_pars):
        if not data_pars.rec_id: raise Exception('Unknow rec_id: data_pars = ' + str(data_pars))
        update_col_record_http(data_pars.col_table, data_pars.rec_id, data_pars.col_equ_flat())
        self.__sql_exec__(sql="UPDATE IGNORE " + data_pars.col_table + " SET " + ', '.join(
            data_pars.col_equ_flat()) + " WHERE rec_id=" + data_pars.rec_id + " LIMIT 1", read=False)
        return self.connection.get_connection().affected_rows() == 1

    ###########################################
    # SELECT
    ###########################################
    # + прочитать
    def select(self, table, select=['id'], where=[], only_first=False):
        if len(select) == 0: raise Exception("Отсутствует select")
        return self.__sql_exec__(
            sql= \
                "SELECT " + ', '.join(select) + " " + \
                "FROM " + table + " " + \
                (("WHERE " + ' AND '.join(where)) if len(where) > 0 else "") + \
                (" LIMIT 1" if only_first else ""),
            read=True)

    ###########################################
    # DELETE (только тесты)
    ###########################################
    def _delete_(self, table, where, only_first=True):
        self.__sql_exec__(sql="DELETE FROM " + table + " WHERE " + where + (" LIMIT 1" if only_first else ""),
                          read=False)

    ###########################################
    # EXEC
    ###########################################
    def __sql_exec__(self, sql, read):
        if DEBUG: print('\n' + sql)
        return db_sql(sql=sql, wait=not DEBUG, read=read, connection=self.connection)
