from data_base_driver.connect import connect_mysql
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_TRIGGER, DAT_SYS_TRIGGER_VARIABLE


def get_trigger_by_id(trigger_id):
    sql = 'SELECT ' + DAT_SYS_TRIGGER.OBJECT_ID + ', '\
                    + DAT_SYS_TRIGGER.TITLE + ', '\
                    + DAT_SYS_TRIGGER.HINT + ' FROM '\
                    + DAT_SYS_TRIGGER.TABLE + ' WHERE '\
                    + DAT_SYS_TRIGGER.ID + ' = ' + str(trigger_id)
    temp_result = db_sql(sql)
    if len(temp_result) > 0:
        result = temp_result[0]
        return {'id': int(trigger_id), 'object_id': int(result[0]), 'name': result[1]}
    else:
        return {'id': 0, 'object_id': 0, 'name': 'unknown'}


def get_trigger_variables(script_id):
    sql = 'SELECT ' + DAT_SYS_TRIGGER_VARIABLE.NAME + ', '\
        + DAT_SYS_TRIGGER_VARIABLE.TITLE + ', '\
        + DAT_SYS_TRIGGER_VARIABLE.HINT + ', '\
        + DAT_SYS_TRIGGER_VARIABLE.TYPE + ', '\
        + DAT_SYS_TRIGGER_VARIABLE.LIST_ID + ', '\
        + DAT_SYS_TRIGGER_VARIABLE.OBJ_ID + ', '\
        + DAT_SYS_TRIGGER_VARIABLE.NECESSARY + ' FROM '\
        + DAT_SYS_TRIGGER_VARIABLE.TABLE + ' WHERE '\
        + DAT_SYS_TRIGGER_VARIABLE.SCRIPT_ID + ' = ' + str(script_id)
    return connect_mysql.db_sql(sql)
