import datetime
from data_base_driver.connect.connect_manticore import db_shinxql
from data_base_driver.connect.connect_mysql import db_sql, db_connect
from data_base_driver.constants.const_dat import DAT_SYS_ID, DAT_OBJ_ROW
from data_base_driver.full_text_search.http_api.add_object_http import add_record_http, add_relation_http

DEBUG = False


###########################################
# MY_SQL: БИБЛИОТЕКА ФУНКЦИЙ ДОСТУПА К SQL
###########################################
class IO_LIB_SQL():
    def __init__(self):
        self.connection = db_connect()


    def __del__(self):
        self.connection.free_connection()
    ###########################################
    # REC_ID
    ###########################################
    # + получить rec_id для нового элемента obj
    def obj_rec_id_new(self, obj_id):
        # в одно обращение к БД без чтения с блокировкой
        self.__sql_exec__(
            sql="UPDATE " + DAT_SYS_ID.TABLE + " SET id = LAST_INSERT_ID(id + 1) WHERE " + DAT_SYS_ID.OBJ_ID + "=" + str(
                obj_id), read=False)
        ret = self.connection.get_connection().insert_id()
        if ret == 0: raise Exception('Unknow get new id for obj.' + str(obj_id))
        return ret

    ###########################################
    # INSERT
    ###########################################
    # + запись всех col-ключей: ОДНОЙ sql-операцией => ОДНА запись
    def obj_insert_col_one(self, data_pars):
        if not data_pars.rec_id: raise Exception('Unknow rec_id: data_pars = ' + str(data_pars))
        sql = "INSERT IGNORE INTO " + data_pars.col_table + " " + \
            "SET " + ', '.join(['id=' + data_pars.rec_id] + data_pars.col_equ_flat())
        self.__sql_exec__(sql, read=False)

    # + запись ОДНОГО row-ключа ОДНОЙ sql-операцией => ОДНА запись
    obj_insert_row_one = lambda self, data_pars, ind: self.insert_one_rec( #возможны проблемы из-за замены стандартной функции
        table=data_pars.row_table,
        equ=['id=' + data_pars.rec_id, ] + data_pars.equ_item(item_dic=data_pars.row_dic[ind], is_null=False)
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
            add_record_http(data_pars.row_table, data_pars.rec_id, date_time_str, item[DAT_OBJ_ROW.KEY_ID],
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
            add_record_http(table,
                            int(equ[0].split('=')[1]),
                            equ[3].split('=')[1].replace('\'', ''),
                            equ[1].split('=')[1],
                            equ[2].split('=')[1].replace('\'', '')
                            )
        else:
            add_relation_http(equ[5].split('=')[1].replace('\'', ''),
                              int(equ[0].split('=')[1]),
                              int(equ[1].split('=')[1]),
                              int(equ[2].split('=')[1]),
                              int(equ[3].split('=')[1]),
                              int(equ[4].split('=')[1]),
                              ''
                              )
        self.__sql_exec__(sql=sql, read=False)

    ###########################################
    # UPDATE
    ###########################################
    # + обновление всех col-ключей: ОДНОЙ sql-операцией
    def obj_update_col_all(self, data_pars):
        if not data_pars.rec_id: raise Exception('Unknow rec_id: data_pars = ' + str(data_pars))
        self.__sql_exec__(sql="UPDATE IGNORE " + data_pars.col_table + " SET " + ', '.join(
            data_pars.col_equ_flat()) + " WHERE id=" + data_pars.rec_id + " LIMIT 1", read=False)
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


    def __shinxql_exec__(self, sql, read):
        if DEBUG: print('\n' + sql)
        return db_shinxql(sql=sql, wait=not DEBUG, read=read)
