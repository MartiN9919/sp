import json

from shapely.geometry import Polygon, LineString

from data_base_driver.additional_functions import date_client_to_server, str_to_sec
from data_base_driver.input_output.input_output import io_get_obj
from data_base_driver.input_output.input_output_mysql import io_get_obj_mysql_tuple, get_total_objects
from data_base_driver.input_output.io_geo import get_points_by_distance, get_points_inside_polygon, \
    feature_collection_by_geometry
from data_base_driver.sys_key.get_key_info import get_key_by_id
from objects.geometry.geometry_analytics import feature_collection_to_manticore_polygon
from objects.record.get_record import get_object_record_by_id_http, get_keys


def intercept_sort_list(elements):
    """
    Функция для пересечения списков с сохранением сортировки
    @param elements: список содержащий списки целых чисел
    @return: список целых чисел встреченных во всех начальных списков с сохранением их сортировки
    """
    if len(elements) == 1:
        return elements[0]
    temp_list = []
    for elem in elements[0]:
        temp = {'elem': elem, 'pos': []}
        for item in elements:
            if elem not in item:
                temp['pos'] = []
                break
            else:
                temp['pos'].append(item.index(elem))
        if len(temp['pos']) > 0:
            temp['middle'] = sum(temp['pos']) / len(temp['pos'])
            temp_list.append(temp)
        else:
            continue
    temp_list.sort(key=lambda x: x['middle'])
    return [temp['elem'] for temp in temp_list]


def sort_result(fetchall):
    temp = {}
    for item in fetchall:
        if temp.get(item[0]) is None:
            temp[item[0]] = 0
        temp[item[0]] += item[1]
    result = sorted(tuple(temp.items()), key=lambda x: x[1])
    return list(result)


def get_intercept_items(items):
    result = []
    for i in items[0]:
        temp_list = [[k for k in j if k[0] == i[0]] for j in items]
        if all(temp_list):
            result.append((i[0], sum(j[0][1] for j in temp_list)))
    return result


def filter_actual(group_id, object_id, fetchall):
    result = []
    for item in fetchall:
        temp_word = '@key_id ' + str(item[1])
        temp = io_get_obj(group_id, object_id, [], [item[0]], 500, temp_word, {'second_start': item[2] + 1})
        if len(temp) == 0:
            result.append(item)
    return result


def filter_date_range(group_id, object_id, items, date_range):
    second_start = str_to_sec(date_client_to_server(date_range.split('-')[0]) + ' 23:59:59')
    second_end = str_to_sec(date_client_to_server(date_range.split('-')[1]) + ' 23:59:59')
    result = []
    for item in items:
        if second_start < item[2] < second_end:
            result.append(item)
        elif item[2] < second_end:
            temp_word = '@key_id ' + str(item[1])
            temp = io_get_obj(group_id, object_id, [], [item[0]], 500, temp_word, {'second_start': item[2] + 1,
                                                                                   'second_end': second_start})
            if len(temp) == 0:
                result.append(item)
    return result


def get_search_result(group_id, word, object_id, actual, date_range=None):
    temp_result = io_get_obj(group_id, object_id, [], [], 500, word, {})
    fetchall = [(int(item['rec_id']), int(item['key_id']), int(item['sec']), item['score']) for item in temp_result]
    fetchall = filter_actual(group_id, object_id, fetchall) if actual else fetchall
    if date_range:
        fetchall = filter_date_range(group_id, object_id, fetchall, date_range)
    return [{'rec_id': item[0], 'object_id': object_id, 'score': item[3]} for item in fetchall]


def find_reliable_http(object_id, request, actual=False, group_id=0):
    if isinstance(request, str) or request is None:
        return find_text(group_id, object_id, request, actual)
    elif isinstance(request, list):
        return find_advanced(group_id, object_id, request, actual)


def find_text(group_id, object_id, request, actual=False, score=False):
    """
    Функция для поиска значений в таблице object, возвращает результат только при полном совпадении
    @param object_id: тип объекта по которым идет поиск
    @param request: искомые параметры
    @param actual: флаг актуальности искомого параметра, если True то учитываются только записи актуальные для объекта
    на данный момент
    @param group_id: идентификатор группы пользователя
    @param score: возвращать ли баллы совпадения
    @return: список id объектов с искомыми параметрами, если score False, в противном случае список кортежей с
    идентификаторами и балами совпадения
    """
    if request is None or len(request) == 0:
        if score:
            return get_total_objects(group_id, object_id)['objects']
        else:
            return [item[0] for item in get_total_objects(group_id, object_id)['objects']]
    request = request.split(' ')
    request = [word.replace('-', '<<') for word in
               request]  # костыль, в последующем поменять настройки мантикоры, что бы индексировала '-'
    result = []
    for param in request:
        word = f"@val {param}" if len(param) > 0 else param  # искать только по значению
        if score:
            temp = sort_result(
                list((item['rec_id'], item['score']) for item in get_search_result(group_id, word, object_id, actual)))
            result.append(temp)
        else:
            result.append(list(set([item['rec_id'] for item in get_search_result(group_id, word, object_id, actual)])))
    if score:
        return get_intercept_items(result)
    else:
        return intercept_sort_list(result)


def find_advanced(group_id, object_id, request, actual=False):
    keys = {}
    result = []
    for param in request:
        if keys.get(param['id']) is None:
            keys[param['id']] = []
        keys[param['id']].append({'value': param['value'], 'range': param['date']})
    for key in keys:
        result.append(find_by_type(group_id, object_id, key, keys[key], actual))
    return intercept_sort_list(result)


def find_by_type(group_id, object_id, key, values, actual):
    key_info = get_key_by_id(key)
    key_type = key_info['type'] if key_info['list_id'] is None else 'list'
    if key_type == 'date' or key_type == 'datetime':
        return find_date_advanced(group_id, object_id, key, values, actual)
    elif key_type == 'geometry':
        return find_geometry_advanced(group_id, values, actual)
    elif key_type == 'geometry_point':
        return find_point_advanced(group_id, values, actual)
    else:
        return find_text_advanced(group_id, object_id, key, values, actual)


def find_text_advanced(group_id, object_id, key, values, actual):
    result = set()
    for value in values:
        word = f"@key_id {key} @val {value['value']}"
        fetchall = get_search_result(group_id, word, object_id, actual, value['range'])
        result.update(set([item['rec_id'] for item in fetchall]))
    return list(result)


def find_date_advanced(group_id, object_id, key, values, actual):
    result = set()
    for value in values:
        date_start = date_client_to_server(value['value'].split('-')[0])
        date_end = date_client_to_server(value['value'].split('-')[1])
        where_dop = [f"val > '{date_start}'", f"val < '{date_end}'"]
        temp_result = io_get_obj_mysql_tuple(group_id, object_id, [key], [], None, where_dop)
        temp_result = [[item[0], item[1], str_to_sec(item[3])] for item in temp_result]
        temp_result = filter_actual(group_id, object_id, temp_result) if actual else temp_result
        temp_result = filter_date_range(group_id, object_id, temp_result, value['range'])
        result.update(set([item[0] for item in temp_result]))
    return list(result)


def find_point_advanced(group_id, values, actual):
    result = set()
    for value in values:
        polygon = feature_collection_to_manticore_polygon(value['value'])
        fetchall = get_points_inside_polygon(polygon['in_polygon'], [], group_id)
        result.update(set(fetchall))
    return list(result)


def find_geometry_advanced(group_id, values, actual):
    result = set()
    for value in values:
        geometries = [item[0] for item in get_total_objects(group_id, 30)['objects']]
        fc_polygons = feature_collection_by_geometry(group_id, 30, geometries, [], {})
        polygon = Polygon(value['value']['features'][0]['geometry']['coordinates'][0])
        fetchall = []
        for feature in fc_polygons['features']:
            geometry = feature['geometry']['geometries'][0]
            if geometry['type'] == 'Polygon':
                if polygon.intersects(Polygon(geometry['coordinates'][0])):
                    fetchall.append(feature['rec_id'])
            elif geometry['type'] == 'LineString':
                if polygon.intersects(LineString(geometry['coordinates'])):
                    fetchall.append(feature['rec_id'])
        result.update(set(fetchall))
    return list(result)


def find_unreliable_http(object_type, request, group_id=0):
    """
    Функция для поиска значений в таблице object, возвращает наиболее похожие результаты
    @param object_type: тип объекта по которым идет поиск
    @param request: искомые параметры
    @param group_id: идентификатор группы пользователя
    @return: список id объектов с искомыми параметрами, если подобных нет, то пустой список
    """
    request = request.replace(' ', '|')
    response = io_get_obj(group_id, object_type, [], [], 500, request, {})
    return [int(hit['rec_id']) for hit in response]


def find_key_value_http(object_id, key_id, value, group_id=0):
    """
    Функция для нахождения в базе данных по отдельным полям
    @param object_id: идентификатор типа объекта
    @param key_id: ключ искомого классификатора
    @param value: искомое значение
    @param group_id: идентификатор группы пользователя
    @return: список идентификатор объектов
    """
    if get_key_by_id(key_id)['type'] == 'date' or get_key_by_id(key_id)['type'] == 'date_time':
        value = str(value).replace('-', '<<')
    else:
        value = str(value)
    response = io_get_obj(group_id, object_id, [], [], 500, '@key_id ' + str(key_id) + ' @val ' + value, {})
    if get_key_by_id(key_id)['type'] != 'date' and get_key_by_id(key_id)['type'] != 'date_time':
        response = [item for item in response if item['val'].lower() == value.lower()]
    remove_list = []
    for index, item in enumerate(response):
        temp_word = '@key_id ' + str(key_id)
        temp = io_get_obj(group_id, object_id, [], [item['rec_id']], 500, temp_word, {})
        for temp_item in temp:
            if item['sec'] == temp_item['sec']:
                continue
            else:
                if item['sec'] < temp_item['sec'] and item['val'] != temp_item['val']:
                    remove_list.append(index)
    return [int(item['rec_id']) for index, item in enumerate(response) if index not in remove_list]


def find_point_intersection(params):
    lat = 0
    lon = 0
    for param in params:
        if param[0] == 25204:
            coordinates = json.loads(param[1])
            lat = coordinates['coordinates'][1]
            lon = coordinates['coordinates'][0]
    return get_points_by_distance(lat, lon, 50)


def find_duplicate_objects(group_id, object_id, rec_id, params):
    """
    Функция для поиска дубликатов объектов при создании/изменении
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param params: вносимые/изменяемые параметры
    @return: список идентификаторов объектов с похожими значениями
    """
    result = []
    if object_id == 25:
        result = find_point_intersection(params)
    nums = len(list(filter(lambda x: x['obj_id'] == object_id and x['need'], get_keys())))
    old_object = get_object_record_by_id_http(object_id, rec_id, group_id) if rec_id else {}
    needed_old_params = [param for param in old_object.get('params', []) if
                         get_key_by_id(param['id']).get('need', 0) == 1]
    new_params = {}
    for param in params:
        key = get_key_by_id(param[0])
        if key['need']:
            new_params[param[0]] = {'value': param[1], 'date': param[2]}
    for param in needed_old_params:
        if param['id'] not in new_params:
            new_params[param['id']] = param['values'][0]
    if nums > len(new_params) or len([item for item in params if get_key_by_id(item[0]).get('need', 0) == 1]) == 0:
        return result
    temp_result = set(
        find_key_value_http(object_id, list(new_params.keys())[0], list(new_params.values())[0]['value'], group_id))
    for param in list(new_params.keys())[1:]:
        temp_result.intersection_update(
            set(find_key_value_http(object_id, param, new_params[param]['value'], group_id)))
    return list(temp_result) + result


def find_same_objects(group_id, object_id, params):
    nums = len(list(filter(lambda x: x['obj_id'] == object_id and x['need'], get_keys())))
    new_params = {}
    for param in params:
        if get_key_by_id(param[0]).get('need', 0) == 1:
            new_params[param[0]] = {'value': param[1], 'date': param[2]}
    if nums == len(new_params) or len(new_params) == 0:
        return []
    else:
        result = set(
            find_key_value_http(object_id, list(new_params.keys())[0], list(new_params.values())[0]['value'], group_id))
        if len(list(new_params.keys())) > 1:
            for param in list(new_params.keys())[1:]:
                result.intersection_update(set(find_key_value_http(object_id, param, new_params[param]['value'],
                                                                   group_id)))
        return list(result)

