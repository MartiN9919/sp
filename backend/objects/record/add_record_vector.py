import os
import shutil
import threading
import datetime

from core.projectSettings.constant import MEDIA_ROOT
from data_base_driver.additional_functions import date_client_to_server, date_time_client_to_server
from data_base_driver.constants.const_dat import DAT_SYS_KEY
from data_base_driver.input_output.input_output import io_get_obj
from data_base_driver.sys_key.get_key_info import get_key_by_id
from data_base_driver.sys_key.get_object_info import get_object_new_rec_id
from files.additional_function import get_object_file_path
from objects.record.add_record import add_record
from objects.record.get_record import get_keys, get_object_record_by_id_http


def find_key_value_http_vector(object_id, key_id, value, group_id=0):
    if get_key_by_id(key_id)['type'] == 'date' or get_key_by_id(key_id)['type'] == 'date_time':
        value = str(value).replace('-', '<<')
    else:
        value = str(value)
    response = io_get_obj(group_id, object_id, [], [], 500, '@key_id ' + str(key_id) + ' @val ' + value, {})
    return [int(item['rec_id']) for index, item in enumerate(response)]


def find_duplicate_vector(group_id, object_id, rec_id, params):
    nums = len(list(filter(lambda x: x['obj_id'] == object_id and x['need'], get_keys())))
    new_params = {}
    for param in params:
        key = get_key_by_id(param[0])
        if key['need']:
            new_params[param[0]] = {'value': param[1], 'date': param[2]}
    if nums > len(new_params) or len([item for item in params if item[0] > 1 and get_key_by_id(item[0]).get('need',0) == 1]) == 0:  # костыль для вектора
        return []
    values = [find_key_value_http_vector(object_id, param, new_params[param]['value'], group_id) for param in new_params]
    if len(values) == 0:
        return []
    result = set(values[0])
    for item in values[1:]:
        result.intersection_update(set(item))
    return list(result)


def parse_value_vector(param):
    """
    Функция для приведения некоторых параметров в правильному виду
    @param param: параметр заносимый в базу данных
    @param object: объект для которого создается новая запись
    @param files: файлы которые возможно несет в себе запись
    @return: список содержащий информацию о параметре в формате  [id, val, datetime]
    """
    value = param['value']
    key = get_key_by_id(param['id'])
    if key.get('type') == DAT_SYS_KEY.TYPE_DATA:
        value = date_client_to_server(value)
    if key.get('type') == DAT_SYS_KEY.TYPE_DATATIME:
        value = date_time_client_to_server(value)
    if key.get('type') == DAT_SYS_KEY.TYPE_STR or key.get('type') == DAT_SYS_KEY.TYPE_STR_ENG:
        value = value.replace('\\', '\\\\')
    return [param['id'], value,
            date_time_client_to_server(param.get('date', datetime.datetime.now().strftime("%d.%m.%Y %H:%M")) + ':00')]


def set_file(rec_id: int, object_id: int, data: list, files_path: str):
    for item in data:
        key = get_key_by_id(item[0])
        if key.get('type') == DAT_SYS_KEY.TYPE_FILE_PHOTO or key.get('type') == DAT_SYS_KEY.TYPE_FILE_ANY or key.get('id') == 1:
            rec_id = get_object_new_rec_id(object_id) if rec_id == 0 else rec_id
            target_path = get_object_file_path(object_id, rec_id, item[1])
            target_dir = '/'.join(target_path.split('/')[:-1])
            if not os.path.exists(MEDIA_ROOT + target_dir):
                os.makedirs(MEDIA_ROOT + target_dir, exist_ok=True)
            path = shutil.copyfile(files_path + '/' + item[1], MEDIA_ROOT + target_path)
            print(f"new file path {path}")


lock = threading.Lock()
duplicates_reports = []


def add_data_vector(group_id, object, files_path):
    """
    Функция для добавления(слияния) информации в базу данных
    @param user: объект пользователя
    @param group_id: идентификационный номер группы пользователя
    @param object: вносимая информация в формате {object_id, rec_id, params:[{id,value,date},...,{}]}
    @return: идентификатор нового/измененного объекта в базе данных
    """
    with lock:
        data = [parse_value_vector(param) for param in object['params']]
        duplicates = find_duplicate_vector(group_id, object.get('object_id'), object.get('rec_id'), data)
        if len(duplicates) > 0:
            report = f"same object: {object.get('object_id')}_{duplicates[0]} vector_object: {object['old_id']}"
            print(report)
            duplicates_reports.append(report)
            object['rec_id'] = duplicates[0]
            # old_object = get_object_record_by_id_http(object['object_id'], duplicates[0], group_id)
            # old_object_params = old_object['params']
            # new_data = []
            # for item in data:
            #     old_param = old_object_params.get([item[0]])
            #     if old_param and get_key_by_id(item[0])['need'] != 1:
            #         if item[1] not in [value['value'] for value in old_param['values']]:
            #             new_data.append(item)
            # data = new_data
            data = [item for item in data if get_key_by_id(item[0])['need'] != 1]
        set_file(object.get('rec_id', 0), object.get('object_id'), data, files_path)
        if object.get('rec_id', 0) != 0:  # проверка на внесение новой записи
            data.append(['id', object.get('rec_id')])
        result = add_record(group_id=group_id, object_id=object.get('object_id'), object_info=data)
        if result != -1:
            return {'object': result}
        else:
            return {'result': -1}
