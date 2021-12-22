import json
import requests

from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_OBJ_ROW, DAT_OBJ_COL, DAT_REL
from data_base_driver.constants.const_fulltextsearch import FullTextSearch
from data_base_driver.input_output.valid_permission_manticore import get_enabled_records, check_relation_permission


def io_get_obj_row_manticore(group_id, object_type, keys, ids, ids_max_block, where_dop_row, time_interval):
    """
    Функция для получения информации о объекте из row индексов мантикоры в формате списка словарей
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта, формат int
    @param keys: список содержащий идентификаторы ключей
    @param ids: список содержащий идентификаторы объектов
    @param ids_max_block: максимальное количество записей в ответе
    @param where_dop_row: аргументы полнотекстового поиска (блок match запроса sphinx/manticore)
    @param time_interval: временной интервал записи в формате словаря с ключами second_start и second_end
    @return: список словарей в формате [{rec_id,sec,key_id,val},{},...,{}]
    """
    index = 'obj_' + FullTextSearch.TABLES[object_type] + '_row'
    must = []
    must.append({'range': {DAT_OBJ_ROW.SEC: {'gte': time_interval.get('second_start', 0),
                                             'lte': time_interval.get('second_end', 100000000000)}}})
    if len(ids) > 0:
        must.append({'in': {DAT_OBJ_ROW.ID: [int(rec_id) for rec_id in ids]}})
    if len(keys) > 0:
        must.append({'in': {DAT_OBJ_ROW.KEY_ID: [str(key) for key in keys]}})
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
    return get_enabled_records(object_type, [item['_source'] for item in json.loads(response.text)['hits']['hits']],
                               group_id, False)


def parse_where_dop(where_dop_row):
    """
    Вспомогательная функция для обработки where_dop_row при поиске по col таблицам
    @param where_dop_row: исходная строка запроса
    @return: None если в запросе нет @key_id, если есть, то key_id в числовом формате
    """
    if where_dop_row.find('@key_id') != -1:
        classifier_id = int(where_dop_row[where_dop_row.find('@key_id')+8:].split(' ')[0])
        return classifier_id
    else:
        return None


def io_get_obj_col_manticore(group_id, object_type, keys, ids, ids_max_block, where_dop):
    """
    Функция для получения информации о объекте из col индексов мантикоры в формате списка словарей
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта, формат int
    @param keys: список содержащий идентификаторы ключей
    @param ids: список содержащий идентификаторы объектов
    @param ids_max_block: максимальное количество записей в ответе
    @param where_dop: строка вставляемая в match часть запроса manticore
    @return: список словарей в формате [{rec_id,sec,key_id,val},{},...,{}]
    """
    col_keys = DAT_SYS_KEY.DUMP.get_rec(obj_id=object_type, col=True, only_first=False)
    if len(keys) == 0:
        result_keys = [{'id': item['id'], 'name': item['name']} for item in col_keys]
    else:
        result_keys = [{'id': item['id'], 'name': item['name']} for item in col_keys if item['id'] in keys]
    if len(result_keys) == 0:
        return []
    key_request = parse_where_dop(where_dop)
    index = 'obj_' + FullTextSearch.TABLES[object_type] + '_col'
    must = []
    if len(ids) > 0:
        must.append({'in': {DAT_OBJ_COL.ID: [int(rec_id) for rec_id in ids]}})
    data = json.dumps({
        'index': index,
        'query': {
            'query_string': where_dop if not key_request else '',
            'bool': {
                'must': must
            }
        },
        'limit': ids_max_block
    })
    response = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data).text)['hits']['hits']
    result = []
    for item in response:
        params = item['_source']
        for key in result_keys:
            if params.get(key['name']) != None and len(str(params.get(key['name']))) > 0:
                if key['name'] == 'location' or key['name'] == 'point':
                    value = json.dumps(params.get(key['name']))
                else:
                    value = str(params.get(key['name']))
                result.append({DAT_OBJ_ROW.ID: int(params['rec_id']),
                               DAT_OBJ_ROW.SEC: params['sec'],
                               DAT_OBJ_ROW.KEY_ID: key['id'],
                               DAT_OBJ_ROW.VAL: value})
    if key_request:
        result = [item for item in result if item[DAT_OBJ_ROW.ID] == key_request]
    return get_enabled_records(object_type, result, group_id, False)


def io_get_obj_manticore_dict(group_id, object_type, keys, ids, ids_max_block, where_dop_row, time_interval):
    """
    Функция для получения информации о объекте из manticore в формате списка словарей
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта, формат int
    @param keys: список содержащий идентификаторы ключей
    @param ids: список содержащий идентификаторы объектов
    @param ids_max_block: максимальное количество записей в ответе
    @param where_dop_row: аргументы полнотекстового поиска (блок match запроса sphinx/manticore)
    @param time_interval: временной интервал записи в формате словаря с ключами second_start и second_end
    @return: список словарей в формате [{rec_id,sec,key_id,val},{},...,{}]
    """
    row_records = io_get_obj_row_manticore(group_id, object_type, keys, ids, ids_max_block, where_dop_row,
                                           time_interval)
    if len(where_dop_row) > 0:
        ids = [item[DAT_OBJ_ROW.ID] for item in row_records]
    col_records = io_get_obj_col_manticore(group_id, object_type, keys, ids, ids_max_block, where_dop_row) # исправить where dop row
    result = row_records + col_records
    return result


def io_get_rel_manticore_dict(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique, rec_id=0):
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
    @return: список словарей в формате [{id,sec,key_id,obj_id_1,rec_id_1,obj_id_2,rec_id_2,val},{},...,{}]
    """
    if rec_id != 0:
        data = json.dumps({
            'index': DAT_REL.TABLE_SHORT,
            'query': {
                'equals': {
                    'id': rec_id
                }
            }
        })
        response = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data).text)['hits']['hits']
        result = [item['_source'] for item in response if check_relation_permission(item, group_id)]
        for relation in result:
            if len(relation['val']) == 0:
                relation['val'] = 0
            else:
                relation['val'] = int(relation['val'])
        return result
    must = []
    must.append({'range': {DAT_REL.SEC: {'gte': time_interval.get('second_start', 0),
                                         'lte': time_interval.get('second_end', 100000000000)}}})
    if len(keys) > 0:
        must.append({'in': {DAT_REL.KEY_ID: [str(key_id) for key_id in keys]}})
    if len(val) > 0:
        must.append({'in': {DAT_REL.VAL: [str(x) for x in val]}})
    request_1_obj_1, request_2_obj_2, request_1_rec_1, request_2_rec_2 = '', '', '', ''
    request_2_obj_1, request_1_obj_2, request_2_rec_1, request_1_rec_2 = '', '', '', ''
    if len(obj_rel_1) > 0:
        request_1_obj_1 = '@' + DAT_REL.OBJ_ID_1 + ' ' + str(obj_rel_1[0])
        request_2_obj_2 = '@' + DAT_REL.OBJ_ID_2 + ' ' + str(obj_rel_1[0])
    if len(obj_rel_1) > 1:
        request_1_rec_1 = '@' + DAT_REL.REC_ID_1 + ' ' + str(obj_rel_1[1])
        request_2_rec_2 = '@' + DAT_REL.REC_ID_2 + ' ' + str(obj_rel_1[1])
    if len(obj_rel_2) > 0:
        request_1_obj_2 = '@' + DAT_REL.OBJ_ID_2 + ' ' + str(obj_rel_2[0])
        request_2_obj_1 = '@' + DAT_REL.OBJ_ID_1 + ' ' + str(obj_rel_2[0])
    if len(obj_rel_2) > 1:
        request_1_rec_2 = '@' + DAT_REL.REC_ID_2 + ' ' + str(obj_rel_2[1])
        request_2_rec_1 = '@' + DAT_REL.REC_ID_1 + ' ' + str(obj_rel_2[1])
    data_1 = json.dumps({
        'index': DAT_REL.TABLE_SHORT,
        'query': {
            'query_string': ' '.join([request_1_obj_1, request_1_obj_2, request_1_rec_1, request_1_rec_2]),
            'bool': {
                'must': must
            }
        },
        "limit": 10000,
        "max_matches": 10000
    })
    data_2 = json.dumps({
        'index': DAT_REL.TABLE_SHORT,
        'query': {
            'query_string': ' '.join([request_2_obj_1, request_2_obj_2, request_2_rec_1, request_2_rec_2]),
            'bool': {
                'must': must
            }
        },
        "limit": 10000,
        "max_matches": 10000
    })
    response_1 = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data_1).text)['hits']['hits']
    response_2 = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data_2).text)['hits']['hits']
    full_result = [{'id': int(item['_id']),
                    'sec': item['_source']['sec'],
                    'key_id': item['_source']['key_id'],
                    'obj_id_1': item['_source']['obj_id_1'],
                    'rec_id_1': item['_source']['rec_id_1'],
                    'obj_id_2': item['_source']['obj_id_2'],
                    'rec_id_2': item['_source']['rec_id_2'],
                    'val': item['_source']['val'],
                    } for item in response_1 + response_2 if check_relation_permission(item, group_id)]
    for relation in full_result:
        if len(relation['val']) == 0:
            relation['val'] = 0
        else:
            relation['val'] = int(relation['val'])
    unique_result = []
    for item in full_result:
        if len([x for x in unique_result if item[DAT_REL.SEC] == x[DAT_REL.SEC] and
                                            item[DAT_REL.KEY_ID] == x[DAT_REL.KEY_ID] and
                                            item[DAT_REL.OBJ_ID_1] == x[DAT_REL.OBJ_ID_1] and
                                            item[DAT_REL.REC_ID_1] == x[DAT_REL.REC_ID_1] and
                                            item[DAT_REL.OBJ_ID_2] == x[DAT_REL.OBJ_ID_2] and
                                            item[DAT_REL.REC_ID_2] == x[DAT_REL.REC_ID_2] and
                                            item[DAT_REL.VAL] == x[DAT_REL.VAL]]) == 0:
            unique_result.append(item)
    if is_unique:
        return unique_result
    else:
        return full_result
