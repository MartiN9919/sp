from data_base_driver.additional_functions import date_time_client_to_server
from data_base_driver.constants.const_fulltextsearch import FullTextSearch
from objects.record.find_object import find_reliable_http
from objects.record.get_record import get_record_title
from objects.relations.find_rel import search_relations_with_key


def recursion_search(group_id: int, request: dict) -> dict:
    """
    Вспомогательная функция для рекурсивного поиска объекта по древовидному запросу
    @param group_id: идентификатор группы пользователя
    @param request: древовидный запрос
    @return: список словарей формате [{object_id, rec_ids},...,{}]
    """
    result = {'object_id': request[FullTextSearch.OBJECT_ID], 'records': None, 'old': []}
    for relation in request.get(FullTextSearch.RELATIONS, []):
        main_object_records = [0] if len(request.get(FullTextSearch.REQUEST, '')) == 0 else find_reliable_http(
            request.get(FullTextSearch.OBJECT_ID), request.get(FullTextSearch.REQUEST, ''),
            request.get(FullTextSearch.ACTUAL, False))
        if len(relation.get(FullTextSearch.RELATIONS, [])) > 0:
            old_result = recursion_search(group_id, relation)
            other_objects_id = old_result['object_id']
            other_objects_records = old_result['records']
            result['pre_old'] = old_result['old']
        else:
            other_objects_id = relation['object_id']
            other_objects_records = [0] if len(relation.get(FullTextSearch.REQUEST, '')) == 0 else find_reliable_http(
               relation.get(FullTextSearch.OBJECT_ID),
               relation.get(FullTextSearch.REQUEST, ''),
               relation.get(FullTextSearch.ACTUAL, False))
        result['old'].append({'object_id': other_objects_id, 'records': other_objects_records})
        temp_result = None
        for rec_id in other_objects_records:
            for rec_id_main in main_object_records:
                temp_set = search_relations_with_key(relation.get(FullTextSearch.REL, {}).
                                                     get(FullTextSearch.RELATION_ID, 0),
                                                     request.get(FullTextSearch.OBJECT_ID, None), rec_id_main,
                                                     other_objects_id, rec_id,
                                                     relation.get(FullTextSearch.REL, {}).
                                                     get(FullTextSearch.REL_VALUE, 0),
                                                     date_time_client_to_server(relation.get(FullTextSearch.REL, {}).
                                                                                get(FullTextSearch.DATE_TIME_START)),
                                                     date_time_client_to_server(relation.get(FullTextSearch.REL, {}).
                                                                                get(FullTextSearch.DATE_TIME_END)),
                                                     group_id)
                if not temp_result:
                    temp_result = set([int(item['rec_id']) for item in temp_set])
                else:
                    temp_result = temp_result.union([int(item['rec_id']) for item in temp_set])
        if not result.get('records'):
            result['records'] = temp_result
        else:
            result['records'].intersection_update(temp_result)
    for temp in result.get('pre_old', []):
        if temp['object_id'] == result['object_id']:
            result['records'] = result['records'].difference(temp['records'])
    return result


def search(request, group_id, triggers):
    """
    Функция точка входа для рекурсивного поиска объекта по древовидному запросу
    @param request: древовидный запрос
    @param group_id: идентификатор группы пользователя
    @param triggers: установленные пользователем триггеры
    @return: список найденных объектов в формате [{object_id, rec_id, params:[{id,val},...,{}]},...,{}]
    """
    if len(request.get(FullTextSearch.RELATIONS, None)) != 0:
        return [get_record_title(request.get(FullTextSearch.OBJECT_ID, None), item, group_id, triggers=triggers) for
                item in recursion_search(group_id, request)['records']]
    else:
        return [get_record_title(request.get(FullTextSearch.OBJECT_ID, None), item, group_id, triggers=triggers) for
                item in find_reliable_http(request.get(FullTextSearch.OBJECT_ID, None),
                                           request.get(FullTextSearch.REQUEST, ''),
                                           request.get(FullTextSearch.ACTUAL, False),
                                           group_id)]
