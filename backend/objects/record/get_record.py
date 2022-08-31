from data_base_driver.additional_functions import get_date_time_from_sec, date_server_to_client, \
    date_time_server_to_client, parse_type
from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_OWNER
from data_base_driver.constants.const_key import SYS_KEY_CONSTANT
from data_base_driver.input_output.input_output import io_get_obj
from data_base_driver.sys_key.get_key_info import get_key_by_id
from data_base_driver.sys_key.get_list import get_groups_list, get_item_list_value
from data_base_driver.trigger.trigger_execute import check_triggers


def get_title(params, title_len=3):
    """
    Функция для получения названия объекта по его параметрам
    @param params: row параметры объекта
    @param title_len: длинна названия
    @return: название составленное из параметров с учетом приоритета и длинны
    """
    title_list = []
    for param in params:
        key = get_key_by_id(param['id'])
        title_list.append({'title': key['title'],
                           'priority': key['priority'],
                           'value': param['values'][0]['value'],
                           'visible': key['visible']})
    title_list = [str(item['title'] + ': ' + item['value']) if item['visible'] == 'all' else item['value']
                  for item in sorted(title_list, key=lambda x: x['priority']) if item['visible'] != 'none']
    return ', '.join(title_list[:title_len])


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
    permission = {keys_validation_tuple[0]: [],
                  keys_validation_tuple[1]: [],
                  keys_validation_tuple[2]: [],
                  keys_validation_tuple[3]: []}
    for param in params:
        if int(param[0]) in keys_validation_tuple[:3]:
            permission[int(param[0])].append({
                'group_id': int(param[1]),
                'data_time': get_date_time_from_sec(param[2])
            })
    return permission


def get_record_title(object_id, rec_id, group_id=0, record=None, length=3, triggers=None):
    """
    Функция для получения строки с краткой информацией о объекте
    @param object_id: тип объекта
    @param rec_id: идентификатору записи
    @param group_id: идентификатору группы пользователя
    @param record: записи о объекте для формирования заголовка, по умолчанию None
    @param length: длинна названия, по умолчанию 3
    @param triggers: проверять ли триггеры у указанных объектов
    @return: словарь в формате {object_id, rec_id, title},...,{}]}
    """
    if record is None:
        record = get_object_record_by_id_http(object_id, rec_id, group_id, triggers=triggers)
    if len(list(record['permission'].keys())) > 0:
        write_groups = [item['group_id'] for item in record['permission'][list(record['permission'].keys())[0]]]
        write = DAT_OWNER.DUMP.valid_group(group_id, write_groups)
    else:
        write = True
    title = get_title(record['params'], length)
    triggers = record['triggers']
    return {'object_id': record['object_id'], 'rec_id': record['rec_id'], 'title': title, 'write': write,
            'triggers': triggers}


def get_record_photo(params):
    """
    Функция для получения фотографии объекта
    @param params: список параметров объекта
    @return: название файла фотографии или None если фото нет
    """
    photo_keys = []
    for param in params:
        key = get_key_by_id(param['id'])
        if key['type'] == 'file_photo':
            photo_keys.append({'priority': key['priority'], 'value': param['values'][0]['value']})
    photo_keys.sort(key=lambda x: x['priority'], reverse=True)
    if len(photo_keys):
        return photo_keys[0]['value']
    else:
        return None


def get_value_by_key(key, value):
    """
    Функция для преобразования значения в базе данных в значение для пользователя
    @param key: идентификатор классификатора
    @param value: значение классификатора
    @return: значение для пользователя
    """
    key_type = get_key_by_id(key)['type']
    if key_type == 'checkbox':
        value = 'Да' if value == '1' else 'Нет'
    if key_type == 'date':
        value = date_server_to_client(value)
    if key_type == 'datetime':
        value = date_time_server_to_client(value)
    if key == SYS_KEY_CONSTANT.PARENT_ID_CLASSIFIER_ID:
        if int(value) == 0:
            return 'корень'
        else:
            return get_item_list_value(int(value))
    elif key in SYS_KEY_CONSTANT.GEOMETRY_TRANSFER_LIST:
        temp_value = str(get_item_list_value(value))
        return temp_value[:temp_value.index('(') - 1]
    elif key in SYS_KEY_CONSTANT.NOT_VALUE_TRANSFER_LIST:
        return [item for item in get_groups_list() if item['id'] == int(value)][0]['value']
    return value


def get_object_info(object_id, rec_id, fetchall, group_id=0, triggers=None, title_mod=False):
    params = []
    for item in fetchall:
        try:
            value = get_value_by_key(int(item[0]), item[1])
        except IndexError:
            continue
        keys = [key for key in params if key['id'] == int(item[0])]
        if len(keys) > 0:
            keys[0]['values'].append({'value': value, 'date': get_date_time_from_sec(item[2])[:-3]})
        else:
            params.append(
                {'id': int(item[0]), 'values': [{'value': value, 'date': get_date_time_from_sec(item[2])[:-3]}]})
    for item in params:
        item['values'].sort(key=lambda x: x['date'], reverse=True)
        for value in item['values']:
            value['date'] = date_time_server_to_client(value['date'])
    params.sort(key=lambda x: x['id'])
    permission = get_permission_params(fetchall, object_id)
    if triggers:
        triggers = check_triggers(triggers, group_id, object_id, rec_id)
    else:
        triggers = []
    title = get_record_title(object_id, rec_id, group_id,
                             {'object_id': object_id, 'rec_id': rec_id, 'params': params, 'permission': permission,
                              'triggers': None}, 1 if not title_mod else 3)
    photo = get_record_photo(params)
    return {'object_id': object_id, 'rec_id': rec_id, 'params': params, 'permission': permission,
            'title': title['title'] if not title_mod else title, 'triggers': triggers, 'photo': photo}


def get_objects_records(group_id, object_id, rec_ids, triggers=None, title=False):
    response = io_get_obj(group_id, object_id, [], rec_ids, 20000, '', {})
    objects = {}
    for item in response:
        if objects.get(item['rec_id']) is None:
            objects[item['rec_id']] = []
        objects[item['rec_id']].append((int(item['key_id']), item['val'], int(item['sec'])))
    result = {}
    for rec_id in objects:
        result[rec_id] = get_object_info(object_id, rec_id, objects[rec_id], group_id, triggers, title)
    return result


def get_object_record_by_id_http(object_id, rec_id, group_id=0, triggers=None):
    """
    Функция для получения информации о объекте по его типу и идентификатору записи
    @param object_id: тип объекта
    @param rec_id: идентификатору записи
    @param group_id: идентификатору группы пользователя
    @param triggers: объект содержащий триггеры, если есть
    @return: словарь в формате {object_id, rec_id, params:[{id,values:[{value,date},...,{}],},...,{}]}
    """
    response = io_get_obj(group_id, object_id, [], [rec_id], 500, '', {})
    if len(response) == 0:
        return None
    temp = [(int(item['key_id']), item['val'], int(item['sec'])) for item in response]
    return get_object_info(object_id, rec_id, temp, group_id, triggers)


def get_keys():
    """
    Получение списка ключей классификатора
    @return: список словарей с информацией об искомых ключах
    """
    keys = DAT_SYS_KEY.DUMP.get_rec(only_first=False)
    result = []
    for key in keys:
        temp = dict(key)
        temp.pop('rel_obj_1_id')
        temp.pop('rel_obj_2_id')
        temp['type'] = parse_type(temp['type'], temp['list_id'])
        temp.pop('list_id')
        result.append(temp)
    result.sort(key=lambda x: x['title'])
    result.sort(key=lambda x: x['priority'])
    result.sort(key=lambda x: x['obj_id'])
    return result


def get_keys_blank():
    """
    Функция для получения классификаторов для бланков
    @return: список объектов содержащий классификаторы для бланков
    """
    keys = DAT_SYS_KEY.DUMP.get_rec(only_first=False)
    result = []
    for key in keys:
        temp = dict(key)
        temp.pop('rel_obj_1_id')
        temp.pop('rel_obj_2_id')
        temp['type'] = 'list' if temp.get('list_id') else temp['type']
        result.append(temp)
    result.sort(key=lambda x: x['id'])
    result.sort(key=lambda x: x['obj_id'])
    return result


def get_object_param_by_key(group_id, object_id, rec_id, key_id):
    """
    Функция для получения параметра объекта
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param key_id: идентификатор искомого параметра
    @return: наиболее актуальное значение искомого параметра если он есть, если нет - None
    """
    object_params = get_object_record_by_id_http(object_id, rec_id, group_id, None)['params']
    object_param_list = [item for item in object_params if item['id'] == key_id]
    return object_param_list[0]['values'][0]['value'] if len(object_param_list) > 0 else None
