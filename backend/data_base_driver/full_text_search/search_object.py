import datetime
from copy import copy

from data_base_driver.connect.connect_manticore import db_shinxql
from data_base_driver.constants.full_text_search import Full_text_search
from data_base_driver.full_text_search.search_rel import search_rel


def find_reliable(object_type, request):
    """
    Функция для поиска значений в таблице object, возвращает результат только при полном совпадении
    @param object_type: тип объекта по которым идет поиск
    @param request: искомые параметры
    @return: список id объектов с искомыми параметрами, если не найдено, то пустой список
    """

    request = request.split(' ')
    result = None
    for word in request:
        fetchall = db_shinxql('SELECT id FROM obj_' + object_type + '_row WHERE MATCH(\'' + word + '\')')
        if result == None:
            result = set(fetchall)
        else:
            result.intersection_update(set(fetchall))
    return [item[0] for item in list(result)]


def find_unreliable(object_type, request):
    """
    Функция для поиска значений в таблице object, возвращает наиболее похожие результаты
    @param object_type: тип объекта по которым идет поиск
    @param request: искомые параметры
    @return: список id объектов с искомыми параметрами, если подобных нет, то пустой список
    """
    request = request.replace(' ', '|')
    result = db_shinxql('SELECT id FROM obj_' + object_type + '_row WHERE MATCH(\'' + request + '\')')
    return [item[0] for item in result]


def find_datetime(request, date_time=None, mode=0):
    data_time_request = ';'
    if date_time:
        days = date_time.toordinal() + 365
        seconds = int(datetime.timedelta(hours=date_time.time().hour, minutes=date_time.time().minute,
                                         seconds=date_time.time().second).total_seconds())
        if mode == 0:
            mode = '='
        if mode == 1:
            mode = '>'
        if mode == 2:
            mode = '<'
        data_time_request = ' AND date ' + mode + ' ' + str(days) + ';'


def get_sorted_list(items):
    counter = {}
    for item in items:
        try:
            counter[item] += 1
        except KeyError:
            counter[item] = 1

    return [item[0] for item in sorted(counter.items(), key=lambda x: x[1], reverse=True)]


def find_with_rel(object_type, request):
    temp_result = []
    result = []
    temp_result.append([object_type, find_unreliable(Full_text_search.TABLES[object_type], request)])
    for table in Full_text_search.TABLES:
        if table == object_type:
            continue
        temp_result.append([table, find_unreliable(Full_text_search.TABLES[table], request)])

    iter_res = iter(temp_result)
    for item in iter_res:
        for item_next in iter_res:
            for rec_id in item[1]:
                for rec_id_second in item_next[1]:
                    res = search_rel(item[0], rec_id, item_next[0], rec_id_second)
                    if len(res) != 0:
                        result.append(rec_id)
    if len(result) != 0:
        return get_sorted_list(result)
    else:
        result = find_reliable(Full_text_search.TABLES[object_type], request)
        if len(result) != 0:
            return result
        else:
            return find_unreliable(Full_text_search.TABLES[object_type], request)

# print(find_with_rel(45, 'Описание 3 tv2'))

