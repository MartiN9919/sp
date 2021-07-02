import json
import requests
from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.full_text_search.additional_functions import get_date_from_days_sec, intercept_sort_list


def find_reliable_http(object_type, request, actual=False):
    """
    Функция для поиска значений в таблице object, возвращает результат только при полном совпадении
    @param object_type: тип объекта по которым идет поиск
    @param request: искомые параметры
    @param actual: флаг актуальности искомого параметра, если True то учитываются только записи актуальные для объекта на данный момент
    @return: список id объектов с искомыми параметрами, если не найдено, то пустой список
    """
    request = request.split(' ')
    result = []
    for word in request:
        data = json.dumps({"index": "obj_" + object_type + "_row", "query": {"query_string": word}, "limit": 500})
        response = requests.post(FullTextSearch.SEARCH_URL, data=data)
        fetchall = [(int(hit['_source']['rec_id']), int(hit['_source']['key_id']), (int(hit['_source']['date'])),
                     (int(hit['_source']['sec']))) for hit in json.loads(response.text)['hits']['hits']]
        remove_list = []
        if actual:
            for item in fetchall:
                temp_word = '@key_id ' + str(item[1])
                data = json.dumps({"index": "obj_" + object_type + "_row",
                                   "query": {
                                       "query_string": temp_word,
                                       'equals': {'rec_id': item[0]}
                                   },
                                   "limit": 500})
                response = requests.post(FullTextSearch.SEARCH_URL, data=data)
                temp = json.loads(response.text)['hits']['hits']
                for temp_item in temp:
                    if item[2] == temp_item['_source']['date'] and item[3] == temp_item['_source']['sec']:
                        continue
                    else:
                        if item[2] < temp_item['_source']['date'] or item[2] == temp_item['_source']['date'] \
                                and item[3] < temp_item['_source']['sec']:
                            remove_list.append(item)
        fetchall = [item[0] for item in fetchall if not item in remove_list]
        if result == None:
            result.append(list(dict.fromkeys(fetchall)))
        else:
            result.append(list(dict.fromkeys(fetchall)))
    return intercept_sort_list(result)


def find_unreliable_http(object_type, request):
    """
    Функция для поиска значений в таблице object, возвращает наиболее похожие результаты
    @param object_type: тип объекта по которым идет поиск
    @param request: искомые параметры
    @return: список id объектов с искомыми параметрами, если подобных нет, то пустой список
    """
    request = request.replace(' ', '|')
    data = json.dumps({"index": "obj_" + object_type + "_row", "query": {"query_string": request}, "limit": 500})
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
    temp = [(int(item['_source']['key_id']), item['_source']['val'], item['_source']['date'], item['_source']['sec']) for
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
        params.append({'id': int(item[0]), 'value': item[1], 'date': get_date_from_days_sec(int(item[2]), int(item[3])),
                       'old': []})

    for item in params:
        item['old'].sort(key=lambda x: x['date'])

    return {'object_id': object_id, 'rec_id': rec_id, 'params': params}

