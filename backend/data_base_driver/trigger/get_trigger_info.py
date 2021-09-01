from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_TRIGGER


def get_trigger_by_id(id):
    sql = 'SELECT ' + DAT_SYS_TRIGGER.OBJECT_ID + ', '\
                    + DAT_SYS_TRIGGER.TITLE + ', '\
                    + DAT_SYS_TRIGGER.HINT + ' FROM '\
                    + DAT_SYS_TRIGGER.TABLE + ' WHERE '\
                    + DAT_SYS_TRIGGER.ID + ' = ' + str(id)
    temp_result = db_sql(sql)
    if len(temp_result) > 0:
        result = temp_result[0]
        return {'id': int(id), 'object_id': int(result[0]), 'name': result[1]}
    else:
        return {'id': 0, 'object_id': 0, 'name': 'unknow'}