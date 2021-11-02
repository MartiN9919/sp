import datetime

from data_base_driver.sys_key.get_key_dump import get_key_by_name, get_obj_id


def get_document_date_format(date):
    """
    Функция для преобразования строки даты из формата 2020-01-01 в 01.01.2020
    @param date: строка содержащая дату в формате 2020-01-01
    @return: строка содержащая дату в формате 01.01.2020
    """
    return '.'.join(reversed(date.split('-')))


def get_date_from_days_sec(days, sec):
    """
    Функция для получения даты и времени в строковом формате из дней с рождества христова и секунд с начала дня
    @param days: количество дней с прошедших с рождества христова
    @param sec: количество секунд прошедших с начала дня
    @return: строка содержащую дату и время в формате Y-m-d H:M:S
    """
    if days == 0 and sec == 0:
        return 'unknow'
    elif sec == 0:
        h, m, s = 0, 0, 0
    else:
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec - h * 3600 - m * 60
    return datetime.datetime.fromordinal(days - 365).replace(hour=h, minute=m, second=s).strftime("%Y-%m-%d %H:%M:%S")


def get_date_time_from_sec(sec):
    """
    Функция для получения даты и времени в строковом формате из секунд с рождества христова
    @param sec: количество секунд прошедших с рождества христова
    @return: строка содержащую дату и время в формате Y-m-d H:M:S
    """
    days = sec // 86400
    sec = sec % 86400
    return get_date_from_days_sec(days, sec)


def get_sorted_list(items):
    """
    Функция для сортировки списка по количеству вхождений элемента
    @param items: список с числовыми элементами
    @return: список отсортированный в порядке количества вхождений элементов
    """
    counter = {}
    for item in items:
        try:
            counter[item] += 1
        except KeyError:
            counter[item] = 1
    return [item[0] for item in sorted(counter.items(), key=lambda x: x[1], reverse=True)]


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


def intercept_sort_list(elements):
    """
    Функция для пересечения списков с сохранением сортировки
    @param elements: список содержащий списки целых чисел
    @return: список целых чисел встреченных во всех начальных списков с сохранением их сортировки
    """
    if len(elements) == 1:
        return elements[0]
    temp_list = []
    for elem in elements[0]:
        temp = {'elem': elem, 'pos': []}
        for item in elements:
            if not elem in item:
                temp['pos'] = []
                break
            else:
                temp['pos'].append(item.index(elem))
        if len(temp['pos']) > 0:
            temp['midle'] = sum(temp['pos']) / len(temp['pos'])
            temp_list.append(temp)
        else:
            continue
    temp_list.sort(key=lambda x: x['midle'])
    return [temp['elem'] for temp in temp_list]


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
    if key == 'id':
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
            obj = get_obj_id(obj) if isinstance(obj, str) and not (obj.isdigit()) else int(obj)
            if obj != 1:
                data = [(get_id_by_key(item[0]), item[1], item[2]) for item in data]
            else:
                data = data
            return function(group_id, obj, data)
        except Exception as e:
            raise e

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def io_get_object_wrap(function):
    """
    Обертка для упрощения функции
    """
    def wrap(group_id, object, keys, ids, ids_max_block, where_dop_row, time_interval):
        try:
            keys = [get_id_by_key(item) for item in keys]
            object = get_obj_id(object) if isinstance(object, str) and not (object.isdigit()) else int(object)
            return function(group_id, object, keys, ids, ids_max_block, where_dop_row, time_interval)
        except Exception as e:
            raise e

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def io_get_rel_wrap(function):
    """
    Обертка для упрощения функции
    """
    def wrap(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique, rec_id=0):
        try:
            keys = [get_id_by_key(item) for item in keys]
            if obj_rel_1 and len(obj_rel_1) > 0:
                obj_rel_1[0] = get_obj_id(obj_rel_1[0]) if isinstance(obj_rel_1[0], str) and not (
                    obj_rel_1[0].isdigit()) else int(obj_rel_1[0])
            if obj_rel_2 and len(obj_rel_2) > 0:
                obj_rel_2[0] = get_obj_id(obj_rel_2[0]) if isinstance(obj_rel_2[0], str) and not (
                    obj_rel_2[0].isdigit()) else int(obj_rel_2[0])
            return function(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique, rec_id)
        except Exception as e:
            raise e

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
