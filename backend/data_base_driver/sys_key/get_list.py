from data_base_driver.constants.const_dat import DAT_SYS_LIST_DOP, DAT_SYS_LIST_TOP, DAT_OWNER
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.input_output.io_geo import get_geometry_folders


def get_groups_list():
    return [{'id': item['id'], 'value': item['title']} for item in DAT_OWNER.DUMP.get_groups_list()]


def get_list_by_top_id(id):
    """
    Функция для получения списка по его идентификационному номеру из таблицы sys_list_top
    @param id: идентификационный номер из таблицы sys_list_top
    @return: список словаре в формате [{'id':id1,'value':value1},{},...,{}]
    """
    if id == 48:
        return get_geometry_folders(1)
    if id == 53:
        return get_groups_list()
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
    """
    Функция для получения значения листа по его идентификатору
    @param id: идентификатор значения
    @return: значение листа в строковом формате
    """
    return DAT_SYS_LIST_DOP.DUMP.get_item_by_id(int(id))


def get_lists():
    """
    Функция для получения общего списка со всеми списками
    @return: объект в формате {id:{name,title,values:[{id,value},...,{}]},...,id_n:{}}
    """
    sql = 'SELECT ' + DAT_SYS_LIST_TOP.ID + ', '\
        + DAT_SYS_LIST_TOP.NAME + ', '\
        + DAT_SYS_LIST_TOP.TITLE + ' FROM '\
        + DAT_SYS_LIST_TOP.TABLE + ';'
    result = {}
    temp_list = db_sql(sql)
    for temp in temp_list:
        result[int(temp[0])] = {'name': temp[1], 'title': temp[2], 'values': get_list_by_top_id(int(temp[0]))}
    return result



