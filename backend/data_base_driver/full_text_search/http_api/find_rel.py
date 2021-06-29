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


def search_rel_with_key_http(rel_key, object_1_type, object_1_id, object_2_type, object_2_id, list_id):
    """
    Функция для поиска связей между двумя конкретными объектами
    @param rel_key: тип связи
    @param object_1_type: тип первого объекта
    @param object_1_id: идентификационный номер первого объекта
    @param object_2_type: тип второго объекта
    @param object_2_id: идентификационный номер второго объекта
    @param list_id: идентификационный в списке если есть
    @return: список идентификационных номеров объектов
    """
    if object_1_id != 0 and object_2_id != 0:
        data_1 = json.dumps({"index": 'rel', "query": {
            "query_string": get_sphinxql_two_object_1(object_1_type, object_1_id, object_2_type, object_2_id, rel_key,
                                                      list_id)}})
        data_2 = json.dumps({"index": 'rel', "query": {
            "query_string": get_sphinxql_two_object_2(object_1_type, object_1_id, object_2_type,
                                                      object_2_id, rel_key, list_id)}})
        response_1 = requests.post(FullTextSearch.SEARCH_URL, data=data_1)
        response_2 = requests.post(FullTextSearch.SEARCH_URL, data=data_2)
        result = set([item['_source']['rec_id_1'] for item in json.loads(response_1.text)['hits']['hits']])
        result = result.union(
            set([item['_source']['rec_id_2'] for item in json.loads(response_2.text)['hits']['hits']]))
    elif object_1_id == 0 and object_2_id != 0:
        data_1 = json.dumps({"index": 'rel', "query": {
            "query_string": get_sphinxql_without_first_object_1(object_1_type, object_2_type, object_2_id, rel_key,
                                                                list_id)}})
        data_2 = json.dumps({"index": 'rel', "query": {
            "query_string": get_sphinxql_without_first_object_2(object_1_type, object_2_type, object_2_id, rel_key,
                                                                list_id)}})
        response_1 = requests.post(FullTextSearch.SEARCH_URL, data=data_1)
        response_2 = requests.post(FullTextSearch.SEARCH_URL, data=data_2)
        result = set([item['_source']['rec_id_1'] for item in json.loads(response_1.text)['hits']['hits']])
        result = result.union(
            set([item['_source']['rec_id_2'] for item in json.loads(response_2.text)['hits']['hits']]))
    elif object_1_id != 0 and object_2_id == 0:
        data_1 = json.dumps({"index": 'rel', "query": {
            "query_string": get_sphinxql_without_second_object_1(object_1_type, object_1_id, object_2_type, rel_key,
                                                                 list_id)}})
        data_2 = json.dumps({"index": 'rel', "query": {
            "query_string": get_sphinxql_without_second_object_2(object_1_type, object_1_id, object_2_type, rel_key,
                                                                 list_id)}})
        response_1 = requests.post(FullTextSearch.SEARCH_URL, data=data_1)
        response_2 = requests.post(FullTextSearch.SEARCH_URL, data=data_2)
        result = set([item['_source']['rec_id_1'] for item in json.loads(response_1.text)['hits']['hits']])
        result = result.union(
            set([item['_source']['rec_id_2'] for item in json.loads(response_2.text)['hits']['hits']]))
    else:
        data_1 = json.dumps({"index": 'rel', "query": {
            "query_string": get_sphinxql_without_objects_1(object_1_type, object_2_type, rel_key, list_id)}})
        data_2 = json.dumps({"index": 'rel', "query": {
            "query_string": get_sphinxql_without_objects_2(object_1_type, object_2_type, rel_key, list_id)}})
        response_1 = requests.post(FullTextSearch.SEARCH_URL, data=data_1)
        response_2 = requests.post(FullTextSearch.SEARCH_URL, data=data_2)
        result = set([item['_source']['rec_id_1'] for item in json.loads(response_1.text)['hits']['hits']])
        result = result.union(
            set([item['_source']['rec_id_2'] for item in json.loads(response_2.text)['hits']['hits']]))
    return [int(item) for item in list(result)]
