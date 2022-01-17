from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_SYS_OBJ


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
    @:param object1: имя или id первого объекта
    @:param object2: имя или id второго объекта
    @:return: список словарей c информацией о искомых ключах
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


def get_relation_keys():
    return [item for item in DAT_SYS_KEY.DUMP.get_rec(obj_id=1, only_first=False) if
            item['rel_obj_1_id'] and item['rel_obj_2_id']]


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



