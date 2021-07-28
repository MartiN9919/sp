import json

import requests

from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.input_output.io_class import IO


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


def io_get_obj_generator(group_id, obj, keys=[], ids=[], ids_max_block=None, where_dop_row=[]):
    """
    Функция аналогична функции io_get_obj, за исключением типа возвращаемого значения, в данном случае возвращается
    генератор, а не кортеж
    """
    yield from IO(group_id=group_id).get_obj(
        obj=obj,
        keys=keys,
        ids=ids,
        ids_max_block=ids_max_block,
        where_dop_row=where_dop_row,
    )


def io_get_obj(group_id, obj, keys=[], ids=[], ids_max_block=None, where_dop_row=[]):
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


def io_get_obj_manticore_dict(group_id, object_type, keys, ids, ids_max_block, where_dop_row):
    """
    Функция для получения информации о объекте из мантикоры в формате списка словарей
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта, формат int
    @param keys: список содержащий идентификаторы ключей
    @param ids: список содержащий идентификаторы объектов
    @param ids_max_block: максимальное количество записей в ответе
    @param where_dop_row: аргументы полнотекствого поиска (блок match запроса sphinx/manticore)
    @return: список словарей в формате [{rec_id,sec,key_id,val},{},...,{}]
    """
    if not ids:
        ids = []
    if not keys:
        keys = []
    if not where_dop_row:
        where_dop_row = ''
    if not ids_max_block:
        ids_max_block = 100
    index = 'obj_' + FullTextSearch.TABLES[object_type] + '_row'
    must = []
    if len(ids) > 0:
        must.append({'in': {'rec_id': [int(rec_id) for rec_id in ids]}})
    if len(keys) > 0:
        must.append({'in': {'key_id': [str(key) for key in keys]}})
    data = json.dumps({
        'index': index,
        'query': {
            'query_string': where_dop_row,
            'bool': {
                'must': must
            }
        },
        "limit": ids_max_block
    })
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    return [item['_source'] for item in json.loads(response.text)['hits']['hits']]


def io_get_obj_manticore_tuple(group_id, object_type, keys, ids, ids_max_block, where_dop_row):
    """
    Функция для получения информации о объекте из мантикоры в формате списка кортежей
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта, формат int
    @param keys: список содержащий идентификаторы ключей
    @param ids: список содержащий идентификаторы объектов
    @param ids_max_block: максимальное количество записей в ответе
    @param where_dop_row: аргументы полнотекствого поиска (блок match запроса sphinx/manticore)
    @return: список словарей в формате [(rec_id,key_id,val,sec),(),...,()]
    """
    return [(item['rec_id'], int(item['key_id']), item['val'], item['sec'])
            for item in io_get_obj_manticore_dict(group_id,
                                                  object_type,
                                                  keys,
                                                  ids,
                                                  ids_max_block,
                                                  where_dop_row)]


def io_get_rel_generator(group_id, keys=[], obj_rel_1=None, obj_rel_2=None, where_dop=[]):
    """
    Функция аналогична функции io_get_rel, за исключением типа возвращаемого значения, в данном случае возвращается генератор,
     а не кортеж
    """
    yield from IO(group_id=group_id).get_rel(
        keys=keys,
        obj_rel_1=obj_rel_1,
        obj_rel_2=obj_rel_2,
        where_dop=where_dop,
    )


def io_get_rel(group_id, keys=[], obj_rel_1=None, obj_rel_2=None, where_dop=[], is_unique=False):
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


def io_get_rel_manticore_dict(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique):
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
    @return: список словарей в формате [{sec,key_id,obj_id_1,rec_id_1,obj_id_2,rec_id_2,val},{},...,{}]
    """
    if not keys:
        keys = []
    if not val:
        val = []
    if not time_interval:
        time_interval = {}
    must = []
    must.append({'range': {'sec': {'gte': time_interval.get('second_start', 0),
                                   'lte': time_interval.get('second_end', 100000000000)}}})
    if len(keys) > 0:
        must.append({'in': {'key_id': [str(key_id) for key_id in keys]}})
    if len(val) > 0:
        must.append({'in': {'val': [str(x) for x in val]}})
    request_1_obj_1, request_2_obj_2,  request_1_rec_1, request_2_rec_2 = '', '', '', ''
    request_2_obj_1, request_1_obj_2,  request_2_rec_1, request_1_rec_2 = '', '', '', ''
    if len(obj_rel_1) > 0:
        request_1_obj_1 = '@obj_id_1 ' + str(obj_rel_1[0])
        request_2_obj_2 = '@obj_id_2 ' + str(obj_rel_1[0])
    if len(obj_rel_1) > 1:
        request_1_rec_1 = '@rec_id_1 ' + str(obj_rel_1[1])
        request_2_rec_2 = '@rec_id_2 ' + str(obj_rel_1[1])
    if len(obj_rel_2) > 0:
        request_1_obj_2 = '@obj_id_2 ' + str(obj_rel_2[0])
        request_2_obj_1 = '@obj_id_1 ' + str(obj_rel_2[0])
    if len(obj_rel_2) > 1:
        request_1_rec_2 = '@rec_id_2 ' + str(obj_rel_2[1])
        request_2_rec_1 = '@rec_id_1 ' + str(obj_rel_2[1])
    data_1 = json.dumps({
        'index': 'rel',
        'query': {
            'query_string': ' '.join([request_1_obj_1, request_1_obj_2, request_1_rec_1, request_1_rec_2]),
            'bool': {
                'must': must
            }
        }
        })
    data_2 = json.dumps({
        'index': 'rel',
        'query': {
            'query_string': ' '.join([request_2_obj_1, request_2_obj_2, request_2_rec_1, request_2_rec_2]),
            'bool': {
                'must': must
            }
        }
    })
    response_1 = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data_1).text)['hits']['hits']
    response_2 = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data_2).text)['hits']['hits']
    full_result = [item['_source'] for item in response_1 + response_2]
    unique_result = []
    for item in full_result:
        if len([x for x in unique_result if item['sec'] == x['sec'] and
                                      item['key_id'] == x['key_id'] and
                                      item['obj_id_1'] == x['obj_id_1'] and
                                      item['rec_id_1'] == x['rec_id_1'] and
                                      item['obj_id_2'] == x['obj_id_2'] and
                                      item['rec_id_2'] == x['rec_id_2'] and
                                      item['val'] == x['val']]) == 0:
            unique_result.append(item)
    if is_unique:
        return unique_result
    else:
        return full_result


def io_get_rel_manticore_tuple(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique):
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
    temp_result = io_get_rel_manticore_dict(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique)
    return [(int(item['key_id']),
             item['sec'],
             int(item['obj_id_1']),
             int(item['rec_id_1']),
             int(item['obj_id_2']),
             int(item['rec_id_2']),
             item['val']
             ) for item in temp_result]


###########################################
# ЧТЕНИЕ GEOMETRY_TREE
###########################################
# ret = [ {id: , name: , icon: }, ... ]
def io_get_geometry_tree(
        group_id,
        parent_id,
        write=True,
):
    return tuple(IO(group_id=group_id).get_geometry_tree(
        parent_id=parent_id,
        write=write,
    ))


