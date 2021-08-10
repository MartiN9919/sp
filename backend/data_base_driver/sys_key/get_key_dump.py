from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_SYS_OBJ
from data_base_driver.sys_key.get_list import get_list_by_top_id


def get_obj_id(name):
    """
    Функция для получения идентификационного номера объекта по его имени
    @param name: имя объекта
    @return: идентификационного номера объекта
    """
    return DAT_SYS_OBJ.DUMP.get_rec(name=name)[DAT_SYS_OBJ.ID]


def filter_rel(dict, object1, object2):
    """
    Функция для фильтрации типа связей по типу объектов
    @param dict: словарь содержащий тип связи
    @param object1: идентификационный номер 1 объекта
    @param object2: идентификационный номер 2 объекта
    @return: True если тип связи относится к данным объекта, False если не относится
    """
    if (dict[DAT_SYS_KEY.REL_OBJ_1_ID] == object1 and dict[DAT_SYS_KEY.REL_OBJ_2_ID] == object2) \
            or (dict[DAT_SYS_KEY.REL_OBJ_2_ID] == object1 and dict[DAT_SYS_KEY.REL_OBJ_1_ID] == object2):
        return True
    else:
        return False


def get_keys_by_rel(object1, object2):
    """
    получения списка ключей по типу объектов которые он связывает
    :param object1: имя или id первого объекта
    :param object2: имя или id второго объекта
    :return: список словарей c информацией о искомых ключах
    """
    if isinstance(object1, str) and not (object1.isdigit()):
        object1 = get_obj_id(object1)
    if isinstance(object2, str) and not (object2.isdigit()):
        object2 = get_obj_id(object2)
    if object1 > object2:
        tmp = object1
        object1 = object2
        object2 = tmp
    return [item for item in DAT_SYS_KEY.DUMP.get_rec(obj_id=1, only_first=False) if
            filter_rel(item, int(object1), int(object2))]


def get_relations_list(object1, object2):
    """
    Функция для получения списка возможных связей по типу связываемых объектов
    @param object1: имя или id первого объекта
    @param object2: имя или id второго объекта
    @return: список в формате [{id,title,hint,list},...,{}]
    """
    result = []
    for item in get_keys_by_rel(object1, object2):
        list_item = None
        if item.get('list_id'):
            list_item = get_list_by_top_id(int(item.get('list_id')))
        result.append({'id': item['id'], 'title': item['title'], 'hint': item['hint'], 'list': list_item})
    return result


def get_keys_by_object(object):
    """
    Получение списка ключей по типу объекта
    @param object: имя или тип объекта
    @return: список словарей c информацией о искомых ключах
    """
    if isinstance(object, str) and not (object.isdigit()):
        object = get_obj_id(object)
    keys = DAT_SYS_KEY.DUMP.get_rec(obj_id=int(object), only_first=False)
    result = []
    for key in keys:
        temp = dict(key)
        if key['id'] == 25202 or key['id'] == 25203: # проверка на lat, lon, если да то пропускаем - КОСТЫЛЬ
            continue
        temp.pop('rel_obj_1_id')
        temp.pop('rel_obj_2_id')
        if temp.get('list_id'):
            temp['list_id'] = get_list_by_top_id(int(temp.get('list_id')))
        result.append(temp)
    return result


def get_key_by_id(id):
    """
    Функция для получения ключа классификатора по его идентификационному номеру
    @param id: идентификационный номер ключа классификатора
    @return: словарь содержащий информацию о ключе классификатора
    """
    if isinstance(id, str) and not (id.isdigit()):
        return 'error'
    else:
        return DAT_SYS_KEY.DUMP.get_rec(id=int(id))


def get_key_by_name(name):
    """
    Функция для получения ключа классификатора по его имени
    @param name: имя ключа классификатора
    @return: словарь содержащий информацию о ключе классификатора
    """
    return DAT_SYS_KEY.DUMP.get_rec(name=name)
