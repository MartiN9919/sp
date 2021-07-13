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
    value = str(value).replace('-', '<<')
    data = json.dumps(
        {"index": 'obj_' + FullTextSearch.TABLES[object_id] + '_row',
         "query": {"query_string": '@key_id ' + str(key_id) + ' @val ' + value},
         "limit": 100})
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    remove_list = []
    for item in json.loads(response.text)['hits']['hits']:
        temp_word = '@key_id ' + str(key_id)
        data = json.dumps({"index": "obj_" + FullTextSearch.TABLES[object_id] + "_row",
                           "query": {
                               "query_string": temp_word,
                               'equals': {'rec_id': item['_source']['rec_id']}
                           },
                           "limit": 500})
        temp_response = requests.post(FullTextSearch.SEARCH_URL, data=data)
        temp = json.loads(temp_response.text)['hits']['hits']
        for temp_item in temp:
            if item['_source']['sec'] == temp_item['_source']['sec']:
                continue
            else:
                if item['_source']['sec'] < temp_item['_source']['sec']:
                    remove_list.append(item)
    return [int(item['_source']['rec_id']) for item in json.loads(response.text)['hits']['hits']
            if not int(item['_source']['rec_id']) in remove_list]


