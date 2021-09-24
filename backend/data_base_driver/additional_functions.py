import datetime


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