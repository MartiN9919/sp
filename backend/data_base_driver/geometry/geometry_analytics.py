import json

import requests

from data_base_driver.constants.const_dat import DAT_OBJ_COL
from data_base_driver.constants.const_fulltextsearch import FullTextSearch
from data_base_driver.input_output.input_output import io_get_obj
from data_base_driver.input_output.valid_permission_manticore import check_object_permission


def get_point_inside_polygon(polygon, points, group_id):
    """
    Функция для получения точек лежащих в пределах полигона
    @param polygon: список точек полигона в формате: [x1, y1, x2, y2, ..., xn, yn]
    @param points: список идентификаторов точек, для которых осуществляется поиск, если для всех - пустой список
    @param group_id: идентификатор группы пользователя
    @return: список идентификаторов подходящих точек
    """
    must = [{'equals': {'inside': 1}}]
    if len(points) > 0:
        must.append({'in': {DAT_OBJ_COL.ID: [int(rec_id) for rec_id in points]}})
    data = json.dumps({
        'index': DAT_OBJ_COL.table_name('point'),
        'script_fields': {
            'inside': {
                'script': {
                    'inline': 'CONTAINS(GEOPOLY2D(' + str(polygon)[1:-1] + '), lat, lon)'
                }
            }
        },
        'query': {
            'bool': {
                'must': must
            }
        }
    })
    response = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data).text)['hits']['hits']
    return [item['_source']['rec_id'] for item in response
            if check_object_permission(group_id, 25, item['_source']['rec_id'], False)]


def get_distance_between_point(point1, point2, group_id):
    """
    Функция для получения расстояния между 2 точками из базы данных
    @param point1: идентификатор первой точки
    @param point2: идентификатор второй точки
    @param group_id: идентификатор группы пользователя
    @return: расстояния в километрах
    """
    point_1_params = io_get_obj(group_id, 25, [25202, 25203], [point1], 100, '', {})
    if len(point_1_params) < 2:
        return 0
    lat = 0
    lon = 0
    for param in point_1_params:
        if param['key_id'] == 25202:
            lat = param['val']
        else:
            lon = param['val']
    data = json.dumps({
        'index': DAT_OBJ_COL.table_name('point'),
        'query': {
            'equals': {
                'rec_id': point2
            }
        },
        'script_fields': {
            'distance': {
                'script': {
                    'inline': 'GEODIST(' + str(lat) + ', ' + str(lon) + ', lat, lon, {in=degrees, out=km})'
                }
            }
        }
    })
    response = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data).text)['hits']['hits']
    if len(response) == 0:
        return 0
    return response[0]['_source']['distance']
