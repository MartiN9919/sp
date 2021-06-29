import json

import requests

from data_base_driver.constants.fulltextsearch import FullTextSearch


def find_key_value_http(object_id, key_id, value):
    """
    Функция для нахождения в базе данных по отдельным полям
    @param object_id: идентификатор типа объекта
    @param key_id: ключ искомого классификатора
    @param value: искомое значение
    @return: список идентификатор объектов
    """
    data = json.dumps(
        {"index": 'obj_' + FullTextSearch.TABLES[object_id] + '_row',
         "query": {"query_string": '@key_id ' + str(key_id) + '@val ' + str(value)}})
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    return [int(item['_id']) for item in json.loads(response.text)['hits']['hits']]


