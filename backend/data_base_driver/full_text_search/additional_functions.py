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