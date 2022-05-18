from typing import List

from data_base_driver.additional_functions import date_time_client_to_server
from data_base_driver.input_output.input_output import io_get_rel
from objects.record.find_object import find_reliable_http
from objects.relations.additional_functions import get_seconds_from_request_data_time, get_unique_objects
from objects.relations.get_rel import get_object_relations


def validate_relation_actual(rel, date_time_start, date_time_end, group_id=0):
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


def search_relations_with_key(rel_key, object_id_1, rec_id_1, object_id_2, rec_id_2, list_id, date_time_start,
                              date_time_end, group_id=0) -> List[dict]:
    """
    Функция для поиска связей между двумя конкретными объектами
    @param rel_key: тип связи
    @param object_id_1: тип первого объекта
    @param rec_id_1: идентификационный номер первого объекта
    @param object_id_2: тип второго объекта
    @param rec_id_2: идентификационный номер второго объекта
    @param list_id: идентификационный в списке если есть
    @param date_time_start: дата и время начала поиска связи
    @param date_time_end: дата и время конца поиска связи
    @param group_id: идентификатор группы пользователя
    @return: список связанных объектов в формате {object_id, rec_id, key_id(тип связи)}
    """
    result = []
    rel_key = [] if rel_key == 0 else [rel_key]
    list_id = [] if list_id == 0 else [list_id]
    object1 = [object_id_1] if rec_id_1 == 0 else [object_id_1, rec_id_1]
    object2 = [object_id_2] if rec_id_2 == 0 else [object_id_2, rec_id_2]
    second_start, second_end = get_seconds_from_request_data_time(date_time_start, date_time_end)
    time_interval = {'second_start': second_start, 'second_end': second_end}
    temp_result = io_get_rel(group_id, rel_key, object1, object2, list_id, time_interval, True)
    temp_result = [temp for temp in temp_result if validate_relation_actual(temp, date_time_start, date_time_end)]
    temp_item = {'object_id': object_id_1}
    for temp in temp_result:
        if int(temp['obj_id_1']) == object_id_1:
            if int(temp['obj_id_2']) == object_id_1:
                if rec_id_1 == 0 and rec_id_2 == 0:
                    result.append({**temp_item, 'rec_id': int(temp['rec_id_1']), 'key_id': int(temp['key_id'])})
                    result.append({**temp_item, 'rec_id': int(temp['rec_id_2']), 'key_id': int(temp['key_id'])})
                else:
                    if rec_id_2 == int(temp['rec_id_1']):
                        result.append({**temp_item, 'rec_id': int(temp['rec_id_2']), 'key_id': int(temp['key_id'])})
                    else:
                        result.append({**temp_item, 'rec_id': int(temp['rec_id_1']), 'key_id': int(temp['key_id'])})
            else:
                result.append({**temp_item, 'rec_id': int(temp['rec_id_1']), 'key_id': int(temp['key_id'])})
        else:
            result.append({**temp_item, 'rec_id': int(temp['rec_id_2']), 'key_id': int(temp['key_id'])})
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
            res = search_relations_with_key(rel_key, object_1_type, item, object_2_type, item_next, list_id,
                                           date_time_start, date_time_end, group_id)
            if len(res) != 0:
                result.extend([int(elem['rec_id']) for elem in res])
    return result


def search_relations_recursive(group_id: int, request: dict, parent: dict) -> list:
    """
    Функция для рекурсивного построения дерева связей по запросу
    @param group_id: идентификатор группы пользователя
    @param request: запрос в формате:
        {object_id, rec_id, rels:[
            {object_id, rel:{id, value, date_time_start, date_time_end}, request, actual, rels:[{},{},...,{}]},
            {},
            ...,
            {}
        ]}
    @param parent: узел на текущей итерации
    @return: список связей текущего узла
    """
    relations: list = []
    for relation in request.get('rels', []):
        is_next: bool = len(relation.get('rels', [])) > 0
        if len(relation.get('request', '')) != 0:
            records = find_reliable_http(relation.get('object_id'), relation.get('request', ''),
                                         relation.get('actual'), group_id)
        else:
            records = [0]
        temp_length: int = 0
        for rec_id in records:
            related_objects = search_relations_with_key(
                relation.get('rel').get('id'), relation.get('object_id'), rec_id, parent.get('object_id'),
                parent.get('rec_id'), relation.get('rel').get('value'),
                date_time_client_to_server(relation.get('rel').get('date_time_start')),
                date_time_client_to_server(relation.get('rel').get('date_time_end')), group_id
            )
            if len(related_objects) > 0:
                for related_object in related_objects:
                    new_parent = {'object_id': related_object.get('object_id'), 'rec_id': int(related_object['rec_id'])}
                    if is_next:
                        temp = search_relations_recursive(group_id, relation, new_parent)
                        temp_length += len(temp)
                        if len(temp):
                            new_parent['relations'] = temp
                            relations.append(new_parent)
                    else:
                        relations.append(new_parent)
        if temp_length == 0 and is_next:
            return []
    return relations


def search_relations(group_id, request):
    """
    Функция для поиска связей по запросу
    @param group_id: идентификатор группы пользователя
    @param request: запрос в формате:
        {object_id, rec_id, rels:[
            {object_id, rel:{id, value, date_time_start, date_time_end}, request, actual, rels:[{},{},...,{}]},
            {},
            ...,
            {}
        ]}
    @return: словарь в формате:
        {object_id, rec_id, params, rels:[
            {object_id, rec_id, params, rels:[{},{},...,{}]},
            {},
            ...,
            {}
        ]}
    """
    if len(request.get('rels')) == 0:
        result = get_unique_objects(get_object_relations(group_id, request['object_id'], request['rec_id'], [], True))
    else:
        parent = {'object_id': request['object_id'], 'rec_id': request['rec_id']}
        result = get_unique_objects(search_relations_recursive(group_id, request, parent))
    return [item for item in result.values() if item['object_id'] != 1]

