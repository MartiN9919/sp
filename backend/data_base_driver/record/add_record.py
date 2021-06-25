import datetime

from data_base_driver.full_text_search.search_key_params import find_key_value
from data_base_driver.full_text_search.search_object import get_object_record_by_id
from data_base_driver.input_output.io import io_set
from data_base_driver.sys_key.get_key_dump import get_key_by_id


def add_record(group_id, object_id, object_info):
    """
    функция для добавления объекта в базу данных
    @param group_id: идентификационный номер группы пользователя
    @param object_id: идентификационный номер типа объекта
    @param object_info: информация об объекте в формате [[key:value],[],...,[]]
    для добавления информации о уже существующем объекте необходимо в качестве ключа передать id,
    а в качестве значение точный идентификационный номер объекта
    @return:
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
    data = [[param['id'], param['val'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            for param in object['params']]
    if object.get('rec_id', 0) != 0:
        data.append(['id', object.get('rec_id')])
    else:
        temp_set = None
        for item in data:
            if get_key_by_id(int(item[0])).get('need', 0) == 1:
                if temp_set:
                    temp_set.intersection_update(set(find_key_value(object.get('object_id'), item[0], item[1])))
                else:
                    temp_set = set(find_key_value(object.get('object_id'), item[0], item[1]))
        if len(temp_set) != 0:
            return {'status': 2, 'objects': [get_object_record_by_id(item) for item in temp_set]}
    result = add_record(group_id=group_id, object_id=object.get('object_id'), object_info=data)
    if result != -1:
        return {'status': 1,
                'rec_id': result}
    else:
        return {'status': -1}



