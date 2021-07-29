import datetime

from data_base_driver.record.find_object import find_key_value_http
from data_base_driver.record.get_record import get_object_record_by_id_http
from data_base_driver.input_output.io import io_set
from data_base_driver.record.validate_record import validate_record, get_country_by_number, remove_special_chars
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


def add_data(group_id, object):
    """
    Функция для добавления информации в базу данных
    @param group_id: идентификационный номер группы пользователя
    @param object: вносимая информация в формате {object_id, rec_id, params:[{id,val},...,{}]}
    @return: идентификатор нового/измененного объекта в базе данных
    """
    try:
        data = [[param['id'], param['value'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                for param in object['params'] if validate_record(param)]
    except Exception as e:
        raise e
    # костыль для добавления классификатора телефона для страны, придумать как переделать-------------------------------
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
    # ------------------------------------------------------------------------------------------------------------------
    if len(data) == 0: # проверка на пустой запрос
        return {'status': 1,
                'object': get_object_record_by_id_http(object.get('object_id'), object.get('rec_id', 0))}
    if object.get('rec_id', 0) != 0: # проверка на внесение новой записи
        data.append(['id', object.get('rec_id')])

    elif not object.get('force', False): # проверка на дублирование
        temp_set = None
        for item in data:
            if get_key_by_id(int(item[0])).get('need', 0) == 1:
                if type(temp_set) == set:
                    temp_set.intersection_update(set(find_key_value_http(object.get('object_id'), item[0], item[1])))
                else:
                    temp_set = set(find_key_value_http(object.get('object_id'), item[0], item[1]))
        if len(temp_set) != 0:
            return {'status': 2, 'objects': [get_object_record_by_id_http(object.get('object_id'), item) for item in temp_set]}
    result = add_record(group_id=group_id, object_id=object.get('object_id'), object_info=data)
    if result != -1:
        return {'status': 1,
                'object': get_object_record_by_id_http(object.get('object_id'), result)}
    else:
        return {'status': -1}



