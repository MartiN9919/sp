from data_base_driver.additional_functions import get_date_time_from_sec, get_title
from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_OWNER
from data_base_driver.input_output.input_output import io_get_obj
from data_base_driver.sys_key.get_key_dump import get_key_by_id


def get_object_record_by_id_http(object_id, rec_id, group_id=0):
    """
    Функция для получения информации о объекте по его типу и идентификатору записи
    @param object_id: тип объекта
    @param rec_id: идентификатору записи
    @param group_id: идентификатору группы пользователя
    @return: словарь в формате {object_id, rec_id, params:[{id,val},...,{}]}
    """
    response = io_get_obj(group_id, object_id, [], [rec_id], 500, '', {})
    temp = [(int(item['key_id']), item['val'], int(item['sec'])) for item in response
            if int(item['key_id']) not in DAT_SYS_KEY.DUMP.owners.get(object_id, [])]
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
    permission = get_permission_params(response, object_id)
    return {'object_id': object_id, 'rec_id': rec_id, 'params': params, 'permission': permission}


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


def get_permission_params(params, object_id):
    """
    Функция для получения словаря разрешений для данного объекта
    @param params: список записей о объекте
    @param object_id: идентификатор типа объекта
    @return: словарь в формате {permission_type:{id,groups:[]}, ..., {}}
    """
    if object_id not in DAT_SYS_KEY.DUMP.owners.keys():
        return {}
    keys_validation_tuple = DAT_SYS_KEY.DUMP.owners[object_id]
    permission = {keys_validation_tuple[0]: {'title': 'разрешение на запись', 'groups': []},
                  keys_validation_tuple[1]: {'title': 'разрешение на чтение', 'groups': []},
                  keys_validation_tuple[2]: {'title': 'разрешение на чтение временно', 'groups': []},
                  keys_validation_tuple[3]: {'title': 'запрет', 'groups': []}}
    for param in params:
        if int(param['key_id']) in keys_validation_tuple:
            permission[int(param['key_id'])]['groups'].append({
                'group_id': int(param['val']),
                'group_title': DAT_OWNER.DUMP.get_group_title(int(param['val'])),
                'data_time': get_date_time_from_sec(param['sec'])
            })
    return permission
