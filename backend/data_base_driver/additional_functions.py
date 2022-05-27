import datetime

from data_base_driver.sys_key.get_object_info import get_object_id
from data_base_driver.sys_key.get_key_info import get_key_by_name


def get_date_from_days_sec(days, sec, client=False):
    """
    Функция для получения даты и времени в строковом формате из дней с рождества христова и секунд с начала дня
    @param days: количество дней с прошедших с рождества христова
    @param sec: количество секунд прошедших с начала дня
    @param client: клиентский формат даты, если True то d/m/Y
    @return: строка содержащую дату и время в формате Y-m-d H:M:S
    """
    if days == 0 and sec == 0:
        return '0001-01-01 12:00:00'
    elif sec == 0:
        h, m, s = 0, 0, 0
    else:
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec - h * 3600 - m * 60
    if client:
        return datetime.datetime.fromordinal(days - 365).replace(hour=h, minute=m, second=s).strftime(
            "%d-%m-%Y %H:%M:%S")
    else:
        return datetime.datetime.fromordinal(days - 365).replace(hour=h, minute=m, second=s).strftime(
            "%Y-%m-%d %H:%M:%S")


def get_date_time_from_sec(sec, client=False):
    """
    Функция для получения даты и времени в строковом формате из секунд с рождества христова
    @param sec: количество секунд прошедших с рождества христова
    @param client: клиентский формат даты, если True то d/m/Y
    @return: строка содержащую дату и время в формате Y-m-d H:M:S
    """
    days = sec // 86400
    sec = sec % 86400
    return get_date_from_days_sec(days, sec, client)


def date_time_to_sec(date_time):
    """
    Функция для преобразования даты и времени в секунды
    @param date_time: дата и время в формате python datetime.datetime
    @return: целочисленное количество секунд
    """
    days = date_time.date().toordinal() + 365
    return date_time.time().second + date_time.time().minute * 60 + date_time.time().hour * 3600 + days * 86400


def str_to_sec(date_time_str):
    return date_time_to_sec(datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S"))


def date_client_to_server(date_str):
    return '-'.join(reversed(date_str.split('.'))) if date_str else None


def date_time_client_to_server(date_time_str):
    return date_client_to_server(date_time_str.split(' ')[0]) + ' ' + date_time_str.split(' ')[1] if date_time_str else None


def date_server_to_client(date_str):
    return '.'.join(reversed(date_str.split('-'))) if date_str else None


def date_time_server_to_client(date_time_str, sep=' '):
    return date_server_to_client(date_time_str.split(' ')[0]) + sep + date_time_str.split(' ')[1] if date_time_str else None


def push_dict(dictionary, key, value):
    """
    Функция для добавления в список по ключу словаря, если ключа нет то создает список с одним значением
    @param dictionary: исходный словарь
    @param key: ключ словаря
    @param value: вносимое значение
    """
    if dictionary.get(key, None):
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def get_second_range(date_start, date_end):
    """
    Функция для получения диапазона времени в секундах
    @param date_start: стартовая дата в строковом формате гг.мм.дд
    @param date_end: дата окончания гг.мм.дд
    @return: словарь в формате {second_start, second_end}
    """
    date_time_start = date_start + ' 00:00:00'
    date_time_end = date_end + ' 00:00:00'
    return {'second_start': str_to_sec(date_time_start), 'second_end': str_to_sec(date_time_end)}


def get_id_by_key(key):
    if isinstance(key, str) and key == 'id':
        return key
    if isinstance(key, str) and not (key.isdigit()):
        return get_key_by_name(key)['id']
    else:
        return key


def io_set_wrap(function):
    """
    Обертка для упрощения функции
    """
    def wrap(group_id, obj, data):
        try:
            obj = get_object_id(obj) if isinstance(obj, str) and not (obj.isdigit()) else int(obj)
            if obj != 1:
                data = [(get_id_by_key(item[0]), item[1], item[2]) if item[0] != 'id' else (item[0], item[1])
                        for item in data]
            else:
                data = data
            return function(group_id, obj, data)
        except Exception as e:
            raise e

    return wrap


def io_get_object_wrap(function):
    """
    Обертка для упрощения функции
    """
    def wrap(group_id, object, keys, ids, ids_max_block, where_dop_row, time_interval):
        try:
            keys = [get_id_by_key(item) for item in keys]
            object = get_object_id(object) if isinstance(object, str) and not (object.isdigit()) else int(object)
            return function(group_id, object, keys, ids, ids_max_block, where_dop_row, time_interval)
        except Exception as e:
            raise e

    return wrap


def io_get_rel_wrap(function):
    """
    Обертка для упрощения функции
    """
    def wrap(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique, rec_id=0):
        try:
            keys = [get_id_by_key(item) for item in keys]
            if obj_rel_1 and len(obj_rel_1) > 0:
                obj_rel_1[0] = get_object_id(obj_rel_1[0]) if isinstance(obj_rel_1[0], str) and not (
                    obj_rel_1[0].isdigit()) else int(obj_rel_1[0])
            if obj_rel_2 and len(obj_rel_2) > 0:
                obj_rel_2[0] = get_object_id(obj_rel_2[0]) if isinstance(obj_rel_2[0], str) and not (
                    obj_rel_2[0].isdigit()) else int(obj_rel_2[0])
            return function(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique, rec_id)
        except Exception as e:
            raise e

    return wrap


def parse_type(key_type, list_id=None, object_id=None):
    """
    Функция для преобразования формата типа
    @param key_type: название типа в базе данных
    @param list_id: идентификатор списка если есть
    @param object_id: идентификатор типа искомого объекта если есть
    @return: тип в формате {title, value}
    """
    if list_id:
        return {'title': 'list', 'value': list_id}
    elif key_type == 'search':
        return {'title': 'search', 'value': object_id}
    elif key_type == 'text_eng':
        return {'title': 'text', 'value': 'eng'}
    elif key_type == 'text_ru':
        return {'title': 'text', 'value': 'ru'}
    elif key_type == 'date':
        return {'title': 'date', 'value': 'date'}
    elif key_type == 'datetime':
        return {'title': 'date', 'value': 'datetime'}
    elif key_type == 'geometry':
        return {'title': 'geometry', 'value': 'polygon'}
    elif key_type == 'geometry_point':
        return {'title': 'geometry', 'value': 'point'}
    elif key_type == 'file_any':
        return {'title': 'file', 'value': 'any'}
    elif key_type == 'file_photo':
        return {'title': 'file', 'value': 'photo'}
    return {'title': key_type, 'value': None}
