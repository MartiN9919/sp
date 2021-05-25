import datetime

from data_base_driver.connect.connect_manticore import db_shinxql


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
