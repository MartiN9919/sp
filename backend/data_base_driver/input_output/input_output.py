from datetime import datetime

from data_base_driver.additional_functions import get_date_time_from_sec, date_time_to_sec, io_set_wrap, \
    io_get_object_wrap, io_get_rel_wrap
from data_base_driver.input_output.input_output_manticore import io_get_rel_manticore_dict, io_get_obj_manticore_dict
from data_base_driver.input_output.input_output_mysql import io_get_rel_mysql_tuple, io_get_obj_mysql_tuple
from data_base_driver.input_output.io_class import IO
from requests.exceptions import ConnectionError


@io_set_wrap
def io_set(group_id, obj, data):
    """
    функция для добавление объекта в базу данных
    @param group_id: группа привилегий пользователя
    @param obj: тип добавляемого объекта
    @param data: вносимая информация об объекте в формате вложенного списков [[key1,value1],[key2,value2],...,[keyN,valueN]],
    для того что бы добавить значение уже существующему элементу необходимо передать по ключу id его идентификационный номер
    @return: кортеж где 0 элемент это статус выполнения True/False, 1 элемент - rec_id добавленного/дополненного объекта
    """
    return IO(group_id=group_id).set(
        obj=obj,
        data=data,
    )


@io_get_object_wrap
def io_get_obj(group_id, object_type, keys, ids, ids_max_block, where_dop_row, time_interval):
    """
    Функция для получения информации о объекте из мантикоры в формате списка словарей
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта, формат int
    @param keys: список содержащий идентификаторы ключей
    @param ids: список содержащий идентификаторы объектов
    @param ids_max_block: максимальное количество записей в ответе
    @param where_dop_row: аргументы полнотекстового поиска (блок match запроса sphinx/manticore)
    @param time_interval: временной интервал записи в формате словаря с ключами second_start и second_end
    @return: список словарей в формате [{rec_id,sec,key_id,val},{},...,{}]
    """
    if not ids:
        ids = []
    if not keys:
        keys = []
    if not where_dop_row:
        where_dop_row = ''
    if not ids_max_block:
        ids_max_block = 1000
    if not time_interval:
        time_interval = {}
    try:
        return io_get_obj_manticore_dict(group_id, object_type, keys, ids, ids_max_block, where_dop_row, time_interval)
    except ConnectionError:
        where_dop_sql = []
        if len(where_dop_row) != 0:
            where_dop_sql.append('val=\"' + where_dop_row + '\"')
        if time_interval.get('second_start', None):
            where_dop_sql.append('dat>\"' + get_date_time_from_sec(time_interval.get('second_start', None)) + '\"')
        if time_interval.get('second_end', None):
            where_dop_sql.append('dat<\"' + get_date_time_from_sec(time_interval.get('second_start', None)) + '\"')
        result_tuple = io_get_obj_mysql_tuple(group_id, object_type, keys, ids, ids_max_block, where_dop_sql)
        result = [{'rec_id': item[0], 'key_id': item[1], 'val': item[2].encode(),
                   'sec': date_time_to_sec(datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S'))} for item in
                  result_tuple]  # в col 3 а не 4 параметра
        result.sort(key=lambda x: x['rec_id'])
        return result


def io_get_obj_tuple(group_id, object_type, keys, ids, ids_max_block, where_dop_row, time_interval):
    """
    Функция для получения информации о объекте из мантикоры в формате списка кортежей
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта, формат int
    @param keys: список содержащий идентификаторы ключей
    @param ids: список содержащий идентификаторы объектов
    @param ids_max_block: максимальное количество записей в ответе
    @param where_dop_row: аргументы полнотекстового поиска (блок match запроса sphinx/manticore)
    @param time_interval: временной интервал записи в формате словаря с ключами second_start и second_end
    @return: список словарей в формате [(rec_id,key_id,val,sec),(),...,()]
    """
    return [(item['rec_id'], int(item['key_id']), item['val'], item['sec'])
            for item in io_get_obj(group_id,
                                   object_type,
                                   keys,
                                   ids,
                                   ids_max_block,
                                   where_dop_row,
                                   time_interval)]


@io_get_rel_wrap
def io_get_rel(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique, rec_id=0):
    """
    Функция для получения информации о связях в формате списка словарей
    @param group_id: идентификатор группы пользователя
    @param keys: список идентификаторов типов связей
    @param obj_rel_1: информация о первом объекте для связи в формате списка [object_type(int), rec_id(int)],
    может быть пустым или содержать только тип объекта
    @param obj_rel_2: информация о втором объекте для связи в формате списка [object_type(int), rec_id(int)]
    может быть пустым или содержать только тип объекта
    @param val: список с возможными идентификаторами значений закрепленных списков
    @param time_interval: словарь хранящий промежуток времени в секундах: {second_start, second_end}
    @param is_unique: флаг проверки результирующего списка на уникальность входящих элементов
    @param rec_id: идентификатор связи, для проверки создания связи
    @return: список словарей в формате [{sec,key_id,obj_id_1,rec_id_1,obj_id_2,rec_id_2,val},{},...,{}]
    """
    if not keys:
        keys = []
    if not val:
        val = []
    if not time_interval:
        time_interval = {}
    try:
        return io_get_rel_manticore_dict(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique, rec_id)
    except ConnectionError:
        where_dop_sql = []
        if time_interval.get('second_start', None):
            where_dop_sql.append('dat>\"' + get_date_time_from_sec(time_interval.get('second_start', None)) + '\"')
        if time_interval.get('second_end', None):
            where_dop_sql.append('dat<\"' + get_date_time_from_sec(time_interval.get('second_start', None)) + '\"')
        result_tuple = io_get_rel_mysql_tuple(group_id, keys, obj_rel_1, obj_rel_2, where_dop_sql, is_unique)
        return [{'sec': date_time_to_sec(datetime.strptime(item[1], '%Y-%m-%d %H:%M:%S')),
                 'key_id': item[0],
                 'obj_id_1': item[2],
                 'rec_id_1': item[3],
                 'obj_id_2': item[4],
                 'rec_id_2': item[5],
                 'val': None} for item in result_tuple]


def io_get_rel_tuple(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique):
    """
    Функция для получения информации о связях в формате списка кортежей
    @param group_id: идентификатор группы пользователя
    @param keys: список идентификаторов типов связей
    @param obj_rel_1: информация о первом объекте для связи в формате списка [object_type(int), rec_id(int)],
    может быть пустым или содержать только тип объекта
    @param obj_rel_2: информация о втором объекте для связи в формате списка [object_type(int), rec_id(int)]
    может быть пустым или содержать только тип объекта
    @param val: список с возможными идентификаторами значений закрепленных списков
    @param time_interval: словарь хранящий промежуток времени в секундах: {second_start, second_end}
    @param is_unique: флаг проверки результирующего списка на уникальность входящих элементов
    @return: список словарей в формате [(key_id,sec,obj_id_1,rec_id_1,obj_id_2,rec_id_2,val),(),...,()]
    """
    temp_result = io_get_rel(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique)
    return [(int(item['key_id']),
             item['sec'],
             int(item['obj_id_1']),
             int(item['rec_id_1']),
             int(item['obj_id_2']),
             int(item['rec_id_2']),
             item['val'],
             item['id']
             ) for item in temp_result]


