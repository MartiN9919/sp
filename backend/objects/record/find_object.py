from data_base_driver.additional_functions import intercept_sort_list
from data_base_driver.constants.const_key import SYS_KEY_CONSTANT
from data_base_driver.input_output.input_output import io_get_obj
from data_base_driver.sys_key.get_key_dump import get_key_by_id
from synonyms_manager.get_synonyms import get_synonyms


def find_reliable_http(object_type, request, actual=False, group_id=0):
    """
    Функция для поиска значений в таблице object, возвращает результат только при полном совпадении
    @param object_type: тип объекта по которым идет поиск
    @param request: искомые параметры
    @param actual: флаг актуальности искомого параметра, если True то учитываются только записи актуальные для объекта
    на данный момент
    @param group_id: идентификатор группы пользователя
    @return: список id объектов с искомыми параметрами, если не найдено, то пустой список
    """
    if not request:
        request = ''
    synonyms_list = []
    if object_type == SYS_KEY_CONSTANT.FILE_ID:
        synonyms_list = get_synonyms(request)
    request = request.split(' ') + synonyms_list
    request = [word.replace('-', '<<') for word in request] # костыль, в последующем поменяить настройки мантикоры, что бы индексировала '-'
    result = []
    for word in request:
        temp_result = io_get_obj(group_id, object_type, [], [], 500, word, {})
        fetchall = [(int(item['rec_id']), int(item['key_id']), int(item['sec'])) for item in temp_result]
        remove_list = []
        if actual:
            for item in fetchall:
                temp_word = '@key_id ' + str(item[1])
                temp = io_get_obj(group_id, object_type, [], [item[0]], 500, temp_word, {})
                for temp_item in temp:
                    if item[2] == temp_item['sec']:
                        continue
                    else:
                        if item[2] < temp_item['sec']:
                            remove_list.append(item)
        fetchall = [item[0] for item in fetchall if not item in remove_list]
        result.append(list(dict.fromkeys(fetchall)))
    if object_type != SYS_KEY_CONSTANT.FILE_ID:
        return intercept_sort_list(result)
    else:
        return [item for sublist in result for item in sublist]


def find_unreliable_http(object_type, request, group_id=0):
    """
    Функция для поиска значений в таблице object, возвращает наиболее похожие результаты
    @param object_type: тип объекта по которым идет поиск
    @param request: искомые параметры
    @param group_id: идентификатор группы пользователя
    @return: список id объектов с искомыми параметрами, если подобных нет, то пустой список
    """
    request = request.replace(' ', '|')
    response = io_get_obj(group_id, object_type, [], [], 500, request, {})
    return [int(hit['rec_id']) for hit in response]


def find_key_value_http(object_id, key_id, value, group_id=0):
    """
    Функция для нахождения в базе данных по отдельным полям
    @param object_id: идентификатор типа объекта
    @param key_id: ключ искомого классификатора
    @param value: искомое значение
    @param group_id: идентификатор группы пользователя
    @return: список идентификатор объектов
    """
    if get_key_by_id(key_id)['type'] == 'date' or get_key_by_id(key_id)['type'] == 'date_time':
        value = str(value).replace('-', '<<')
    else:
        value = str(value)
    response = io_get_obj(group_id, object_id, [], [], 500, '@key_id ' + str(key_id) + ' @val ' + value, {})
    remove_list = []
    for item in response:
        temp_word = '@key_id ' + str(key_id)
        temp = io_get_obj(group_id, object_id, [], [item['rec_id']], 500, temp_word, {})
        for temp_item in temp:
            if item['sec'] == temp_item['sec']:
                continue
            else:
                if item['sec'] < temp_item['sec'] and item['val'] != temp_item['val']:
                    remove_list.append(int(item['rec_id']))
    return [int(item['rec_id']) for item in response if not int(item['rec_id']) in remove_list]