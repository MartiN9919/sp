from data_base_driver.additional_functions import get_date_time_from_sec, get_title
from data_base_driver.input_output.input_output import io_get_obj_manticore_dict
from data_base_driver.sys_key.get_key_dump import get_key_by_id


def get_object_record_by_id_http(object_id, rec_id, group_id=0):
    """
    Функция для получения информации о объекте по его типу и идентификатору записи
    @param object_id: тип объекта
    @param rec_id: идентификатору записи
    @param group_id: идентификатору группы пользователя
    @return: словарь в формате {object_id, rec_id, params:[{id,val},...,{}]}
    """
    response = io_get_obj_manticore_dict(group_id, object_id, [], [rec_id], 500, '')
    temp = [(int(item['key_id']), item['val'], int(item['sec'])) for item in response]
    params = []
    for item in temp:
        keys = [key for key in params if key['id'] == int(item[0])]
        if len(keys) > 0:
            for key in keys:
                key['values'].append({'value': item[1], 'date': get_date_time_from_sec(item[2])})
            continue
        params.append({'id': int(item[0]), 'values': [{'value': item[1], 'date': get_date_time_from_sec(item[2])}]})
    for item in params:
        item['values'].sort(key=lambda x: x['date'], reverse=True)
    params.sort(key=lambda x: get_key_by_id(x['id'])['title'], reverse=True)
    params.sort(key=lambda x: get_key_by_id(x['id'])['need'], reverse=True)
    return {'object_id': object_id, 'rec_id': rec_id, 'params': params}


def get_record_title(object_id, rec_id, group_id=0):
    """
    Функция для получения строки с краткой информацией о объекте
    @param object_id: тип объекта
    @param rec_id: идентификатору записи
    @param group_id: идентификатору группы пользователя
    @return: словарь в формате {object_id, rec_id, title},...,{}]}
    """
    record = get_object_record_by_id_http(object_id, rec_id, group_id)
    title = get_title(record['params'])
    return {'object_id': record['object_id'], 'rec_id': record['rec_id'], 'title': title}


