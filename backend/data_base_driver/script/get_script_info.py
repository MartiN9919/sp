from data_base_driver.connect import connect_mysql
from data_base_driver.constants.const_dat import DAT_SYS_SCRIPT, DAT_OWNER, DAT_SYS_SCRIPT_VARIABLE


def get_script_type(script_id):
    """
    Функция для получения типа скрипта
    @param script_id: идентификационный номер скрипта
    @return: тип скрипта с строковом формате
    """
    sql = 'SELECT ' + DAT_SYS_SCRIPT.TYPE + ' FROM ' \
          + DAT_SYS_SCRIPT.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_SCRIPT.ID + ' = ' \
          + str(script_id)
    return connect_mysql.db_sql(sql)[0][0]


def get_script_title(script_id):
    """
    Функция для получения названия скрипта
    @param script_id: идентификационный номер скрипта
    @return: название скрипта в строковом формате
    """
    sql = 'SELECT ' + DAT_SYS_SCRIPT.TITLE + ' FROM ' \
          + DAT_SYS_SCRIPT.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_SCRIPT.ID + ' = ' \
          + str(script_id)
    return connect_mysql.db_sql(sql)[0][0]


def get_script_variables(script_id):
    sql = 'SELECT ' + DAT_SYS_SCRIPT_VARIABLE.NAME + ', '\
        + DAT_SYS_SCRIPT_VARIABLE.TITLE + ', '\
        + DAT_SYS_SCRIPT_VARIABLE.HINT + ', '\
        + DAT_SYS_SCRIPT_VARIABLE.TYPE + ', '\
        + DAT_SYS_SCRIPT_VARIABLE.LIST_ID + ', '\
        + DAT_SYS_SCRIPT_VARIABLE.OBJ_ID + ' FROM '\
        + DAT_SYS_SCRIPT_VARIABLE.TABLE + ' WHERE '\
        + DAT_SYS_SCRIPT_VARIABLE.SCRIPT_ID + ' = ' + str(script_id)
    return connect_mysql.db_sql(sql)
