import itertools
import json
import requests
from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.full_text_search.additional_functions import get_date_from_days_sec


def find_reliable_http(object_type, request):
    """
    Функция для поиска значений в таблице object, возвращает результат только при полном совпадении
    @param object_type: тип объекта по которым идет поиск
    @param request: искомые параметры
    @return: список id объектов с искомыми параметрами, если не найдено, то пустой список
    """
    request = request.split(' ')
    result = None
    for word in request:
        data = json.dumps({"index": "obj_" + object_type + "_row", "query": {"match": {"val": word}}, "limit": 500})
        response = requests.post(FullTextSearch.SEARCH_URL, data=data)
        fetchall = [int(hit['_source']['rec_id']) for hit in json.loads(response.text)['hits']['hits']]
        if result == None:
            result = set(fetchall)
        else:
            result.intersection_update(set(fetchall))
    return [item for item in list(result)]


def find_unreliable_http(object_type, request):
    """
    Функция для поиска значений в таблице object, возвращает наиболее похожие результаты
    @param object_type: тип объекта по которым идет поиск
    @param request: искомые параметры
    @return: список id объектов с искомыми параметрами, если подобных нет, то пустой список
    """
    request = request.replace(' ', '|')
    data = json.dumps({"index": "obj_" + object_type + "_row", "query": {"match": {"val": request}}, "limit": 500})
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    return [int(hit['_source']['rec_id']) for hit in json.loads(response.text)['hits']['hits']]


def get_object_record_by_id_http(object_id, rec_id):
    """
    Функция для получения информации о объекте по его типу и идентификатору записи
    @param object_type: тип объекта
    @param rec_id: идентификатору записи
    @return: словарь в формате {object_id, rec_id, params:[{id,val},...,{}]}
    """
    data = json.dumps(
        {"index": 'obj_' + FullTextSearch.TABLES[object_id] + '_row',
         "query": {"equals": {"rec_id": rec_id}},
         "limit": 500})
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    temp = [(item['_source']['key_id'], item['_source']['val'], item['_source']['date'], item['_source']['sec']) for
            item in json.loads(response.text)['hits']['hits']]
    params = []
    for item in temp:
        keys = [key for key in params if key['id'] == item[0]]
        if len(keys) > 0:
            for key in keys:
                if key['date'] > get_date_from_days_sec(int(item[2]), int(item[3])):
                    key['old'].append({'value': item[1], 'date': get_date_from_days_sec(int(item[2]), int(item[3]))})
                else:
                    key['old'].append({'value': key['value'], 'date': key['date']})
                    key['value'] = item[1]
                    key['date'] = get_date_from_days_sec(int(item[2]), int(item[3]))
            continue
        params.append({'id': int(item[0]), 'value': item[1], 'date': get_date_from_days_sec(int(item[2]), int(item[3])), 'old':[]})

    for item in params:
        item['old'].sort(key=lambda x: x['date'])

    return {'object_id': object_id, 'rec_id': rec_id, 'params': params}

