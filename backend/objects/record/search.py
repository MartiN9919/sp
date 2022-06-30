from data_base_driver.additional_functions import date_time_client_to_server
from data_base_driver.constants.const_fulltextsearch import FullTextSearch
from objects.record.find_object import find_reliable_http, find_text
from objects.record.get_record import get_record_title
from objects.relations.find_rel import search_relations_with_key


def recursion_search(group_id: int, request: dict) -> dict:
    """
    Вспомогательная функция для рекурсивного поиска объекта по древовидному запросу
    @param group_id: идентификатор группы пользователя
    @param request: древовидный запрос
    @return: список словарей формате [{object_id, rec_ids},...,{}]
    """
    result = {'object_id': request[FullTextSearch.OBJECT_ID], 'records': None, 'old': [], 'pre_old': []}
    for relation in request.get(FullTextSearch.RELATIONS, []):
        main_object_records = [0] if len(request.get(FullTextSearch.REQUEST, '')) == 0 else find_reliable_http(
            request.get(FullTextSearch.OBJECT_ID), request.get(FullTextSearch.REQUEST, ''),
            request.get(FullTextSearch.ACTUAL, False))
        if len(relation.get(FullTextSearch.RELATIONS, [])) == 0:
            other_objects_id = relation['object_id']
            other_objects_records = [0] if len(relation.get(FullTextSearch.REQUEST, '')) == 0 else find_reliable_http(
                relation.get(FullTextSearch.OBJECT_ID),
                relation.get(FullTextSearch.REQUEST, ''),
                relation.get(FullTextSearch.ACTUAL, False))
        else:
            old_result = recursion_search(group_id, relation)
            other_objects_id = old_result['object_id']
            other_objects_records = old_result['records']
            result['pre_old'] += old_result['old']
        result['old'].append({'object_id': other_objects_id, 'records': other_objects_records})
        temp_result = set()
        for rec_id in other_objects_records:
            for rec_id_main in main_object_records:
                temp_set = search_relations_with_key(
                    relation.get(FullTextSearch.REL, {}).get(FullTextSearch.RELATION_ID, 0),
                    request.get(FullTextSearch.OBJECT_ID, None), rec_id_main,
                    other_objects_id, rec_id,
                    relation.get(FullTextSearch.REL, {}).get(FullTextSearch.REL_VALUE, 0),
                    date_time_client_to_server(
                        relation.get(FullTextSearch.REL, {}).get(FullTextSearch.DATE_TIME_START)),
                    date_time_client_to_server(relation.get(FullTextSearch.REL, {}).get(FullTextSearch.DATE_TIME_END)),
                    group_id)
                if len(temp_result) == 0:
                    temp_result = set([int(item['rec_id']) for item in temp_set])
                else:
                    temp_result = temp_result.union([int(item['rec_id']) for item in temp_set])
        if result.get('records') is None:
            result['records'] = temp_result
        else:
            result['records'].intersection_update(temp_result)
    for temp in result.get('pre_old', []):
        if temp['object_id'] == result['object_id']:
            result['records'] = result['records'].difference(temp['records'])
    return result


def search_many_objects(group_id, object_ids, request, triggers, actual):
    result = []
    for object_id in object_ids:
        result += [{'rec_id': item[0], 'score': item[1], 'object_id': object_id}
                   for item in find_text(group_id, object_id, request, actual, score=True)]
    return [get_record_title(item['object_id'], item['rec_id'], group_id, triggers=triggers[str(item['object_id'])])
            for item in sorted(result, key=lambda x: x['score'], reverse=True)]


def search(request, group_id, triggers):
    """
    Функция точка входа для рекурсивного поиска объекта по древовидному запросу
    @param request: древовидный запрос
    @param group_id: идентификатор группы пользователя
    @param triggers: установленные пользователем триггеры
    @return: список найденных объектов в формате [{object_id, rec_id, params:[{id,val},...,{}]},...,{}]
    """
    base_object_list = request.get(FullTextSearch.OBJECT_ID, [])
    if len(base_object_list) == 0:
        return []
    if len(base_object_list) > 1:
        return search_many_objects(group_id, base_object_list, request.get(FullTextSearch.REQUEST, ''), triggers,
                                   request.get(FullTextSearch.ACTUAL, False))
    else:
        request[FullTextSearch.OBJECT_ID] = base_object_list[0]
    if len(request.get(FullTextSearch.RELATIONS, None)) != 0:
        return [get_record_title(request.get(FullTextSearch.OBJECT_ID, None), item, group_id, triggers=triggers[str(request[FullTextSearch.OBJECT_ID])]) for
                item in recursion_search(group_id, request)['records']]
    else:
        return [get_record_title(request.get(FullTextSearch.OBJECT_ID, None), item, group_id, triggers=triggers[str(request[FullTextSearch.OBJECT_ID])]) for
                item in find_reliable_http(request.get(FullTextSearch.OBJECT_ID, None),
                                           request.get(FullTextSearch.REQUEST, ''),
                                           request.get(FullTextSearch.ACTUAL, False),
                                           group_id)]
