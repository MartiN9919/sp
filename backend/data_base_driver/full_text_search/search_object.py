from data_base_driver.connect.connect_manticore import db_shinxql
from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.full_text_search.search_rel import search_rel_with_key


def get_sorted_list(items):
    """
    Функция для сортировки списка по количеству вхождений элемента
    @param items: список с числовыми элементами
    @return: список отсортированный в порядке количества вхождений элементов
    """
    counter = {}
    for item in items:
        try:
            counter[item] += 1
        except KeyError:
            counter[item] = 1

    return [item[0] for item in sorted(counter.items(), key=lambda x: x[1], reverse=True)]


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


def find_with_rel_unreliable(object_type, request):
    """
    Функция для поиска записей в базе данных с учетом связей, без точного совпадения
    @param object_type: тип основного объекта для поиска
    @param request: строка запроса
    @return: список с идентификаторами подходящих записей
    """
    temp_result = []
    result = []
    temp_result.append([object_type, find_unreliable(FullTextSearch.TABLES[object_type], request)])
    for table in FullTextSearch.TABLES:
        if table == object_type:
            continue
        temp_result.append([table, find_unreliable(FullTextSearch.TABLES[table], request)])

    iter_res = iter(temp_result)
    for item in iter_res:
        for item_next in iter_res:
            for rec_id in item[1]:
                for rec_id_second in item_next[1]:
                    res = search_rel_with_key(0, item[0], rec_id, item_next[0], rec_id_second)
                    if len(res) != 0:
                        result.append(rec_id)
    if len(result) != 0:
        return get_sorted_list(result)
    else:
        result = find_reliable(FullTextSearch.TABLES[object_type], request)
        if len(result) != 0:
            return result
        else:
            return find_unreliable(FullTextSearch.TABLES[object_type], request)


def find_with_rel_reliable_key(object_1_type, request_1, object_2_type, request_2, rel_key):
    """
    Функция для поиска записей с учетом связей, проводит надежную сверку по двум запросам, учитывает тип связи
    @param object_1_type: тип главного объекта для связи
    @param request_1: запрос по главному объекту
    @param object_2_type: тип второстепенного объекта для связи
    @param request_2: запрос по второстепенному объекту
    @param rel_key: тип связи
    @return: список с идентификаторами подходящих записей
    """
    result = []
    if len(request_1) == 0:
        result1 = [0]
    else:
        result1 = find_reliable(FullTextSearch.TABLES[object_1_type], request_1)
    if len(request_2) == 0:
        result2 = [0]
    else:
        result2 = find_reliable(FullTextSearch.TABLES[object_2_type], request_2)
    for item in result1:
        for item_next in result2:
            res = search_rel_with_key(rel_key, object_1_type, item, object_2_type, item_next)
            if len(res) != 0:
                result.append(item)
    return result


def find_recursive_key(object_type, request, object_type_list, request_list, rel_key_list):
    """
    Функция для поиска записей с учетом большого количества связей и их типа
    @param object_type: тип главного объекта
    @param request: запрос к таблице главного объекта
    @param object_type_list: список с типами второстепенных объектов
    @param request_list: список с запросами ко второстепенным объектам
    @param rel_key_list: список типов связей
    @return: список с идентификаторами подходящих записей
    """
    temp_result = []
    for num, object in enumerate(object_type_list):
        temp_result.append(find_with_rel_reliable_key(object_type, request, object_type_list[num], request_list[num],
                                                      rel_key_list[num]))
    result = []
    for item in temp_result:
        result += item
    return get_sorted_list(result)


test = {'object_id':45, 'request': 'Описание 3', 'rel_id': 0, 'rels':
    [{'object_id':15, 'request': 'tv1', 'rel_id': 0, 'rels':
        [{'object_id':10, 'request': 'val 4', 'rel_id': 0, 'rels': [
            {'object_id':45, 'request': 'Описание 2', 'rel_id': 0, 'rels':[]}
        ]}]},
     {'object_id':10, 'request': 'val 3', 'rel_id': 508, 'rels': []}]}

test_object = {'object_id': 45, 'rec_id': 34, 'params': [{'id': 45001, 'val': 'val1'}, {'id': 45002, 'val': 'val2'}]}


def get_object_by_id(object_type, rec_id):
    """
    Функция для получения информации о объекте по его типу и идентификатору записи
    @param object_type: тип объекта
    @param rec_id: идентификатору записи
    @return: словарь в формате {object_id, rec_id, params:[{id,val},...,{}]}
    """
    sql = 'SELECT key_id, val FROM obj_' + FullTextSearch.TABLES[object_type] + '_row WHERE id = ' + \
                str(rec_id) + ';'
    params = [{'id': int(item[0]), 'val': item[1]} for item in db_shinxql(sql)]
    return {'object_id': object_type, 'rec_id': rec_id, 'params': params}


def search(request):
    """
    Вспомогательная функция для рекурсивного поиска объекта по древовидному запросу
    @param request: древовидный запрос
    @return: список словарей формате [{object_id, rec_ids},...,{}]
    """
    result = []
    for rel in request.get('rels', None):
        if len(rel.get('rels', None)) == 0:
            result.append({'object_id': request.get('object_id', None), 'rec_ids':
                find_with_rel_reliable_key(request.get('object_id', None), request.get('request', None),
                               rel.get('object_id', None), rel.get('request', None), rel.get('rel_id', None))})
        else:
            if len(request.get('request', None)) == 0:
                main_object_ids = [0]
            else:
                main_object_ids = find_reliable(FullTextSearch.TABLES[request.get('object_id', None)],
                                            request.get('request', None))
            temp = search(rel)
            temp_result = []
            for item in temp:
                for rec_id in item.get('rec_ids'):
                    for id in main_object_ids:
                        if len(search_rel_with_key(rel.get('rel_id'), request.get('object_id', None), id,
                                                     item.get('object_id'), rec_id)) != 0:
                            temp_result.append(id)
            result.append({'object_id':request.get('object_id', None), 'rec_ids': temp_result})
    return result


def search_top(request):
    """
    Функция точка входа для рекурсивного поиска объекта по древовидному запросу
    @param request: древовидный запрос
    @return: список найденных объектов в формате [{object_id, rec_id, params:[{id,val},...,{}]},...,{}]
    """
    result = []
    if len(request.get('rels', None)) != 0:
        temp = search(request)
        for item in temp:
            result.append(item.get('rec_ids'))
        res = None
        for item in result:
            if len(item) == 0:
                res = set()
                break
            if not res:
                res = set(item)
            else:
                res.intersection_update(set(item))
        return [get_object_by_id(request.get('object_id', None), item) for item in list(res)]
    else:
        return [get_object_by_id(request.get('object_id', None), item) for item in
                find_reliable(FullTextSearch.TABLES[request.get('object_id', None)], request.get('request', None))]





