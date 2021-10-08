import json
from math import sin, cos, atan2, sqrt

import requests
import geopandas
from functools import reduce

from shapely.speedups._speedups import LineString

from data_base_driver.constants.const_dat import DAT_OBJ_COL
from data_base_driver.constants.const_fulltextsearch import FullTextSearch
from data_base_driver.input_output.input_output import io_get_obj
from data_base_driver.input_output.valid_permission_manticore import check_object_permission


def deg_to_rad(angle):
    """
    Функция для перевода градусов в радианы
    @param angle: угол в градусах
    @return: угол в радианах
    """
    return angle * (3.14 / 180)


def get_distance_between_point_math(x1, y1, x2, y2):
    """
    Функция для получения расстояния между 2 точками по их географичесим координатам
    @param x1: координата по x 1 точки
    @param y1: координата по y 1 точки
    @param x2: координата по x 2 точки
    @param y2: координата по y 2 точки
    @return: расстояние в метрах между точками
    """
    R = 6371
    dx = deg_to_rad(x2-x1)
    dy = deg_to_rad(y2-y1)
    a = sin(dy/2) * sin(dy/2) + cos(deg_to_rad(y1)) * cos(deg_to_rad(y2)) * sin(dx/2) * sin(dx/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c * 1000


def get_lines_intersection(line1, line2):
    """
    Функция для получения точек и линий пересечения двух кривых
    @param line1: первая исходная линия shapely line string
    @param line2: вторая исходная линия shapely line string
    @return: feature collection содержащий пересекшиеся объекты
    """
    return line1.intersection(line2)


def get_line_buffer_polygon(line):
    """
    Функция для получения многоугольника описывающего линию
    @param line: исходная линия shapely line string
    @return: feature collection содержащий полигон описывающий заданную линию
    """
    return geopandas.GeoSeries([line.buffer(0.5)]).__geo_interface__


def get_points_inside_polygon(polygon, points, group_id):
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
    else:
        return []
    data = json.dumps({
        'index': DAT_OBJ_COL.table_name('point'),
        'script_fields': {
            'inside': {
                'script': {
                    'inline': 'CONTAINS(GEOPOLY2D(' + str(polygon)[1:-1] + '), '
                                                                           'point.coordinates[0], point.coordinates[1])'
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
                    'inline': 'GEODIST(' + str(lat) + ', ' + str(lon) + ', point.coordinates[1], point.coordinates[0], '
                                                                        '{in=degrees, out=km})'
                }
            }
        }
    })
    response = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data).text)['hits']['hits']
    if len(response) == 0:
        return 0
    return response[0]['_source']['distance']


def feature_collection_to_manticore_polygon(feature_collection):
    """
    Фунция для преобразования feature collection в формат полигона manticore/sphinx
    @param feature_collection: feature collection одержащий информацию о полигонах
    @return: полигон в формате [x1,y1,x2,y2,...,xn,yn]
    """
    temp_list = []
    for feature in feature_collection['features']:
        if feature['geometry']['type'] == 'GeometryCollection':
            for geometry in feature['geometry']['geometries']:
                if geometry['type'] == 'Polygon':
                    temp_list.append(geometry['coordinates'])
        else:
            if feature['geometry']['type'] == 'Polygon':
                temp_list.append(feature['geometry']['coordinates'])
    in_polygon = []
    out_polygon = []
    for temp in temp_list:
        in_polygon.append(reduce(lambda x, y: x+y, temp[0]))
        for out in temp[1:]:
            out_polygon.append(reduce(lambda x, y: x+y, out))
    return {'in_polygon': in_polygon, 'out_polygon': out_polygon}
