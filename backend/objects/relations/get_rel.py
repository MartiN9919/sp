from multiprocessing import Process, Manager
from typing import List

from data_base_driver.additional_functions import get_date_time_from_sec, date_time_server_to_client
from data_base_driver.input_output.input_output import io_get_rel
from data_base_driver.sys_key.get_key_dump import get_relation_keys
from data_base_driver.sys_key.get_list import get_item_list_value
from objects.record.get_record import get_object_record_by_id_http
from objects.relations.additional_functions import get_unique_objects, check_in_list


def get_related_objects(group_id, object_id, rec_id, keys, values, time_interval, result_object_type=0) -> list:
    """
    Функция для получения списка объектов связанных с искомым по заданным характеристикам (Для скриптов)
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param keys: список идентификаторов типов связей, если любые то пустой список
    @param values: список идентификаторов значений связей, если любые то пустой список
    @param time_interval: временной интервал установления связи в формате {second_start,second_end}
    @param result_object_type: идентификатор типа результирующего объекта для фильтрации, если любой то 0
    @return: список словарей в формате [{object_id, rec_id, key_id, val},...,{}]
    """
    temp_object = [] if result_object_type == 0 else [result_object_type]
    relations = io_get_rel(group_id, keys, [object_id, rec_id], temp_object, values, time_interval, True)
    result: List[dict] = []
    for relation in relations:
        if int(relation['obj_id_1']) == object_id and int(relation['rec_id_1']) == rec_id:
            result.append({'object_id': int(relation['obj_id_2']), 'rec_id': int(relation['rec_id_2']),
                           'key_id': int(relation['key_id']), 'val': relation['val']})
        else:
            result.append({'object_id': int(relation['obj_id_1']), 'rec_id': int(relation['rec_id_1']),
                           'key_id': int(relation['key_id']), 'val': relation['val']})
    result = [dict(s) for s in set(frozenset(d.items()) for d in result)]
    return result


def get_relations_cascade(group_id: int, object_id: int, rec_id: int, depth: int, parents: list = None) -> list:
    """
    Функция для получения дерева связей объекта на заданную глубину
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param depth: глубина построения дерева
    @param parents: объекты уже встреченные в текущей ветке
    @return: список связей в формате [{object_id, rec_id, relations:[{},...,{}], relation_types:[{},...,{}]},...,{}]
    """
    if depth == 0:
        return []
    if not parents:
        parents = []
    relations = get_related_objects(group_id, object_id, rec_id, [], [], {})
    relations = [item for item in relations if not check_in_list(item, ['object_id', 'rec_id'], parents)]
    for relation in relations:
        relation['relations'] = get_relations_cascade(group_id, relation['object_id'], relation['rec_id'], depth - 1,
                                                      [*parents, {'object_id': object_id, 'rec_id': rec_id}])
    return relations


def get_relations_by_object(group_id: int, object_id: int, rec_id: int) -> list:
    """
    Вспомогательная функция получения связей с определенной записью таблицы событий-связей,
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор или имя типа объекта
    @param rec_id: идентификатор объекта в базе данных
    @return: список связей [{object_id, rec_id, relation_types},...,{}]
    """
    temp_relations = io_get_rel(group_id, [], [object_id, rec_id], [], [], {}, True)
    relations = []
    for relation in temp_relations:
        id_str = '1' if relation['obj_id_2'] == object_id and relation['rec_id_2'] == rec_id else '2'
        temp_object_id, temp_rec_id = f"obj_id_{id_str}", f"rec_id_{id_str}"
        doc = get_object_record_by_id_http(20, relation['document_id'], group_id, []) \
            if relation['document_id'] != 0 else None
        old_relation = [item for item in relations if relation[temp_object_id] == item['object_id'] and
                        relation[temp_rec_id] == item['rec_id']]
        if len(old_relation) > 0:
            temp_relation = [item for item in old_relation[0]['relation_types'] if item['id'] == relation['key_id']]
            if len(temp_relation) > 0:
                temp_relation[0]['values'].append(
                    {'value': get_item_list_value(int(relation['val'])) if relation['val'] != 0 else '',
                     'date': get_date_time_from_sec(relation['sec'])[:-3], 'doc': doc})
            else:
                old_relation[0]['relation_types'].append({'id': relation['key_id'], 'values': [
                    {'value': get_item_list_value(int(relation['val'])) if relation['val'] != 0 else '', 'doc': doc,
                     'date': get_date_time_from_sec(relation['sec'])[:-3]}]})
        else:
            relations.append({
                'object_id': relation[temp_object_id],
                'rec_id': relation[temp_rec_id],
                'relation_types': [{
                    'id': relation['key_id'],
                    'values': [{
                        'value': get_item_list_value(int(relation['val'])) if
                        relation['val'] != 0 else '',
                        'date': get_date_time_from_sec(relation['sec'])[:-3],
                        'doc': doc
                    }]
                }]
            })
    for relation in relations:
        for relation_type in relation['relation_types']:
            relation_type['values'].sort(key=lambda x: x['date'], reverse=True)
            for value in relation_type['values']:
                value['date'] = date_time_server_to_client(value['date'])
    return relations


def get_object_relations(group_id, object_id, rec_id, objects, is_all=False):
    """
    Функция получения всех связей для объекта, с учетом уже имеющихся объектов
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param objects: список объектов связи с которыми требуются в результате
    @param is_all: флаг для получения всех связей
    @return: список словарей в формате [{object_id, rec_id, params, relations:[{key_id, sec, val},...,{}]},...,{}]
    """
    if len(objects) == 0 and not is_all:
        return []
    result = get_relations_by_object(group_id, object_id, rec_id)
    result = [temp for temp in result if check_in_list(temp, ['object_id', 'rec_id'], objects) or is_all]
    return result


def get_objects_process(group_id, object_id, rec_id, depth, value):
    """
    Функция для работы в отдельном процессе для поиска уникальных связанных объектов и путей к ним
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param depth: глубина поиска
    @param value: словарь для сохранения результата
    """
    relations = get_relations_cascade(group_id, object_id, rec_id, depth)
    value[f"{object_id}_{rec_id}"] = get_unique_objects(relations)


def get_objects_relation(group_id, object_id_1, rec_id_1, object_id_2, rec_id_2, depth=3):
    """
    Функция для получения связей между двумя объектами
    @param group_id: идентификатор группы пользователя
    @param object_id_1: идентификатор типа первого объекта
    @param rec_id_1: идентификатор первого объекта
    @param object_id_2: идентификатор типа второго объекта
    @param rec_id_2: идентификатор второго объекта
    @param depth: глубина поиска саязей
    @return: список связей в формате [{key_id, val, sec},...,{}]
    """
    value = Manager().dict()
    process_1 = Process(target=get_objects_process, args=(group_id, object_id_1, rec_id_1, depth, value))
    process_2 = Process(target=get_objects_process, args=(group_id, object_id_2, rec_id_2, depth, value))
    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()
    objects_1 = value[str(object_id_1) + '_' + str(rec_id_1)]
    objects_2 = value[str(object_id_2) + '_' + str(rec_id_2)]
    temp_result = []
    for object_1 in objects_1:
        if objects_2.get(object_1):
            if len(objects_1[object_1]['path']) > 0 and len(objects_2[object_1]['path']) > 0:
                if objects_1[object_1]['path'][-1] == objects_2[object_1]['path'][-1]:
                    continue
            if len([item for item in objects_1[object_1]['path'] if
                    item['object_id'] == object_id_2 and item['rec_id'] == rec_id_2]) == 0 and len(
                [item for item in objects_2[object_1]['path'] if
                 item['object_id'] == object_id_1 and item['rec_id'] == rec_id_1]) == 0:
                temp_result += objects_1[object_1]['path'] + objects_2[object_1]['path'] + \
                               [{'object_id': objects_1[object_1]['object_id'],
                                 'rec_id': objects_1[object_1]['rec_id']}]
    result = [dict(s) for s in set(frozenset(d.items()) for d in temp_result)]
    return result


def get_relations_list():
    """
    Функция для получения списка связей
    @return: список в формате [{id,title,hint,list},...,{}]
    """
    result = []
    for item in get_relation_keys():
        list_id = None
        if item.get('list_id'):
            relation_type = {'title': 'list', 'value': item.get('list_id')}
            list_id = item.get('list_id')
        else:
            relation_type = {'title': 'unknow', 'value': None}
        result.append({'id': item['id'], 'title': item['title'], 'hint': item['hint'], 'list': list_id,
                       'type': relation_type, 'object_id_1': item['rel_obj_1_id'], 'object_id_2': item['rel_obj_2_id'],
                       'blocked_blank': item['blocked_blank']})
    return result
