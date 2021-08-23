import json

import requests

from data_base_driver.connect.connect_pgsql import db_pg_sql
from data_base_driver.constants.const_fulltextsearch import FullTextSearch


def get_geometry_hint_by_request(request):
    data = json.dumps({
        'index': 'osm_polygon',
        'query': {
            'query_string': request
        }
    })
    response = requests.post(FullTextSearch.OSM_SEARCH_URL, data=data)
    result = [{'id': int(item['_id']), 'name': item['_source']['name'], 'address': item['_source']['addr']}
              for item in json.loads(response.text)['hits']['hits']]
    return result


def get_geometry_by_id(id):
    sql = 'SELECT ST_AsGeoJSON(way) FROM planet_osm_polygon WHERE osm_id = ' + str(id) + ';'
    return db_pg_sql(sql)[0][0]


def get_geometry_by_request(request):
    geometry = get_geometry_hint_by_request(request)
    for item in geometry:
        item['geometry'] = get_geometry_by_id(item['id'])
    return geometry


