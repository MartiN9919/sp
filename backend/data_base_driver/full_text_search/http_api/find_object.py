import json

import requests
from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.full_text_search.additional_functions import get_date_from_days_sec


def find_reliable_http(object_type, request):
    request = request.split(' ')
    result = None
    for word in request:
        data = json.dumps({"index": "obj_" + object_type + "_row", "query": {"match": {"val": word}}})
        response = requests.post(FullTextSearch.SEARCH_URL, data=data)
        fetchall = [int(hit['_id']) for hit in json.loads(response.text)['hits']['hits']]
        if result == None:
            result = set(fetchall)
        else:
            result.intersection_update(set(fetchall))
    return [item for item in list(result)]


def find_unreliable_http(object_type, request):
    request = request.replace(' ', '|')
    data = json.dumps({"index": "obj_" + object_type + "_row", "query": {"match": {"val": request}}})
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    return [int(hit['_id']) for hit in json.loads(response.text)['hits']['hits']]


def get_object_record_by_id_http(object_id, rec_id):
    data = json.dumps(
        {"index": 'obj_' + FullTextSearch.TABLES[object_id] + '_row', "query": {"equals": {"id": rec_id}}})
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    temp = [(item['_source']['key_id'], item['_source']['val'], item['_source']['date'], item['_source']['sec']) for
            item in json.loads(response.text)['hits']['hits']]
    params = [{'id': int(item[0]), 'val': item[1], 'date': get_date_from_days_sec(int(item[2]), int(item[3]))} for item
              in temp]
    return {'object_id': object_id, 'rec_id': rec_id, 'params': params}

