from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.full_text_search.http_api.find_object import find_reliable_http, get_object_record_by_id_http
from data_base_driver.full_text_search.http_api.find_rel import search_rel_with_key_http
from data_base_driver.full_text_search.sphinxql.find_object import find_reliable, get_object_record_by_id
from data_base_driver.full_text_search.sphinxql.find_rel import search_rel_with_key


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
    result = []
    for rel in request.get(FullTextSearch.RELATIONS, None):
        if len(rel.get(FullTextSearch.RELATIONS, None)) == 0:
            result.append({FullTextSearch.OBJECT_ID: request.get(FullTextSearch.OBJECT_ID, None),
                           'rec_ids': find_with_rel_reliable_key(request.get(FullTextSearch.OBJECT_ID, None),
                                                                 request.get(FullTextSearch.REQUEST, None),
                                                                 rel.get(FullTextSearch.OBJECT_ID, None),
                                                                 rel.get(FullTextSearch.REQUEST, None),
                                                                 rel.get(FullTextSearch.RELATION_ID, None),
                                                                 rel.get(FullTextSearch.LIST_ID, 0))})
        else:
            if len(request.get(FullTextSearch.REQUEST, None)) == 0:
                main_object_ids = [0]
            else:
                main_object_ids = find_reliable_http(FullTextSearch.TABLES[request.get(FullTextSearch.OBJECT_ID, None)],
                                                request.get(FullTextSearch.REQUEST, None))
            temp = recursion_search(rel)
            temp_result = []
            for item in temp:
                for rec_id in item.get('rec_ids'):
                    for rec_id_main in main_object_ids:
                        temp_result.extend(search_rel_with_key_http(rel.get(FullTextSearch.RELATION_ID),
                                                               request.get(FullTextSearch.OBJECT_ID, None), rec_id_main,
                                                               item.get(FullTextSearch.OBJECT_ID), rec_id,
                                                               rel.get(FullTextSearch.LIST_ID, 0)))

            result.append(
                {FullTextSearch.OBJECT_ID: request.get(FullTextSearch.OBJECT_ID, None), 'rec_ids': temp_result})
    return result


def search(request):
    """
    Функция точка входа для рекурсивного поиска объекта по древовидному запросу
    @param request: древовидный запрос
    @return: список найденных объектов в формате [{object_id, rec_id, params:[{id,val},...,{}]},...,{}]
    """
    result = []
    if len(request.get(FullTextSearch.RELATIONS, None)) != 0:
        temp = recursion_search(request)
        for item in temp:
            result.append(item.get('rec_ids'))
        temp_set = None
        for item in result:
            if len(item) == 0:
                temp_set = set()
                break
            if not temp_set:
                temp_set = set(item)
            else:
                temp_set.intersection_update(set(item))
        return [get_object_record_by_id_http(request.get(FullTextSearch.OBJECT_ID, None), item) for item in temp_set]
    else:
        return [get_object_record_by_id_http(request.get(FullTextSearch.OBJECT_ID, None), item) for item in
                find_reliable_http(FullTextSearch.TABLES[request.get(FullTextSearch.OBJECT_ID, None)],
                              request.get(FullTextSearch.REQUEST, None))]
