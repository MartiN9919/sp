import json
import requests

from requests.exceptions import ConnectionError
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
    sql = 'SELECT ST_AsGeoJSON(way) FROM planet_osm_polygon WHERE osm_id = ' + str(id) + ';'
    return db_pg_sql(sql)[0][0]





"""
OLD
def aj_polygon_get_osm(request):
    data              = json.loads(request.body)
    polygon_name_list = data.get('polygon_name_list', [])
    if len(polygon_name_list)==0: return []
    polygon_name_str  = "'"+"','".join(polygon_name_list)+"'"

    features     = []
    for ind, item in enumerate(DB_read_lines_pgsql(
        sql=
            "SELECT "+
                OSM_POLYGON.OSM_ID+", "+
                OSM_POLYGON.NAME  +", "+
                OSM_POLYGON.TAGS  +", "+
                "ST_AsGeoJSON(ST_Transform("+OSM_POLYGON.WAY+", 4326)) as geojson "+
            "FROM " +OSM_POLYGON.TABLE+" "+
            "WHERE "+OSM_POLYGON.NAME +" IN ("+polygon_name_str+")",
        database=CONNECT.OSM)):
        feature  = geojson.Feature(
            geometry   = json.loads(item[3]),
            properties = {
                'id':               ind,
                OSM_POLYGON.OSM_ID: item[0],
                OSM_POLYGON.NAME:   item[1],
                OSM_POLYGON.TAGS:   item[2],
            },
        )
        features.append(feature)
    return geojson.FeatureCollection(features)

"""
