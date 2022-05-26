import json
import geojson
import requests

from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_OBJ_ROW, DAT_OBJ_COL
from data_base_driver.constants.const_fulltextsearch import FullTextSearch
from data_base_driver.constants.const_geocoder import Geocoder
from data_base_driver.constants.const_key import SYS_KEY_CONSTANT
from data_base_driver.input_output.input_output import io_get_obj, io_get_rel
from data_base_driver.input_output.valid_permission_manticore import check_object_permission
from data_base_driver.sys_key.get_list import get_item_list_value
from data_base_driver.additional_functions import get_date_time_from_sec
from data_base_driver.sys_key.get_key_info import get_key_by_id


def feature_collection_by_geometry(group_id, object_type, rec_id, keys, time_interval):
    """
    Функция для получения feature collection в формате geojson для конкретных экземпляров геометрий
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта (25 - точка, 30 - геометрия)
    @param rec_id: список идентификаторов объектов
    @param keys: список идентификаторов ключей классификатора которые необходимо вынести в properties
    @param time_interval: интервал времени в который должны были быть созданы искомые записи
    @return: feature collection содержащая информацию о искомых геометриях
    """
    from data_base_driver.sys_key.get_list import get_item_list_value
    if object_type == SYS_KEY_CONSTANT.POINT_ID:
        keys += [SYS_KEY_CONSTANT.POINT_CLASSIFIER_ID, SYS_KEY_CONSTANT.POINT_TYPE_CLASSIFIER_ID,
                 SYS_KEY_CONSTANT.BORDER_POINT]
    elif object_type == SYS_KEY_CONSTANT.GEOMETRY_ID:
        keys += [SYS_KEY_CONSTANT.GEOMETRY_CLASSIFIER_ID, SYS_KEY_CONSTANT.GEOMETRY_TYPE_CLASSIFIER_ID]
    else:
        raise Exception(1, 'Неверный тип объекта')
    if len(rec_id) == 0:
        return geojson.FeatureCollection(features=[])
    records = io_get_obj(group_id, object_type, keys, rec_id, 1000, '', time_interval)
    objects = {}
    for record in records:
        if not objects.get(record[DAT_OBJ_ROW.ID]):
            objects[record[DAT_OBJ_ROW.ID]] = {}
        if get_key_by_id(record[DAT_OBJ_ROW.KEY_ID])[DAT_SYS_KEY.TYPE_VAL] == 'geometry' or \
                get_key_by_id(record[DAT_OBJ_ROW.KEY_ID])[DAT_SYS_KEY.TYPE_VAL] == 'geometry_point':
            if not objects[record[DAT_OBJ_ROW.ID]].get('geometry'):
                objects[record[DAT_OBJ_ROW.ID]]['geometry'] = []
            objects[record[DAT_OBJ_ROW.ID]]['geometry'].append({DAT_OBJ_ROW.KEY_ID: record[DAT_OBJ_ROW.KEY_ID],
                                                                DAT_OBJ_ROW.VAL: record[DAT_OBJ_ROW.VAL],
                                                                DAT_OBJ_ROW.SEC: record[DAT_OBJ_ROW.SEC]})
            objects[record[DAT_OBJ_ROW.ID]]['geometry'].sort(key=lambda x: x[DAT_OBJ_ROW.SEC], reverse=True)
        elif int(record[DAT_OBJ_ROW.KEY_ID]) == SYS_KEY_CONSTANT.BORDER_POINT:
            if not objects[record[DAT_OBJ_ROW.ID]].get('text'):
                objects[record[DAT_OBJ_ROW.ID]]['text'] = []
            objects[record[DAT_OBJ_ROW.ID]]['text'].append({DAT_OBJ_ROW.KEY_ID: record[DAT_OBJ_ROW.KEY_ID],
                                                            DAT_OBJ_ROW.VAL: record[DAT_OBJ_ROW.VAL],
                                                            DAT_OBJ_ROW.SEC: record[DAT_OBJ_ROW.SEC]})
            objects[record[DAT_OBJ_ROW.ID]]['text'].sort(key=lambda x: x[DAT_OBJ_ROW.SEC], reverse=True)
        elif int(record[DAT_OBJ_ROW.KEY_ID]) in SYS_KEY_CONSTANT.GEOMETRY_TYPES:
            temp_value = str(get_item_list_value(record[DAT_OBJ_ROW.VAL]))
            value = temp_value[temp_value.index('(') + 1:temp_value.index(')')]
            if not objects[record[DAT_OBJ_ROW.ID]].get('type'):
                objects[record[DAT_OBJ_ROW.ID]]['type'] = []
            objects[record[DAT_OBJ_ROW.ID]]['type'].append({DAT_OBJ_ROW.KEY_ID: record[DAT_OBJ_ROW.KEY_ID],
                                                            DAT_OBJ_ROW.VAL: value,
                                                            DAT_OBJ_ROW.SEC: record[DAT_OBJ_ROW.SEC]})
            objects[record[DAT_OBJ_ROW.ID]]['type'].sort(key=lambda x: x[DAT_OBJ_ROW.SEC], reverse=True)
        else:
            if not objects[record[DAT_OBJ_ROW.ID]].get('params'):
                objects[record[DAT_OBJ_ROW.ID]]['params'] = []
            old_params = [item for item in objects[record[DAT_OBJ_ROW.ID]]['params'] if
                          item['key_id'] == record[DAT_OBJ_ROW.KEY_ID]]
            if len(old_params) > 0:
                old_params[0] = {DAT_OBJ_ROW.KEY_ID: record[DAT_OBJ_ROW.KEY_ID],
                                 DAT_OBJ_ROW.VAL: record[DAT_OBJ_ROW.VAL],
                                 DAT_OBJ_ROW.SEC: record[DAT_OBJ_ROW.SEC]}
            else:
                objects[record[DAT_OBJ_ROW.ID]]['params'].append({DAT_OBJ_ROW.KEY_ID: record[DAT_OBJ_ROW.KEY_ID],
                                                                  DAT_OBJ_ROW.VAL: record[DAT_OBJ_ROW.VAL],
                                                                  DAT_OBJ_ROW.SEC: record[DAT_OBJ_ROW.SEC]})
    temp = []
    for object in objects:
        if objects[object].get('geometry'):
            geometry = json.loads(objects[object].get('geometry')[0]['val'])
            params = {'hint': ''}
            for param in objects[object].get('params', []):
                params[get_key_by_id(param[DAT_OBJ_ROW.KEY_ID])[DAT_SYS_KEY.NAME]] = \
                    [param[DAT_OBJ_ROW.VAL], get_date_time_from_sec(param[DAT_OBJ_ROW.SEC])]
                params['hint'] += param[DAT_OBJ_ROW.VAL]
            if objects[object].get('type'):
                params['class'] = objects[object]['type'][0]['val']
            if objects[object].get('text'):
                params['text'] = objects[object]['text'][0]['val']
            feature = geojson.Feature(geometry=geometry, properties=params)
            feature['rec_id'] = object
            feature['obj_id'] = object_type
            temp.append(feature)
    return geojson.FeatureCollection(temp)


def get_geometries(group_id, rec_id):
    return feature_collection_by_geometry(group_id, 30, [rec_id], [], {})['features'][0]['geometry']['geometries']


def relations_to_geometry_id(group_id, geometry_type, object_type, rec_id, keys_relation, time_interval):
    """
    Функция для преобразования связей в идентификаторы геометрий
    @param group_id: идентификатор группы пользователя
    @param geometry_type: идентификатор типа геометрии (25 - точка, 30 - геометрия)
    @param object_type: идентификатор связи объекта связь с которым мы ищем, если с любым то 0
    @param rec_id: идентификатор объекта, если не известен то 0
    @param keys_relation: список идентификаторов типов связей между геометрией и объектом
    @param time_interval: временной интервал установления связи в секундах
    @return: список идентификаторов найденных геометрических объектов
    """
    if object_type == 0:
        object = []
    elif rec_id == 0:
        object = [object_type]
    else:
        object = [object_type, rec_id]
    relations = io_get_rel(group_id, keys_relation, object, [geometry_type, ], [], time_interval, True)
    objects = [(int(item['obj_id_1']), int(item['rec_id_1'])) for item in relations] + \
              [(int(item['obj_id_2']), int(item['rec_id_2'])) for item in relations]
    geo_ids = [item[1] for item in objects if item[0] == geometry_type]
    return geo_ids


def build_tree_from_list(geometry_list):
    """
    Функция точка входа для построения дерева геометрий
    @param geometry_list: список геометрий
    @return: дерево геометрий
    """
    root = [item for item in geometry_list if item['parent_id'] == 0]
    for temp in root:
        temp.pop('parent_id')
    temp_geometry_list = [item for item in geometry_list if item not in root]
    temp_folders = {}
    for item in temp_geometry_list:
        if not temp_folders.get(item['parent_id']):
            temp_folders[item['parent_id']] = []
        temp_folders[item['parent_id']].append(item)
    for folder in temp_folders:
        for item in temp_folders[folder]:
            item.pop('parent_id')
        root.append({'name': get_item_list_value(int(folder)), 'children': temp_folders[folder]})
    return root


def get_geometry_search(text):
    """
    Функция для получения дерева геометрий, отфильтрованного по text
    @param text: текст запроса поиска
    @return: дерево геометрий
    """
    data = json.dumps({
        'index': 'obj_geometry_col',
        'query': {
            'query_string': '@name ' + text,
        },
        'limit': 1000,
    })
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    geometries = [{
        'id': item['_source']['rec_id'],
        'name': item['_source']['name'],
        'parent_id': item['_source']['parent_id'],
        'sec': item['_source']['sec'],
    } for item in json.loads(response.text)['hits']['hits']]
    temp_result, temp_id = [], []
    for geometry in geometries:
        if geometry['id'] in temp_id:
            continue
        temp_id.append(geometry['id'])
        data = json.dumps({
            'index': 'obj_geometry_col',
            'query': {
                'equals': {'rec_id': int(geometry['id'])}
            }
        })
        temp_geometry = {'id': geometry['id'], 'name': geometry['name'], 'parent_id': 0}
        geometry_information = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data).text)['hits']['hits']
        geometry_information.sort(key=lambda x: x['_source']['sec'])
        for temp in geometry_information:
            if temp['_source']['parent_id'] != 0:
                temp_geometry['parent_id'] = temp['_source']['parent_id']
            if len(temp['_source']['name']) != 0:
                temp_geometry['name'] = temp['_source']['name']
        temp_result.append(temp_geometry)
    return build_tree_from_list(temp_result)


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
        if param['key_id'] == 25204:
            coordinates = json.loads(param[1])
            lat = coordinates['coordinates'][1]
            lon = coordinates['coordinates'][0]
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


def get_points_by_distance(lat: float, lon: float, distance: int) -> list:
    """
    Функция для получения всех точек на удалении дистанции от заданной
    @param lat: широта
    @param lon: долгота
    @param distance: дистанция
    @return: список идентификаторов точек
    """
    data = json.dumps({
        'index': DAT_OBJ_COL.table_name('point'),
        'query': {
            "range": {
                'distance': {
                    'gte': 0,
                    'lte': float(distance)
                }
            }
        },
        'script_fields': {
            'distance': {
                'script': {
                    'inline': 'GEODIST(' + str(lat) + ', ' + str(lon) + ', point.coordinates[1], point.coordinates[0], '
                                                                        '{in=degrees, out=metres})'
                }
            }
        },
    })
    response = json.loads(requests.post(FullTextSearch.SEARCH_URL, data=data).text)['hits']['hits']
    return [item['_source']['rec_id'] for item in response]


def get_feature_collection_by_address(address: str) -> dict:
    """
    Функция для получения feature collection по адресу
    @param address: адрес
    @return: feature collection содержащий геометрии относящиеся к этому адресу
    """
    result = requests.get(Geocoder.SEARCH_URL, params={'q': address})
    return result.json()


def get_point_by_address(address: str) -> dict:
    """
    Функция для получения  json точки по адресу
    @param address: адрес
    @return: json точки если найдена или пустой словарь
    """
    feature_collection = get_feature_collection_by_address(address)
    for feature in feature_collection['features']:
        if feature['geometry']['type'] == 'Point':
            return feature['geometry']
    else:
        return {}
