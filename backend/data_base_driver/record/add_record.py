import datetime
import json

from data_base_driver.input_output.io_geo import get_geometry_id_by_name, get_geometry_by_id
from data_base_driver.record.find_object import find_key_value_http
from data_base_driver.record.get_record import get_object_record_by_id_http, get_keys_by_object
from data_base_driver.input_output.input_output import io_set
from data_base_driver.record.validate_record import validate_record, get_country_by_number, remove_special_chars, \
    validate_geometry_permission
from data_base_driver.relations.add_rel import add_rel_by_other_object
from data_base_driver.sys_key.get_key_dump import get_key_by_id


def add_record(group_id, object_id, object_info):
    """
    функция для добавления объекта в базу данных
    @param group_id: идентификационный номер группы пользователя
    @param object_id: идентификационный номер типа объекта
    @param object_info: информация об объекте в формате [[key:value],[],...,[]]
    для добавления информации о уже существующем объекте необходимо в качестве ключа передать id,
    а в качестве значение точный идентификационный номер объекта
    @return: rec_id добавленной записи
    """
    result = io_set(group_id=group_id, obj=object_id, data=object_info)
    if result[0]:
        return result[1]
    else:
        return -1


def additional_processing(user, object, data):
    """
    Функция для дополнительной обработки входящих параметров с учетом особенностей системы
    @param user: объект пользователя
    @param object: объект для добавления
    @param data: данные для добавления
    """
    if object.get('object_id') == 52:
        country = get_country_by_number([param for param in object['params'] if param['id'] == 50054][0]['value'])
        fl = 0
        for temp in data:
            if temp[0] == 50054:
                temp[1] = remove_special_chars(temp[1])
            if temp[0] == 50055:
                temp[1] = country
                fl = 1
        if fl == 0:
            data.append([50055, country, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    # костыль для добавления геометрических объектов, придумать как переделать------------------------------------------
    if object.get('object_id') == 25:
        point = [item for item in data if item[0] == 25204]
        if len(point) > 0:
            point[0][1] = json.dumps(point[0][1]['features'][0]['geometry'])
    if object.get('object_id') == 30:
        if not validate_geometry_permission(user):
            raise Exception(2, 'Нет прав на изменение геометрии')
        location = [item for item in data if item[0] == 30304]
        if len(location) > 0:
            geometry = {"type": "GeometryCollection", "geometries": []}
            for feature in location[0][1]['features']:
                geometry['geometries'].append(feature['geometry'])
            location[0][1] = json.dumps(geometry)
        parent = [item for item in data if item[0] == 30302]
        if len(parent) > 0:
            parent[0][1] = str(get_geometry_id_by_name(parent[0][1]))


def add_data(user, group_id, object):
    """
    Функция для добавления(слияния) информации в базу данных
    @param user: объект пользователя
    @param group_id: идентификационный номер группы пользователя
    @param object: вносимая информация в формате {object_id, rec_id, params:[{id,val,date},...,{}]}
    @return: идентификатор нового/измененного объекта в базе данных
    """
    try:
        data = [
            [param['id'], param['value'], param.get('date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + ':00']
            for param in object['params'] if validate_record(param)]
    except Exception as e:
        raise e
    # костыль для добавления классификатора телефона для страны, придумать как переделать-------------------------------
    additional_processing(user, object, data)
    # ------------------------------------------------------------------------------------------------------------------
    if not object.get('force', False):  # проверка на дублирование
        temp_set = None
        for item in data:
            if get_key_by_id(int(item[0])).get('need', 0) == 1:
                if type(temp_set) == set:
                    temp_set.intersection_update(set(find_key_value_http(object.get('object_id'), item[0], item[1])))
                else:
                    temp_set = set(find_key_value_http(object.get('object_id'), item[0], item[1]))
        if temp_set and len(temp_set) == len(
                [item for item in get_keys_by_object(object.get('object_id')) if item['need'] == 1]):
            return {'objects': [get_object_record_by_id_http(object.get('object_id'), item, group_id)
                                for item in temp_set]}
    if object.get('rec_id_old', 0) != 0:  # действия при слиянии объектов
        old_object = get_object_record_by_id_http(object.get('object_id'), object.get('rec_id_old'), group_id)
        for param in old_object['params']:
            for value in param['values']:
                data.append([param['id'], value['value'], value['date']])
        add_rel_by_other_object(group_id, object.get('object_id', 0), object.get('rec_id', 0),
                                object.get('object_id', 0), object.get('rec_id_old', 0))
    if len(data) == 0:  # проверка на пустой запрос
        return {'object': object.get('rec_id', 0)}
    if object.get('rec_id', 0) != 0:  # проверка на внесение новой записи
        data.append(['id', object.get('rec_id')])
    result = add_record(group_id=group_id, object_id=object.get('object_id'), object_info=data)
    if result != -1:
        return {'object': result}
    else:
        return {'result': -1}


def add_geometry(user, group_id, rec_id, location, name, parent_id, icon):
    """
    Функция для добавления геометрии
    @param user: объект пользователя
    @param group_id: идентификатор группы пользователя
    @param rec_id: идентификатор добавляемой геометрии, если новая, то 0
    @param location: feature collection содержащая информацию о вносимой геометрии
    @param name: имя новой геометрии
    @param parent_id: идентификатор родительской папки
    @param icon: название иконки геометрии
    @return: словарь содержащий информацию о геометрии
    """
    date_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    data = []
    if location:
        data.append({'id': 30304, 'value': location, 'date': date_time_str})
    if name:
        data.append({'id': 30303, 'value': str(name), 'date': date_time_str})
    if parent_id:
        data.append({'id': 30302, 'value': get_geometry_by_id(int(parent_id))['name'], 'date': date_time_str})
    if icon:
        data.append({'id': 30301, 'value': str(icon), 'date': date_time_str})
    return add_data(user, group_id, {'object_id': 30, 'rec_id': rec_id, 'params': data})
