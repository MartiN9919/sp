from requests.exceptions import ConnectionError
from data_base_driver.connect.connect_pgsql import db_pg_sql


def osm_search(text):
    """
    Поиск osm-записей
    @param text: поисковая строка
    @return: json [{id,name,icon,},...]
    """
    try:
        print(999, text)
        return [
            { 'id': 1, 'name': 'Тест 1', },
            { 'id': 2, 'name': 'Тест 2', },
            { 'id': 3, 'name': 'Тест 3', },
        ]
    except ConnectionError:
        return []



def osm_fc(id):
    return {}

        #def db_pg_sql(sql, wait=False, read=True, database=OSM, connection=-1):

"""
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
