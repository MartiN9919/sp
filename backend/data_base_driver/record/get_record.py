from data_base_driver.additional_functions import get_date_time_from_sec
from data_base_driver.input_output.io import io_get_obj_manticore_dict
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
                if key['date'] > get_date_time_from_sec(item[2]):
                    key['old'].append({'value': item[1], 'date': get_date_time_from_sec(item[2])})
                else:
                    key['old'].append({'value': key['value'], 'date': key['date']})
                    key['value'] = item[1]
                    key['date'] = get_date_time_from_sec(int(item[2]))
            continue
        params.append({'id': int(item[0]), 'value': item[1], 'date': get_date_time_from_sec(item[2]),
                       'old': []})
    for item in params:
        item['old'].sort(key=lambda x: x['date'], reverse=True)
    params.sort(key=lambda x: get_key_by_id(x['id'])['title'], reverse=True)
    params.sort(key=lambda x: get_key_by_id(x['id'])['need'], reverse=True)
    title_list = []
    for param in params:
        key = get_key_by_id(param['id'])
        if key['priority']:
            title_list.append({'title': key['title'],
                               'priority': key['priority'],
                               'value': param['value']})
    title_list.sort(key=lambda x: x['priority'])
    if len(title_list) == 0:
        title = ', '.join(str(get_key_by_id(param['id'])['title'] + ': ' + param['value']) for param in params)
    else:
        title = ', '.join(str(title['title'] + ': ' + title['value']) for title in title_list)
    if len(title_list) < 3:
        sub_title = ', '.join(str(get_key_by_id(param['id'])['title'] + ': ' + param['value']) for param in
                              [param for param in params
                               if not get_key_by_id(param['id'])['priority']][:(3 - len(title_list))])
        title += ', ' + sub_title
    return {'object_id': object_id, 'rec_id': rec_id, 'params': params, 'title': title}
