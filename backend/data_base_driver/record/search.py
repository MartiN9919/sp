from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.full_text_search.http_api.find_object import find_reliable_http, get_object_record_by_id_http
from data_base_driver.full_text_search.http_api.find_rel import search_rel_with_key_http
from data_base_driver.relations.get_rel import find_with_rel_reliable_key


def recursion_search(request):
    """
    Вспомогательная функция для рекурсивного поиска объекта по древовидному запросу
    @param request: древовидный запрос
    @return: список словарей формате [{object_id, rec_ids},...,{}]
    """
    result = {'object_id': request.get(FullTextSearch.OBJECT_ID, None),
              'rec_ids': None,
              'old_result': [],
              'pre_old_result': []}
    for rel in request.get(FullTextSearch.RELATIONS, None):
        if len(rel.get(FullTextSearch.RELATIONS, None)) == 0:
            temp_set = set(find_with_rel_reliable_key(request.get(FullTextSearch.OBJECT_ID, None),
                                                      request.get(FullTextSearch.REQUEST, ''),
                                                      rel.get(FullTextSearch.OBJECT_ID, None),
                                                      rel.get(FullTextSearch.REQUEST, ''),
                                                      rel.get(FullTextSearch.REL, {}).get(FullTextSearch.RELATION_ID),
                                                      rel.get(FullTextSearch.REL, {}).get(FullTextSearch.REL_VALUE, 0),
                                                      rel.get(FullTextSearch.REL, {}).get(FullTextSearch.DATE_TIME_START),
                                                      rel.get(FullTextSearch.REL, {}).get(FullTextSearch.DATE_TIME_END),
                                                      request.get(FullTextSearch.ACTUAL, False),
                                                      rel.get(FullTextSearch.ACTUAL, False)))
            if not result.get('rec_ids'):
                result['rec_ids'] = temp_set
            else:
                result['rec_ids'].intersection_update(temp_set)
            if rel.get(FullTextSearch.REQUEST, '') == '':
                result['old_result'].append({'object_id': rel.get(FullTextSearch.OBJECT_ID, None),
                                             'rec_ids': []})
            else:
                result['old_result'].append({'object_id': rel.get(FullTextSearch.OBJECT_ID, None),
                                             'rec_ids': find_reliable_http(
                                                 FullTextSearch.TABLES[rel.get(FullTextSearch.OBJECT_ID, None)],
                                                 rel.get(FullTextSearch.REQUEST, ''),
                                                 rel.get(FullTextSearch.ACTUAL, False))})
        else:
            if request.get(FullTextSearch.REQUEST, ''):
                if len(request.get(FullTextSearch.REQUEST, '')) == 0:
                    main_object_ids = [0]
                else:
                    main_object_ids = find_reliable_http(FullTextSearch.TABLES[request.get(FullTextSearch.OBJECT_ID, None)],
                                                         request.get(FullTextSearch.REQUEST, ''),
                                                         request.get(FullTextSearch.ACTUAL, False))
            else:
                main_object_ids = [0]
            temp = recursion_search(rel)
            result['old_result'].append({'object_id': temp['object_id'],
                                         'rec_ids': temp['rec_ids']})
            result['pre_old_result'] = temp['old_result']
            temp_result = set()
            for rec_id in temp.get('rec_ids'):
                for rec_id_main in main_object_ids:
                    temp_set = set(search_rel_with_key_http(rel.get(FullTextSearch.REL, {}).
                                                            get(FullTextSearch.RELATION_ID, 0),
                                                            request.get(FullTextSearch.OBJECT_ID, None), rec_id_main,
                                                            temp.get(FullTextSearch.OBJECT_ID), rec_id,
                                                            rel.get(FullTextSearch.REL, {}).
                                                            get(FullTextSearch.REL_VALUE, 0),
                                                            rel.get(FullTextSearch.REL, {}).
                                                            get(FullTextSearch.DATE_TIME_START),
                                                            rel.get(FullTextSearch.REL, {}).
                                                            get(FullTextSearch.DATE_TIME_END),
                                                            ))
                    if len(temp_result) == 0:
                        temp_result = temp_set
                    else:
                        temp_result = temp_result.union(temp_set)
            result['rec_ids'] = temp_result
    for temp in result['pre_old_result']:
        if temp['object_id'] == result['object_id']:
            result['rec_ids'] = result['rec_ids'].difference(temp['rec_ids'])
    return result


def search(request):
    """
    Функция точка входа для рекурсивного поиска объекта по древовидному запросу
    @param request: древовидный запрос
    @return: список найденных объектов в формате [{object_id, rec_id, params:[{id,val},...,{}]},...,{}]
    """
    if len(request.get(FullTextSearch.RELATIONS, None)) != 0:
        return [get_object_record_by_id_http(request.get(FullTextSearch.OBJECT_ID, None), item) for item in
                recursion_search(request)['rec_ids']]
    else:
        return [get_object_record_by_id_http(request.get(FullTextSearch.OBJECT_ID, None), item) for item in
                find_reliable_http(FullTextSearch.TABLES[request.get(FullTextSearch.OBJECT_ID, None)],
                                   request.get(FullTextSearch.REQUEST, ''),
                                   request.get(FullTextSearch.ACTUAL, False))]
