import datetime
import json
import requests
from data_base_driver.constants.fulltextsearch import FullTextSearch


def get_sphinxql_two_object_1(object_1_type, object_1_id, object_2_type, object_2_id, key_id=0, list_id=0):
    tmp = '@obj_id_1 ' + str(object_1_type) + ' @rec_id_1 ' + str(object_1_id) + ' @obj_id_2 ' + str(
        object_2_type) + ' @rec_id_2 ' + str(object_2_id)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    return tmp


def get_sphinxql_two_object_2(object_1_type, object_1_id, object_2_type, object_2_id, key_id=0, list_id=0):
    tmp = '@obj_id_1 ' + str(object_2_type) + ' @rec_id_1 ' + str(object_2_id) + ' @obj_id_2 ' + str(
        object_1_type) + ' @rec_id_2 ' + str(object_1_id)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    return tmp


def get_sphinxql_without_first_object_1(object_1_type, object_2_type, object_2_id, key_id=0, list_id=0):
    tmp = '@obj_id_1 ' + str(object_1_type) + ' @obj_id_2 ' + str(object_2_type) + ' @rec_id_2 ' + str(object_2_id)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    return tmp


def get_sphinxql_without_first_object_2(object_1_type, object_2_type, object_2_id, key_id=0, list_id=0):
    tmp = '@obj_id_2 ' + str(object_1_type) + ' @obj_id_1 ' + str(object_2_type) + ' @rec_id_1 ' + str(object_2_id)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    return tmp


def get_sphinxql_without_second_object_1(object_1_type, object_1_id, object_2_type, key_id=0, list_id=0):
    tmp = '@obj_id_1 ' + str(object_1_type) + ' @rec_id_1 ' + str(object_1_id) + ' @obj_id_2 ' + str(object_2_type)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    return tmp


def get_sphinxql_without_second_object_2(object_1_type, object_1_id, object_2_type, key_id=0, list_id=0):
    tmp = '@obj_id_2 ' + str(object_1_type) + ' @rec_id_2 ' + str(object_1_id) + ' @obj_id_1 ' + str(object_2_type)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    return tmp


def get_sphinxql_without_objects_1(object_1_type, object_2_type, key_id=0, list_id=0):
    tmp = '@obj_id_1 ' + str(object_1_type) + ' @obj_id_2 ' + str(object_2_type)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    return tmp


def get_sphinxql_without_objects_2(object_1_type, object_2_type, key_id=0, list_id=0):
    tmp = '@obj_id_1 ' + str(object_2_type) + ' @obj_id_2 ' + str(object_1_type)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    return tmp


def get_validate_request(key_id, rec_id_1, rec_id_2):
    """
    Функция для отправки запроса проверки актуальности
    @param key_id: ключ классификатора проверяемой связи
    @param rec_id_1: идентификатор первого объекта
    @param rec_id_2: идентификатор второго объекта
    @return: упакованный для отправки json
    """
    data = {
        "index": 'rel',
        "query":
            {
                "query_string": '@key_id ' + key_id + ' @rec_id_1 ' + rec_id_1 + ' @rec_id_2 ' + rec_id_2
            }
    }
    return json.dumps(data)


def get_seconds_from_request_data_time(date_time_start, date_time_end):
    if not date_time_start:
        date_time_1_str = '0001-01-01 00:00:00'
    else:
        date_time_1_str = date_time_start + ':00'
    if not date_time_end:
        date_time_2_str = datetime.datetime.now().isoformat(sep=' ')[:19]
    else:
        date_time_2_str = date_time_end + ':00'
    date_time_1 = datetime.datetime.strptime(date_time_1_str, "%Y-%m-%d %H:%M:%S")
    days = date_time_1.date().toordinal() + 365
    seconds_1 = date_time_1.time().second + date_time_1.time().minute * 60 + date_time_1.time().hour * 3600 \
                + days * 86400
    date_time_2 = datetime.datetime.strptime(date_time_2_str, "%Y-%m-%d %H:%M:%S")
    days = date_time_2.date().toordinal() + 365
    seconds_2 = date_time_2.time().second + date_time_2.time().minute * 60 + date_time_2.time().hour * 3600 \
                + days * 86400
    return seconds_1, seconds_2


def validate_rel_actual(rel, date_time_start, date_time_end):
    """
    Функция для проверки актуальности отдельной связи
    @param rel: словарь содержащий информацию о проверяемой связи
    @param date_time_start: дата и время начала выборки
    @param date_time_end: дата и время конца выборки
    @return: False если связь не актуальна, True если актуальна
    """
    seconds_1, seconds_2 = get_seconds_from_request_data_time(date_time_start, date_time_end)
    data = get_validate_request(rel['key_id'], rel['rec_id_1'], rel['rec_id_2'])
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    for temp in json.loads(response.text)['hits']['hits']:
        if temp['_source']['sec'] < seconds_1 or temp['_source']['sec'] > seconds_2 or \
                temp['_source']['sec'] == rel['sec']:
            continue
        if temp['_source']['sec'] > rel['sec']:
            return False
    return True


def get_rel_request(query_string, date_time_start, date_time_end):
    """
    Функция для формирования запроса для поиска связи
    @param query_string: строка запроса manticore/sphinx
    @param date_time_start: начальная дата и время периода поиска
    @param date_time_end: конечная дата и время периода поиска
    @return: json запрос для manticore API
    """
    seconds_1, seconds_2 = get_seconds_from_request_data_time(date_time_start, date_time_end)
    data = {
        "index": 'rel',
        "query":
            {
                "query_string": query_string,
                "range":
                    {
                        "sec":
                            {
                                "gte": seconds_1,
                                "lte": seconds_2
                            }
                    }
            },
        "limit": 100
    }
    return json.dumps(data)


def search_rel_with_key_http(rel_key, object_1_type, object_1_id, object_2_type, object_2_id, list_id, date_time_start,
                               date_time_end, mode=1):
    """
    Функция для поиска связей между двумя конкретными объектами
    @param rel_key: тип связи
    @param object_1_type: тип первого объекта
    @param object_1_id: идентификационный номер первого объекта
    @param object_2_type: тип второго объекта
    @param object_2_id: идентификационный номер второго объекта
    @param list_id: идентификационный в списке если есть
    @param date_time_start: дата и время начала поиска связи
    @param date_time_end: дата и время конца поиска связи
    @return: список идентификационных номеров объектов
    """
    if object_1_id != 0 and object_2_id != 0:
        data_1 = get_rel_request(get_sphinxql_two_object_1(object_1_type, object_1_id, object_2_type, object_2_id,
                                                           rel_key, list_id), date_time_start, date_time_end)
        data_2 = get_rel_request(get_sphinxql_two_object_2(object_1_type, object_1_id, object_2_type, object_2_id,
                                                           rel_key, list_id), date_time_start, date_time_end)
    elif object_1_id == 0 and object_2_id != 0:
        data_1 = get_rel_request(get_sphinxql_without_first_object_1(object_1_type, object_2_type, object_2_id, rel_key,
                                                                list_id), date_time_start, date_time_end)
        data_2 = get_rel_request(get_sphinxql_without_first_object_2(object_1_type, object_2_type, object_2_id, rel_key,
                                                                list_id), date_time_start, date_time_end)
    elif object_1_id != 0 and object_2_id == 0:
        data_1 = get_rel_request(get_sphinxql_without_second_object_1(object_1_type, object_1_id, object_2_type,
                                                                      rel_key, list_id), date_time_start, date_time_end)
        data_2 = get_rel_request(get_sphinxql_without_second_object_2(object_1_type, object_1_id, object_2_type,
                                                                      rel_key, list_id), date_time_start, date_time_end)
    else:
        data_1 = get_rel_request(get_sphinxql_without_objects_1(object_1_type, object_2_type, rel_key, list_id),
                                 date_time_start, date_time_end)
        data_2 = get_rel_request(get_sphinxql_without_objects_2(object_1_type, object_2_type, rel_key, list_id),
                                 date_time_start, date_time_end)
    response_1 = requests.post(FullTextSearch.SEARCH_URL, data=data_1)
    response_2 = requests.post(FullTextSearch.SEARCH_URL, data=data_2)
    result = set([(item['_source']['rec_id_1'], item['_source']['key_id']) for item in json.loads(response_1.text)['hits']['hits']
                  if validate_rel_actual(item['_source'], date_time_start, date_time_end)])
    result = result.union(
        set([(item['_source']['rec_id_2'], item['_source']['key_id']) for item in json.loads(response_2.text)['hits']['hits']
             if validate_rel_actual(item['_source'], date_time_start, date_time_end)]))
    if mode == 1:
        return [int(item[0]) for item in list(result)]
    else:
        return [{'rec_id': item[0], 'key_id': item[1]} for item in list(result)]


def get_relations_with_object_http(object_type, object_id):
    """
    функция для получения всех связей для одного объекта
    @param object_type: тип объекта
    @param object_id: идентификационный номер объекта
    @return: список кортежей в формате [(rel_id,date,obj_id1,rec_id1,obj_id2,rec_id2),(),...,()]
    """
    data_1 = json.dumps({
        "index": 'rel',
        "query": {
            "query_string": '@obj_id_1 ' + str(object_type) + ' @rec_id_1 ' + str(object_id)
        }, "limit": 500
    })
    data_2 = json.dumps({
        "index": 'rel',
        "query": {
            "query_string": '@obj_id_2 ' + str(object_type) + ' @rec_id_2 ' + str(object_id)
        }, "limit": 500
    })
    response_1 = requests.post(FullTextSearch.SEARCH_URL, data=data_1)
    response_2 = requests.post(FullTextSearch.SEARCH_URL, data=data_2)
    resule_1 = [(int(item['_source']['key_id']), item['_source']['sec'], int(item['_source']['obj_id_1']),
                 int(item['_source']['rec_id_1']), int(item['_source']['obj_id_2']), int(item['_source']['rec_id_2']))
                for item in json.loads(response_1.text)['hits']['hits']]
    resule_2 = [(int(item['_source']['key_id']), item['_source']['sec'], int(item['_source']['obj_id_1']),
                 int(item['_source']['rec_id_1']), int(item['_source']['obj_id_2']), int(item['_source']['rec_id_2']))
                for item in json.loads(response_2.text)['hits']['hits']]
    result = set(resule_1)
    result = result.union(set(resule_2))
    return list(result)




