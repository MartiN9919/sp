# -*- coding: utf-8 -*-

import json
import geojson

from   django.contrib.auth.decorators import login_required
from   web.lib.decor                  import decor_json, decor_required_ajax, decor_log_request, decor_required_superuser

from   lib.sys                        import tuple_to_dict
from   lib.db.const.const_connect     import CONNECT
from   lib.db.const.const_osm         import OSM_POLYGON
from   lib.db.connect.connect_mysql   import DB_read_lines as DB_read_lines_mysql, db_sql as db_sql_mysql
from   lib.db.connect.connect_pgsql   import DB_read_lines as DB_read_lines_pgsql, db_sql as db_sql_pgsql


########################################################
# OSM: ПОЛУЧИТЬ РЕГИОНы
# polygon_name_list - список наименований ['Могилёвская область', ...]
########################################################
@login_required(login_url='/auth/login/')
@decor_required_ajax
@decor_log_request
@decor_json
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



# ########################################################
# # GEO: ПРИНАДЛЕЖНОСТЬ ТОЧКИ РЕГИОНАМ
# # regions_id - (list) список регионов: [1, 2, ...]
# # geo_text   - (text) геометрия: 'POINT(26.83553 55.28771)'
# # return [[id, name], ...]
# ########################################################
# #SET @tt = ST_GeomFromText('POINT(26.83553 55.28771)', 4326);
# #SELECT name, ST_AsText(location),ST_AsText(@tt), ST_SRID(location), ST_SRID(@tt)  FROM geo_polygon
# #WHERE ST_Contains(location, @tt);
# ########################################################
# @login_required(login_url='/auth/login/')
# @decor_required_ajax
# @decor_log_request
# @decor_json
# def aj_polygon_contains(request):
#     data       = json.loads(request.body)
#     regions_id = data.get('regions_id', [])
#     geo_text   = data.get('geo_text',   '')
#     if (geo_text=='') or (len(regions_id)==0): return []
#     regions_id = map(lambda x: str(x), regions_id)
#     regions_id = ",".join(regions_id)

#     ret = []
#     for item in DB_read_lines_mysql(
#         sql =
#             'SELECT '+
#                 DATA_GEO_GC.ID  +', '+
#                 DATA_GEO_GC.NAME+' ' +
#             'FROM '+
#                 DATA_GEO_GC.TABLE+' '+
#             'WHERE '+
#                 DATA_GEO_GC.ID+' IN ('+regions_id+') AND '
#                 'ST_Contains('+
#                     DATA_GEO_GC.LOCATION+', '+
#                     'ST_GeomFromText("'+geo_text+'", 4326)'+
#                 ')',
#             database=CONNECT.DATA):
#         ret.append(tuple_to_dict(item, [DATA_GEO_GC.ID, DATA_GEO_GC.NAME]))
#     return ret
