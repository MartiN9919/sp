import copy

from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_KEY, DAT_SYS_ID


def objects_list():
    """
    Функция для получения списка объектов
    @return: список объектов
    """
    temp_list = [item for item in sorted(copy.deepcopy(DAT_SYS_OBJ.DUMP.get_all()), key=lambda x: x[DAT_SYS_OBJ.PRIORITY])
            if item.get('id') != 1]
    keys = DAT_SYS_KEY.DUMP.get_rec(obj_id=1, only_first=False)
    for temp in temp_list:
        temp_rels = []
        temp_keys_1 = list(set([key['rel_obj_2_id'] for key in keys if key['rel_obj_1_id'] == temp['id']]))
        temp_keys_2 = list(set([key['rel_obj_1_id'] for key in keys if key['rel_obj_2_id'] == temp['id']]))
        temp_rels.extend(temp_keys_1)
        temp_rels.extend(temp_keys_2)
        temp['rels'] = temp_rels
    return temp_list


def get_object_id(name):
    """
    Функция для получения идентификационного номера объекта по его имени
    @param name: имя объекта
    @return: идентификационного номера объекта
    """
    return DAT_SYS_OBJ.DUMP.get_rec(name=name)[DAT_SYS_OBJ.ID]


def get_relations():
    return [item for item in DAT_SYS_KEY.DUMP.get_rec(obj_id=1, only_first=False) if
            item['rel_obj_1_id'] and item['rel_obj_2_id']]


def get_object_new_rec_id(object_id):
    """
    Функция для получения идентификатора следующего объекта заданного типа
    @param object_id: идентификатор типа объекта
    @return:
    """
    sql = 'SELECT ' + DAT_SYS_ID.ID + ' FROM '\
                    + DAT_SYS_ID.TABLE + ' WHERE ' \
                    + DAT_SYS_ID.OBJ_ID + ' = ' + str(object_id) + ';'
    return db_sql(sql)[0][0] + 1
