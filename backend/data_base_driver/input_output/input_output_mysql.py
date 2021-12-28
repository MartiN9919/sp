from data_base_driver.additional_functions import get_date_time_from_sec, date_time_to_sec
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_REL
from data_base_driver.input_output.io_class import IO
from data_base_driver.input_output.valid_permission_manticore import check_relation_permission, \
    check_relation_permission_mysql


def io_get_obj_mysql_generator(group_id, obj, keys=[], ids=[], ids_max_block=None, where_dop_row=[]):
    """
    Функция аналогична функции io_get_obj_mysql_tuple, за исключением типа возвращаемого значения, в данном случае возвращается
    генератор, а не кортеж
    """
    yield from IO(group_id=group_id).get_obj(
        obj=obj,
        keys=keys,
        ids=ids,
        ids_max_block=ids_max_block,
        where_dop_row=where_dop_row,
    )


def io_get_obj_mysql_tuple(group_id, obj, keys=[], ids=[], ids_max_block=None, where_dop_row=[]):
    """
    Функция для получения информации об объекте/объектах
    @param group_id: группа привилегий пользователя
    @param obj: тип искомого объекта/объектов
    @param keys: искомые типы значений для искомых объектов, если необходима вся информация передать пустой список
    @param ids: номер либо номера искомых объектов, если необходимы все, передать пустой список
    @param ids_max_block: максимальное количество найденных объектов
    @param where_dop_row: дополнительные sql фильтры если необходимы, передавать как список строк
    @return: список кортежей в формате ((rec_id1,key_id1,val1,date1),(),...,())
    """
    return tuple(IO(group_id=group_id).get_obj(
        obj=obj,
        keys=keys,
        ids=ids,
        ids_max_block=ids_max_block,
        where_dop_row=where_dop_row,
    ))


def io_get_rel_mysql(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique, rec_id):
    date_start = get_date_time_from_sec(time_interval.get('second_start', 0))
    date_end = get_date_time_from_sec(time_interval.get('second_end', 100000000000))
    where_list = []
    where_list.append(DAT_REL.DAT + ' > \'' + date_start + '\' AND ' + DAT_REL.DAT + ' < \'' + date_end + '\'')
    if len(keys) > 0:
        where_list.append('key_id in ' + str(tuple(keys))) if len(keys) > 1 else where_list.append('key_id in (' + str(keys[0]) + ')')
    if len(val) > 0:
        where_list.append('val in ' + str(tuple(val))) if len(val) > 1 else where_list.append('val in (' + str(val[0]) + ')')
    object_1_where, object_2_where = [], []
    if len(obj_rel_1) > 0:
        object_1_where.append(DAT_REL.OBJ_ID_1 + '=' + str(obj_rel_1[0]))
        object_2_where.append(DAT_REL.OBJ_ID_2 + '=' + str(obj_rel_1[0]))
    if len(obj_rel_1) > 1:
        object_1_where.append(DAT_REL.REC_ID_1 + '=' + str(obj_rel_1[1]))
        object_2_where.append(DAT_REL.REC_ID_2 + '=' + str(obj_rel_1[1]))
    if len(obj_rel_2) > 0:
        object_1_where.append(DAT_REL.OBJ_ID_2 + '=' + str(obj_rel_2[0]))
        object_2_where.append(DAT_REL.OBJ_ID_1 + '=' + str(obj_rel_2[0]))
    if len(obj_rel_2) > 1:
        object_1_where.append(DAT_REL.REC_ID_2 + '=' + str(obj_rel_2[1]))
        object_2_where.append(DAT_REL.REC_ID_1 + '=' + str(obj_rel_2[1]))
    request_1 = 'SELECT * FROM ' + DAT_REL.TABLE_SHORT + ' WHERE ' + ' AND '.join(where_list + object_1_where)
    request_2 = 'SELECT * FROM ' + DAT_REL.TABLE_SHORT + ' WHERE ' + ' AND '.join(where_list + object_2_where)
    response = db_sql(request_1) + db_sql(request_2)
    if is_unique:
        response = tuple(set(response))
    return [{
        'id': item[0],
        'sec': date_time_to_sec(item[2]),
        'key_id': item[1],
        'obj_id_1': item[3],
        'rec_id_1': item[4],
        'obj_id_2': item[5],
        'rec_id_2': item[6],
        'val': int(item[7]) if item[7] and len(item[7]) > 0 else 0,
        'document_id': int(item[8]) if item[8] and len(item[7]) > 0 else 0
    } for item in response if check_relation_permission_mysql(item, group_id)]


def io_get_rel_mysql_generator(group_id, keys=[], obj_rel_1=None, obj_rel_2=None, where_dop=[]):
    """
    Функция аналогична функции io_get_rel_mysql_tuple, за исключением типа возвращаемого значения, в данном случае возвращается
    генератор, а не кортеж
    """
    yield from IO(group_id=group_id).get_rel(
        keys=keys,
        obj_rel_1=obj_rel_1,
        obj_rel_2=obj_rel_2,
        where_dop=where_dop,
    )


def io_get_rel_mysql_tuple(group_id, keys=[], obj_rel_1=None, obj_rel_2=None, where_dop=[], is_unique=False):
    """
    Функция для получения списка связей
    @param group_id: группа привилегий пользователя
    @param keys: типы связей, передавать в виде списка строк либо номеров
    @param obj_rel_1: тип и id первого связываемого объекта в формате [type,id]
    @param obj_rel_2: тип и id второго связываемого объекта в формате [type,id]
    @param where_dop: дополнительные параметры sql фильтры, передавать в виде списка строк
    @param is_unique: уникальна ли данная связь
    @return: список кортежей в формате ((rel_id,date,obj_id1,rec_id1,obj_id2,rec_id2),(),...,())
    """
    ret = tuple(IO(group_id=group_id).get_rel(
        keys=keys,
        obj_rel_1=obj_rel_1,
        obj_rel_2=obj_rel_2,
        where_dop=where_dop,
    ))
    if is_unique: ret = tuple(set(ret))
    return ret