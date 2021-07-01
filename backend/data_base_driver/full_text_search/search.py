from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.full_text_search.http_api.find_object import find_reliable_http, get_object_record_by_id_http
from data_base_driver.full_text_search.http_api.find_rel import search_rel_with_key_http


def find_with_rel_reliable_key(object_1_type, request_1, object_2_type, request_2, rel_key, list_id):
    """
    Функция для поиска записей с учетом связей, проводит надежную сверку по двум запросам, учитывает тип связи
    @param object_1_type: тип главного объекта для связи
    @param request_1: запрос по главному объекту
    @param object_2_type: тип второстепенного объекта для связи
    @param request_2: запрос по второстепенному объекту
    @param rel_key: тип связи
    @param list_id: идентификатор значения списка если есть
    @return: список с идентификаторами подходящих записей
    """
    result = []
    if len(request_1) == 0:
        result1 = [0]
    else:
        result1 = find_reliable_http(FullTextSearch.TABLES[object_1_type], request_1)
    if len(request_2) == 0:
        result2 = [0]
    else:
        result2 = find_reliable_http(FullTextSearch.TABLES[object_2_type], request_2)
    for item in result1:
        for item_next in result2:
            res = search_rel_with_key_http(rel_key, object_1_type, item, object_2_type, item_next, list_id)
            if len(res) != 0:
                result.extend([int(elem) for elem in res])
    return result


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
                                                      request.get(FullTextSearch.REQUEST, None),
                                                      rel.get(FullTextSearch.OBJECT_ID, None),
                                                      rel.get(FullTextSearch.REQUEST, None),
                                                      rel.get(FullTextSearch.RELATION_ID, None),
                                                      rel.get(FullTextSearch.LIST_ID, 0)))
            if not result.get('rec_ids'):
                result['rec_ids'] = temp_set
            else:
                result['rec_ids'].intersection_update(temp_set)
            result['old_result'].append({'object_id': rel.get(FullTextSearch.OBJECT_ID, None),
                                            'rec_ids': find_reliable_http(
                                                FullTextSearch.TABLES[rel.get(FullTextSearch.OBJECT_ID, None)],
                                                rel.get(FullTextSearch.REQUEST, None))})
        else:
            if len(request.get(FullTextSearch.REQUEST, None)) == 0:
                main_object_ids = [0]
            else:
                main_object_ids = find_reliable_http(FullTextSearch.TABLES[request.get(FullTextSearch.OBJECT_ID, None)],
                                                     request.get(FullTextSearch.REQUEST, None))
            temp = recursion_search(rel)
            result['old_result'].append({'object_id': temp['object_id'],
                                            'rec_ids': temp['rec_ids']})
            result['pre_old_result'] = temp['old_result']
            temp_result = set()
            for rec_id in temp.get('rec_ids'):
                for rec_id_main in main_object_ids:
                    temp_set = set(search_rel_with_key_http(rel.get(FullTextSearch.RELATION_ID),
                                                            request.get(FullTextSearch.OBJECT_ID, None), rec_id_main,
                                                            temp.get(FullTextSearch.OBJECT_ID), rec_id,
                                                            rel.get(FullTextSearch.LIST_ID, 0)))
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
                                   request.get(FullTextSearch.REQUEST, None))]
