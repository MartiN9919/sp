import json
import geojson
import requests

from requests.exceptions import ConnectionError

from data_base_driver.constants.const_osm import OSM_POLYGON
from data_base_driver.connect.connect_pgsql import db_pg_sql
from data_base_driver.constants.const_fulltextsearch import FullTextSearch

def osm_search(text, geometry=False):
    """
    Поиск osm-записей
    @param text: поисковая строка
    @return: json [{id,name,address,},...]
    """
    try:
        data = text.strip()
        if data == '': return []
        data = json.dumps({
            'index': 'osm_polygon',
            'query': { 'query_string': data, },
        })
        response = requests.post(FullTextSearch.OSM_SEARCH_URL, data=data)
        result = [{'id': int(item['_id']), 'name': item['_source']['name'], 'address': item['_source']['addr']}
            for item in json.loads(response.text)['hits']['hits']]

        if geometry:
            for item in geometry:
                item['geometry'] = osm_fc(item['id'])

        return result
    except ConnectionError:
        return []


def osm_fc(id):
    """
    геомерия(geojson) по ее идентификатору
    @param id: идентификатор геометрии
    @return: geojson
    """
    sql = \
        "SELECT "+\
            OSM_POLYGON.NAME+", "+\
            "ST_AsGeoJSON(ST_Transform("+OSM_POLYGON.WAY+", 4326)) as "+OSM_POLYGON.WAY+" "+\
        "FROM "+OSM_POLYGON.TABLE+" "+\
        "WHERE "+OSM_POLYGON.OSM_ID+" = " + str(id) + ";"
    features = []
    for ind, item in enumerate(db_pg_sql(sql)):
        feature  = geojson.Feature(
            geometry   = json.loads(item[1]),
            properties = {
                'id':             id,
                OSM_POLYGON.NAME: item[0],
            },
        )
        features.append(feature)
    return geojson.FeatureCollection(features)
