import datetime


def get_date_from_days_sec(days, sec):
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
    days = sec // 86400
    sec = sec % 86400
    return get_date_from_days_sec(days,sec)


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
