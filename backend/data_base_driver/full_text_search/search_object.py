from data_base_driver.connect.connect_manticore import db_shinxql
from data_base_driver.constants.full_text_search import Full_text_search
from data_base_driver.full_text_search.search_rel import search_rel, search_rel_with_key


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
    temp_result.append([object_type, find_unreliable(Full_text_search.TABLES[object_type], request)])
    for table in Full_text_search.TABLES:
        if table == object_type:
            continue
        temp_result.append([table, find_unreliable(Full_text_search.TABLES[table], request)])

    iter_res = iter(temp_result)
    for item in iter_res:
        for item_next in iter_res:
            for rec_id in item[1]:
                for rec_id_second in item_next[1]:
                    res = search_rel(item[0], rec_id, item_next[0], rec_id_second)
                    if len(res) != 0:
                        result.append(rec_id)
    if len(result) != 0:
        return get_sorted_list(result)
    else:
        result = find_reliable(Full_text_search.TABLES[object_type], request)
        if len(result) != 0:
            return result
        else:
            return find_unreliable(Full_text_search.TABLES[object_type], request)


def find_with_rel_reliable(object_1_type, request_1, object_2_type, request_2):
    """
    Функция для поиска записей с учетом связей, проводит надежную сверку по двум запросам
    @param object_1_type: тип главного объекта для связи
    @param request_1: запрос по главному объекту
    @param object_2_type: тип второстепенного объекта для связи
    @param request_2: запрос по второстепенному объекту
    @return: список с идентификаторами подходящих записей
    """
    result = []
    result1 = find_reliable(Full_text_search.TABLES[object_1_type], request_1)
    result2 = find_reliable(Full_text_search.TABLES[object_2_type], request_2)
    for item in result1:
        for item_next in result2:
            res = search_rel(object_1_type, item, object_2_type, item_next)
            if len(res) != 0:
                result.append(item)
    return result


def find_recursive(object_type, request, object_type_list, request_list):
    """
    Функция для поиска записей с учетом большого количества связей
    @param object_type: тип главного объекта
    @param request: запрос к таблице главного объекта
    @param object_type_list: список с типами второстепенных объектов
    @param request_list: список с запросами ко второстепенным объектам
    @return: список с идентификаторами подходящих записей
    """
    temp_result = []
    for num, object in enumerate(object_type_list):
        temp_result.append(find_with_rel_reliable(object_type, request, object_type_list[num], request_list[num]))
    result = []
    for item in temp_result:
        result += item
    return get_sorted_list(result)


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
    result1 = find_reliable(Full_text_search.TABLES[object_1_type], request_1)
    result2 = find_reliable(Full_text_search.TABLES[object_2_type], request_2)
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

# print(find_recursive(45, 'Описание 3', [15, 10], ['tv1', 'val 3']))
# print(find_with_rel_reliable_key(45, 'Описание 3', 15, 'tv1', 507))

# tmp = []
# test_list = [[1,2,5],[3,5,7],[1,5],[]]
# for t in test_list:
#     tmp += t
#
# print(get_sorted_list(tmp))
