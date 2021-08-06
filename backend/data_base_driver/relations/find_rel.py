import datetime

from data_base_driver.additional_functions import date_time_to_sec
from data_base_driver.input_output.input_output import io_get_rel
from data_base_driver.record.find_object import find_reliable_http


def get_seconds_from_request_data_time(date_time_start, date_time_end):
    if not date_time_start:
        date_time_1_str = '0001-01-01 00:00:00'
    else:
        date_time_1_str = date_time_start + ':00'
    if not date_time_end:
        date_time_2_str = datetime.datetime.now().isoformat(sep=' ')[:19]
    else:
        date_time_2_str = date_time_end + ':00'
    date_time_1 = datetime.datetime.strptime(date_time_1_str, "%Y-%m-%d %H:%M:%S")
    seconds_1 = date_time_to_sec(date_time_1)
    date_time_2 = datetime.datetime.strptime(date_time_2_str, "%Y-%m-%d %H:%M:%S")
    seconds_2 = date_time_to_sec(date_time_2)
    return seconds_1, seconds_2


def validate_rel_actual(rel, date_time_start, date_time_end, group_id=0):
    """
    Функция для проверки актуальности отдельной связи
    @param rel: словарь содержащий информацию о проверяемой связи
    @param date_time_start: дата и время начала выборки
    @param date_time_end: дата и время конца выборки
    @param group_id: идентификатор группы пользователя
    @return: False если связь не актуальна, True если актуальна
    """
    second_start, second_end = get_seconds_from_request_data_time(date_time_start, date_time_end)
    time_interval = {'second_start': second_start, 'second_end': second_end}
    response = io_get_rel(group_id, [int(rel['key_id'])], [int(rel['obj_id_1']), int(rel['rec_id_1'])],
                                         [int(rel['obj_id_2']), int(rel['rec_id_2'])], [], time_interval, True)
    for temp in response:
        if temp['sec'] < second_start or temp['sec'] > second_end or temp['sec'] == rel['sec']:
            continue
        if temp['sec'] > rel['sec']:
            return False
    return True


def search_rel_with_key_http(rel_key, object_1_type, object_1_id, object_2_type, object_2_id, list_id,
                             date_time_start, date_time_end, group_id=0):
    """
    Функция для поиска связей между двумя конкретными объектами
    @param rel_key: тип связи
    @param object_1_type: тип первого объекта
    @param object_1_id: идентификационный номер первого объекта
    @param object_2_type: тип второго объекта
    @param object_2_id: идентификационный номер второго объекта
    @param list_id: идентификационный в списке если есть
    @param date_time_start: дата и время начала поиска связи
    @param date_time_end: дата и время конца поиска связи
    @param group_id: идентификатор группы пользователя
    @return: список идентификационных номеров объектов
        """
    result = []
    if rel_key == 0:
        rel_key = []
    else:
        rel_key = [rel_key]
    if list_id == 0:
        list_id = []
    else:
        list_id = [list_id]
    object1 = [object_1_type]
    if object_1_id != 0:
        object1.append(object_1_id)
    object2 = [object_2_type]
    if object_2_id != 0:
        object2.append(object_2_id)
    second_start, second_end = get_seconds_from_request_data_time(date_time_start, date_time_end)
    time_interval = {'second_start': second_start, 'second_end': second_end}
    temp_result = io_get_rel(group_id, rel_key, object1, object2, list_id, time_interval, True)
    temp_result = [temp for temp in temp_result if validate_rel_actual(temp, date_time_start, date_time_end)]
    for temp in temp_result:
        if int(temp['obj_id_1']) == object_1_type:
            if int(temp['obj_id_2']) == object_1_type:
                if object_1_id == 0 and object_2_id == 0:
                    result.append({'rec_id': int(temp['rec_id_1']), 'key_id': int(temp['key_id'])})
                    result.append({'rec_id': int(temp['rec_id_2']), 'key_id': int(temp['key_id'])})
                    continue
                elif object_1_id == 0 and object_2_id != 0:
                    if int(temp['rec_id_1']) == object_2_id:
                        result.append({'rec_id': int(temp['rec_id_2']), 'key_id': int(temp['key_id'])})
                        continue
                    else:
                        result.append({'rec_id': int(temp['rec_id_1']), 'key_id': int(temp['key_id'])})
                        continue
                if int(temp['rec_id_2']) == object_1_id:
                    result.append({'rec_id': int(temp['rec_id_2']), 'key_id': int(temp['key_id'])})
                else:
                    result.append({'rec_id': int(temp['rec_id_1']), 'key_id': int(temp['key_id'])})
            else:
                result.append({'rec_id': int(temp['rec_id_1']), 'key_id': int(temp['key_id'])})
        else:
            result.append({'rec_id': int(temp['rec_id_2']), 'key_id': int(temp['key_id'])})
    return result


def find_with_rel_reliable_key(object_1_type, request_1, object_2_type, request_2, rel_key, list_id, date_time_start,
                               date_time_end, actual_1=False, actual_2=False, group_id=0):
    """
    Функция для поиска записей с учетом связей, проводит надежную сверку по двум запросам, учитывает тип связи
    @param object_1_type: тип главного объекта для связи
    @param request_1: запрос по главному объекту
    @param object_2_type: тип второстепенного объекта для связи
    @param request_2: запрос по второстепенному объекту
    @param rel_key: тип связи
    @param list_id: идентификатор значения списка если есть
    @param date_time_start: дата и время начала поиска связи
    @param date_time_end: дата и время конца поиска связи
    @param actual_1: флаг актуальности поиска для первого объекта
    @param actual_2: флаг актуальности поиска для второго объекта
    @param group_id: идентификатор группы пользователя
    @return: список с идентификаторами подходящих записей
    """
    result = []
    if request_1:
        if len(request_1) == 0:
            result1 = [0]
        else:
            result1 = find_reliable_http(object_1_type, request_1, actual_1, group_id)
    else:
        result1 = [0]
    if request_2:
        if len(request_2) == 0:
            result2 = [0]
        else:
            result2 = find_reliable_http(object_2_type, request_2, actual_2, group_id)
    else:
        result2 = [0]
    for item in result1:
        for item_next in result2:
            res = search_rel_with_key_http(rel_key, object_1_type, item, object_2_type, item_next, list_id,
                                           date_time_start, date_time_end, group_id)
            if len(res) != 0:
                result.extend([int(elem['rec_id']) for elem in res])
    return result