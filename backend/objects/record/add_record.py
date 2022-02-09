import datetime
import json
import os
import threading

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from core.settings import MEDIA_ROOT
from data_base_driver.additional_functions import date_time_client_to_server, date_client_to_server
from data_base_driver.constants.const_dat import DAT_SYS_KEY
from data_base_driver.constants.const_key import SYS_KEY_CONSTANT
from objects.record.find_object import find_duplicate_objects
from objects.record.get_record import get_object_record_by_id_http
from data_base_driver.input_output.input_output import io_set
from data_base_driver.sys_key.get_key_dump import get_key_by_id
from data_base_driver.sys_key.get_list import get_item_list_value
from data_base_driver.sys_key.get_object_info import get_object_new_rec_id
from document_driver.document_reader import get_document_text
from objects.record.validate_record import get_country_by_number, remove_special_chars, validate_geometry_permission, \
    validate_record
from objects.relations.add_rel import add_rel_by_other_object


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
    if object.get('object_id') == SYS_KEY_CONSTANT.FILE_ID:
        if len([item for item in data if item[0] == SYS_KEY_CONSTANT.FILE_CLASSIFIER_ID]):
            rec_id = get_object_new_rec_id(object['object_id']) if object['rec_id'] == 0 else object['rec_id']
            path = MEDIA_ROOT + '/files/' + str(object['object_id']) + '/' + str(rec_id) + '/' +\
            [item for item in data if item[0] == SYS_KEY_CONSTANT.FILE_CLASSIFIER_ID][0][1]
            text = get_document_text(path)
            if text:
                data.append([SYS_KEY_CONSTANT.FILE_TEXT_CLASSIFIER_ID, text,
                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    if object.get('object_id') == SYS_KEY_CONSTANT.TELEFON_ID:
        country = get_country_by_number(
            [param for param in object['params'] if param['id'] == SYS_KEY_CONSTANT.PHONE_NUMBER_CLASSIFIER_ID][0][
                'value'])
        fl = 0
        for temp in data:
            if temp[0] == SYS_KEY_CONSTANT.PHONE_NUMBER_CLASSIFIER_ID:
                temp[1] = remove_special_chars(temp[1])
            if temp[0] == SYS_KEY_CONSTANT.PHONE_NUMBER_COUNTRY_ID:
                temp[1] = country
                fl = 1
        if fl == 0:
            data.append([SYS_KEY_CONSTANT.PHONE_NUMBER_COUNTRY_ID, country,
                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    # костыль для добавления геометрических объектов, придумать как переделать------------------------------------------
    if object.get('object_id') == SYS_KEY_CONSTANT.POINT_ID:
        point = [item for item in data if item[0] == SYS_KEY_CONSTANT.POINT_CLASSIFIER_ID]
        if len(point) > 0:
            point[0][1] = json.dumps(point[0][1]['features'][0]['geometry'])
    if object.get('object_id') == SYS_KEY_CONSTANT.GEOMETRY_ID:
        if not validate_geometry_permission(user):
            raise Exception(2, 'Нет прав на изменение геометрии')
        location = [item for item in data if item[0] == SYS_KEY_CONSTANT.GEOMETRY_CLASSIFIER_ID]
        if len(location) > 0:
            geometry = {"type": "GeometryCollection", "geometries": []}
            for feature in location[0][1]['features']:
                geometry['geometries'].append(feature['geometry'])
            location[0][1] = json.dumps(geometry)


def parse_value(param, object, files):
    """
    Функция для приведения некоторых параметров в правильному виду
    @param param: параметр заносимый в базу данных
    @param object: объект для которого создается новая запись
    @param files: файлы которые возможно несет в себе запись
    @return: список содержащий информацию о параметре в формате  [id, val, datetime]
    """
    value = param['value']
    key = get_key_by_id(param['id'])
    if key.get('list_id') != 0 and key['id'] not in SYS_KEY_CONSTANT.NOT_VALUE_TRANSFER_LIST and \
            key['id'] not in SYS_KEY_CONSTANT.GEOMETRY_TRANSFER_LIST and key.get('list_id') != None:
        value = str(get_item_list_value(value))
    if key.get('type') == DAT_SYS_KEY.TYPE_DATA:
        value = date_client_to_server(value)
    if key.get('type') == DAT_SYS_KEY.TYPE_DATATIME:
        value = date_time_client_to_server(value)
    if key.get('type') == DAT_SYS_KEY.TYPE_FILE_PHOTO or key.get('type') == DAT_SYS_KEY.TYPE_FILE_ANY:
        rec_id = get_object_new_rec_id(object['object_id']) if object['rec_id'] == 0 else object['rec_id']
        path = 'files/' + str(object['object_id']) + '/' + str(rec_id) + '/'
        if not os.path.exists(MEDIA_ROOT + '/' + path):
            os.makedirs(MEDIA_ROOT + '/' + path, exist_ok=True)
        file = files[value]
        file_path = default_storage.save(path + file.name, ContentFile(file.read()))
        value = file_path.split('/')[-1]
    return [param['id'], value,
            date_time_client_to_server(param.get('date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + ':00')]


# блокиратор потока для контроля что в один момент времени создается один объект
lock = threading.Lock()


def add_data(user, group_id, object, files=None):
    """
    Функция для добавления(слияния) информации в базу данных
    @param user: объект пользователя
    @param group_id: идентификационный номер группы пользователя
    @param object: вносимая информация в формате {object_id, rec_id, params:[{id,value,date},...,{}]}
    @return: идентификатор нового/измененного объекта в базе данных
    """
    with lock:
        try:
            data = [parse_value(param, object, files) for param in object['params'] if validate_record(param)]
        except Exception as e:
            raise e
        additional_processing(user, object, data)
        if not object.get('force', False):  # проверка на дублирование
            duplicates = find_duplicate_objects(group_id, object.get('object_id'), object.get('rec_id'), data)
            if len(duplicates) > 0:
                return {'objects': [get_object_record_by_id_http(object.get('object_id'), item, group_id)
                                    for item in duplicates]}
        if object.get('rec_id_old', 0) != 0:  # действия при слиянии объектов
            old_object = get_object_record_by_id_http(object.get('object_id'), object.get('rec_id_old'), group_id)
            for param in old_object['params']:
                for value in param['values']:
                    data.append([param['id'], value['value'], value['date'] + ':00'])
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
        data.append({'id': 30302, 'value': parent_id, 'date': date_time_str})
    if icon:
        temp_value = str(get_item_list_value(int(icon)))
        value = temp_value[temp_value.index('(') + 1:temp_value.index(')')]
        data.append({'id': 30301, 'value': str(value), 'date': date_time_str})
    return add_data(user, group_id, {'object_id': 30, 'rec_id': rec_id, 'params': data})
