import os
import shutil
import threading
import datetime

from core.deploy_settings import MEDIA_ROOT
from data_base_driver.additional_functions import date_client_to_server, date_time_client_to_server
from data_base_driver.constants.const_dat import DAT_SYS_KEY
from data_base_driver.sys_key.get_key_dump import get_key_by_id
from data_base_driver.sys_key.get_object_info import get_object_new_rec_id
from objects.record.add_record import add_record
from objects.record.find_object import find_duplicate_objects


def parse_value_vector(param, object, files_path):
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
    if key.get('type') == DAT_SYS_KEY.TYPE_FILE_PHOTO or key.get('type') == DAT_SYS_KEY.TYPE_FILE_ANY:
        rec_id = get_object_new_rec_id(object['object_id']) if object['rec_id'] == 0 else object['rec_id'] # баг при последующем слиянии
        target_path = 'files/' + str(object['object_id']) + '/' + str(rec_id) + '/'
        if not os.path.exists(MEDIA_ROOT + '/' + target_path):
            os.makedirs(MEDIA_ROOT + '/' + target_path, exist_ok=True)
        shutil.copyfile(files_path + '/' + value, MEDIA_ROOT + '/' + target_path + value)
    return [param['id'], value,
            date_time_client_to_server(param.get('date', datetime.datetime.now().strftime("%d.%m.%Y %H:%M")) + ':00')]


lock = threading.Lock()


def add_data_vector(group_id, object, files_path):
    """
    Функция для добавления(слияния) информации в базу данных
    @param user: объект пользователя
    @param group_id: идентификационный номер группы пользователя
    @param object: вносимая информация в формате {object_id, rec_id, params:[{id,value,date},...,{}]}
    @return: идентификатор нового/измененного объекта в базе данных
    """
    with lock:
        data = [parse_value_vector(param, object, files_path) for param in object['params']]
        duplicates = find_duplicate_objects(group_id, object.get('object_id'), object.get('rec_id'), data)
        if len(duplicates) > 0:
            object['rec_id'] = duplicates[0]
            data = [item for item in data if get_key_by_id(item[0])['need'] != 1] # не сработает из-за 0 и 1 id?
        if object.get('rec_id', 0) != 0:  # проверка на внесение новой записи
            data.append(['id', object.get('rec_id')])
        result = add_record(group_id=group_id, object_id=object.get('object_id'), object_info=data)
        if result != -1:
            return {'object': result}
        else:
            return {'result': -1}

