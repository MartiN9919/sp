from data_base_driver.constants.const_dat import DAT_SYS_LIST_DOP, DAT_SYS_LIST_TOP
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.input_output.io_geo import get_geometry_folders


def get_list_by_top_id(id):
    """
    Функция для получения списка по его идентификационному номеру из таблицы sys_list_top
    @param id: идентификационный номер из таблицы sys_list_top
    @return: список словаре в формате [{'id':id1,'value':value1},{},...,{}]
    """
    if id == 48:
        return get_geometry_folders(1)
    sql = 'SELECT ' + DAT_SYS_LIST_DOP.ID + ', ' \
          + DAT_SYS_LIST_DOP.VAL + ' FROM ' \
          + DAT_SYS_LIST_DOP.TABLE + ' WHERE ' \
          + DAT_SYS_LIST_DOP.KEY_ID + ' = ' + str(id)
    return [{'id': item[0], 'value': item[1]} for item in db_sql(sql)]


def get_list_by_name(name):
    """
    Функция для получения списка по его  имени из таблицы sys_list_top
    @param name: имя из таблицы sys_list_top
    @return: список словаре в формате [{'id':id1,'value':value1},{},...,{}]
    """
    sql = 'SELECT ' + DAT_SYS_LIST_TOP.ID + ' FROM ' \
          + DAT_SYS_LIST_TOP.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_LIST_TOP.NAME + ' = \'' + name + '\''
    top_list_id = db_sql(sql)[0][0]
    return get_list_by_top_id(top_list_id)


def get_item_list_value(id):
    sql = 'SELECT ' + DAT_SYS_LIST_DOP.VAL + ' FROM ' \
          + DAT_SYS_LIST_DOP.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_LIST_DOP.ID + ' = ' + str(id) + ';'
    value = db_sql(sql)[0][0]
    return value




