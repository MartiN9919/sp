from math import sin, cos, atan2, sqrt

import geopandas
from functools import reduce


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
    @param line: исходная линия shapely line string1
    @return: feature collection содержащий полигон описывающий заданную линию
    """
    return geopandas.GeoSeries([line.buffer(0.005)]).__geo_interface__


def feature_collection_to_manticore_polygon(feature_collection):
    """
    Функция для преобразования feature collection в формат полигона manticore/sphinx
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
