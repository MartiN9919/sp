import math

import geopandas
from shapely.geometry import Polygon


def get_distance(point1, point2):
    """
    Функция для получения расстояния между 2 точками
    @param point1: координаты первой точки
    @param point2: координаты второй точки
    @return: рассояние между исходными точками
    """
    return math.sqrt(((point1[0]-point2[0])**2) + ((point1[1]-point2[1])**2))


def get_polygon_from_lines(lines):
    """
    Функция для получения многоугольника из набора линий образующих его границы
    @param lines: список линий образующих границы многоугольника, должны идти в порядке смежности
    @return: многоугольник в формате geojson
    """
    points = []
    for line in lines:
        if len(points) == 0:
            points += line
        else:
            if get_distance(points[-1], line[0]) < get_distance(points[-1], line[-1]):
                points += line
            else:
                line.reverse()
                points += line
    result = Polygon(points)
    return geopandas.GeoSeries([result]).__geo_interface__
