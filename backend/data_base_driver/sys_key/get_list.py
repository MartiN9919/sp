from data_base_driver.constants.const_dat import DAT_SYS_LIST_DOP
from data_base_driver.connect.connect_mysql import db_sql


def get_list_by_top_id(id):
    """
    Функция для получения списка по его идентификационному номеру из таблицы sys_list_top
    @param id: идентификационный номер из таблицы sys_list_top
    @return: список словаре в формате [{'id':id1,'value':value1},{},...,{}]
    """
    sql = 'SELECT ' + DAT_SYS_LIST_DOP.ID + ', ' \
          + DAT_SYS_LIST_DOP.VAL + ' FROM ' \
          + DAT_SYS_LIST_DOP.TABLE + ' WHERE ' \
          + DAT_SYS_LIST_DOP.KEY_ID + ' = ' + str(id)
    return [{'id': item[0], 'value': item[1]} for item in db_sql(sql)]

