from data_base_driver.input_output.io import io_get_obj
from data_base_driver.sys_key.get_key_dump import get_key_by_id
from itertools import groupby


def get_records_by_key_params(group_id, type, key, value, keys):
    """
    функция для нахождения объектов с заданным параметрами
    :param type: тип объекта
    :param key: тип искомого ключа
    :param value: значение искомого ключа
    :param keys: параметры которые необходимо знать у найденных объектов
    :return: список словарей в формате [ {id:{param:{title:title1,value:value1},param1:{...},...,paramN:valueN}},{},...{} ]
    """
    objects = io_get_obj(group_id=group_id, obj=type, keys=[key], ids=[], where_dop_row=[])
    objects_id = [object[0] for object in objects if object[2] == str(value)]
    objects = io_get_obj(group_id=group_id, obj=type, ids=objects_id, keys=keys, where_dop_row=[])
    group_objects = [list(group) for key, group in groupby(sorted(list(objects)), lambda x: x[0])]
    result = [{objects[0][0]: {get_key_by_id(record[1])['name']: {'title': get_key_by_id(record[1])['title'],
                                                                  'value': record[2]} for record in objects}}
              for objects in group_objects]
    return result


def get_record_by_id(group_id, object_type, record_id):
    """
    функция для получения отдельного объекта по его идентификационному номеру
    @param group_id: идентификационный номер группы пользователя
    @param object_type: тип объекта, имя или строка
    @param record_id: идентификационный номер объекта
    @return: словарь в формате {rec_id, object_id, params:[{id,val},...,{}]}
    """
    object = io_get_obj(group_id=group_id, obj=object_type, keys=[], ids=[record_id], where_dop_row=[])
    return {'rec_id': record_id, 'object_id': object_type,
            'params': [{'id': record[1], 'value': record[2], 'date': record[3]} for record in object]}


def get_records_by_object(group_id, object_type):
    """
    функция для получения списка объектов по заданному типу
    @param group_id: идентификационный номер группы пользователя
    @param object_type: тип объекта, название иди идентификационный номер
    @return:
    """
    objects = io_get_obj(group_id=group_id, obj=object_type, keys=[], ids=[], where_dop_row=[])
    group_objects = [list(group) for key, group in groupby(sorted(list(objects)), lambda x: x[0])]
    result = [{objects[0][0]: {get_key_by_id(record[1])['name']: {'title': get_key_by_id(record[1])['title'],
                                                                  'value': record[2]} for record in objects}}
              for objects in group_objects]
    return result
