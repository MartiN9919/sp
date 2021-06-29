from data_base_driver.connect.connect_manticore import db_shinxql
from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.full_text_search.additional_functions import get_date_from_days_sec


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


def get_object_record_by_id(object_id, rec_id):
    """
    Функция для получения информации о объекте по его типу и идентификатору записи
    @param object_type: тип объекта
    @param rec_id: идентификатору записи
    @return: словарь в формате {object_id, rec_id, params:[{id,val},...,{}]}
    """
    sql = 'SELECT key_id, val, date, sec FROM obj_' + FullTextSearch.TABLES[object_id] + '_row WHERE id = ' + \
          str(rec_id) + ';'
    params = [{'id': int(item[0]), 'val': item[1], 'date': get_date_from_days_sec(int(item[2]), int(item[3]))} for item
              in db_shinxql(sql)]
    return {'object_id': object_id, 'rec_id': rec_id, 'params': params}


