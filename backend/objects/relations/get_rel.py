import datetime
from multiprocessing import Process, Manager

from data_base_driver.additional_functions import get_date_time_from_sec
from objects.record.find_object import find_reliable_http
from objects.record.get_record import get_object_record_by_id_http
from data_base_driver.input_output.input_output import io_get_rel
from data_base_driver.sys_key.get_key_dump import get_relation_keys
from data_base_driver.sys_key.get_list import get_item_list_value
from data_base_driver.sys_key.get_object_dump import get_object_by_name
from objects.relations.find_rel import search_rel_with_key_http


def get_rel_by_object(group_id, object, id, parents):
    """
    вспомогательная функция получения связей с определенной записью таблицы событий-связей,
    точка входа get_rel_cascade
    @param object: id или имя типа объекта
    @param id: id объекта в базе данных
    @param parents: уже участвующие в линии связи
    @return: объект и его связи в формате {record_id, object_id, rels:[{},...,{}]}
    """
    if not (isinstance(object, int)) and not (object.isdigit()):
        object = get_object_by_name(object)['id']
    rels = io_get_rel(group_id, [], [int(object), id], [], [], {}, True)
    temp_relations = []
    for rel in rels:
        s1, s2 = ('1', '2') if rel['obj_id_2'] == object and rel['rec_id_2'] == id else ('2', '1')
        if len([temp for temp in parents if
                int(temp[0]) == rel['obj_id_' + s1] and temp[1] == rel['rec_id_' + s1]]) == 0:
            temp_relations.append({
                'rel_type': rel['key_id'],
                'val': rel['val'],
                'sec': rel['sec'],
                'id': rel['id'],
                'doc': rel['document_id'],
                'object_id': rel['obj_id_' + s1],
                'rec_id': rel['rec_id_' + s1]
            })
    relations = []
    for relation in temp_relations:
        doc = get_object_record_by_id_http(20, relation['doc'], group_id, []) if relation['doc'] != 0 else None
        old_relation = [item for item in relations if relation['object_id'] == item['object_id'] and
                        relation['rec_id'] == item['rec_id']]
        if len(old_relation) > 0:
            temp_relation = [item for item in old_relation[0]['relations'] if item['id'] == relation['rel_type']]
            if len(temp_relation) > 0:
                temp_relation[0]['values'].append(
                    {'value': get_item_list_value(int(relation['val'])) if relation['val'] != 0 else '',
                     'date': get_date_time_from_sec(relation['sec'])[:-3], 'doc': doc})
            else:
                old_relation[0]['relations'].append({'id': relation['rel_type'],
                                                     'values': [{'value': get_item_list_value(int(relation['val'])) if
                                                     relation['val'] != 0 else '',
                                                                 'date': get_date_time_from_sec(relation['sec'])[:-3]}],
                                                     'doc': doc})
        else:
            relations.append(
                {'object_id': relation['object_id'], 'rec_id': relation['rec_id'],
                 'relations': [{'id': relation['rel_type'],
                                'values': [
                                    {'value': get_item_list_value(int(relation['val'])) if relation['val'] != 0 else '',
                                     'date': get_date_time_from_sec(relation['sec'])[:-3], 'doc': doc}]}]})
    for relation in relations:
        for sub_relation in relation['relations']:
            sub_relation['values'].sort(key=lambda x: x['date'], reverse=True)
    return {'object_id': object, 'relations': [], 'rec_id': id, 'rels': relations}


def get_rel_rec(group_id, rels, depth, parents):
    """
    Вспомогательная функция рекурсивного обхода по графу связей, точка входа get_rel_cascade
    @param group_id: идентификатор группы пользователя
    @param rels: связи уже найденные на данном шаге
    @param depth: глубина рекурсии на данном шаге
    @param parents: связи уже встреченные в графе
    @return: функция производит дозапись в rels по ссылке и не возвращает значения
    """
    if depth == 0 or len(rels) == 0:
        return rels
    for rel in rels:
        new_parents = parents.copy()
        new_rels = get_rel_by_object(group_id, rel['object_id'], rel['rec_id'], new_parents)
        new_parents.append([new_rels['object_id'], new_rels['rec_id']])
        get_rel_rec(group_id, new_rels['rels'], depth - 1, new_parents)
        if rel.get('rels'):
            rel['rels'].append(new_rels['rels'])
        else:
            rel['rels'] = new_rels['rels']


def get_rel_cascade(group_id, object, id, depth):
    """
    функция каскадного обхода графа связей, является точкой входа для получения графа связей
    @param object: id или имя типа объекта
    @param id: id объекта
    @param depth: глубина рекурсивного обхода, чем больше тем больше найденных связей
    @return: список связей в формате {record_id, object_id, params, rels:[{},...,{}]}
    """
    if depth <= 0:
        return []
    rels = get_rel_by_object(group_id, object, id, parents=[])
    get_rel_rec(group_id, rels['rels'], depth - 1, parents=[[rels['object_id'], rels['rec_id']]])
    return rels


def get_related_objects(group_id, object_id, rec_id, keys, values, time_interval, result_object_type=0):
    """
    Функия для получения списка объектов свзанных с искомым по заданным характеристикам
    @param group_id: идентфификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param keys: список идентификаторов типов связей, если любые то пустой список
    @param values: список идентификаторов значений связей, если любые то пустой список
    @param time_interval: временной интервал установления связи в формате {second_start,second_end}
    @param result_object_type: идентификатор типа результирующего объекта для фильтрации, если любой то 0
    @return: список словарей в формате [{object_id, rec_id},...,{}]
    """
    temp_object = [] if result_object_type == 0 else [result_object_type]
    relations = io_get_rel(group_id, keys, [object_id, rec_id], temp_object, values, time_interval, True)
    result = []
    for relation in relations:
        if int(relation['obj_id_1']) == object_id and int(relation['rec_id_1']) == rec_id:
            result.append({'object_id': int(relation['obj_id_2']), 'rec_id': int(relation['rec_id_2']),
                           'key_id': int(relation['key_id']), 'val': relation['val']})
        else:
            result.append({'object_id': int(relation['obj_id_1']), 'rec_id': int(relation['rec_id_1']),
                           'key_id': int(relation['key_id']), 'val': relation['val']})
    result = [dict(s) for s in set(frozenset(d.items()) for d in result)]
    return result


def get_object_relation(group_id, object_id, rec_id, objects, all=False):
    """
    Функция получения всех связей для объекта, с учетом уже имеющихся объектов
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param objects: список объектов связи с которыми требуются в результате
    @param all: флаг для получения всех связей
    @return: список словарей в формате [{object_id, rec_id, params, relations:[{key_id, sec, val},...,{}]},...,{}]
    """
    if len(objects) == 0 and not all:
        return []
    result = []
    temp_result = get_rel_cascade(group_id, object_id, rec_id, 1)['rels']
    for temp in temp_result:
        if len([item for item in objects if item['object_id'] == temp['object_id'] and
                                            item['rec_id'] == temp['rec_id']]) > 0 or all:
            result.append(temp)
    return result


def check_relation(root, object_id, rec_id):
    """
    Функция для проверки нового объекта на связи с уже имеющимися в дереве
    @param root: корень дерева на данной итерации рекурсии
    @param object_id: тип нового объекта
    @param rec_id: идентификатор нового объекта
    @return: ничего не возвращает
    """
    for relation in root['rels']:
        check_relation(relation, object_id, rec_id)
    if len([item for item in root['rels'] if
            item['object_id'] == object_id and item['rec_id'] == rec_id]) > 0 or root.get('checked', False):
        return
    temp_result = search_rel_with_key_http(0,
                                           object_id,
                                           rec_id,
                                           root.get('object_id'),
                                           root.get('rec_id'),
                                           0,
                                           None,
                                           datetime.datetime.now().isoformat(sep=' ')[:16],
                                           )
    if len(temp_result) > 0:
        temp = {'object_id': object_id, 'rec_id': rec_id}
        temp['rels'] = []
        temp['checked'] = True
        root['rels'].append(temp)


def remove_path(parent, child):
    """
    Вспомогательная функция для обозначения вырожденных веток дерева поиска
    @param parent: родитель на данной итерации рекурсии
    @param child: наследник на данной итерации рекурсии
    """
    if not child.get('degenerated'):
        child['degenerated'] = 0
    child['degenerated'] += 1
    if parent and parent.get('parent'):
        remove_path(parent['parent'], parent)


def search_relations_recursive(group_id, request, parent, root):  # НЕОБХОДИМО ПОЧИНИТЬ БАГ С НЕПРАВИЛЬНОЙ ДЕГРАДАЦИЕЙ
    """
    Функция для рекурсивного построения дерева связей по запросу
    @param group_id: идентификатор группы пользователя
    @param request: запрос в формате:
        {object_id, rec_id, rels:[
            {object_id, rel:{id, value, date_time_start, date_time_end}, request, actual, rels:[{},{},...,{}]},
            {},
            ...,
            {}
        ]}
    @param parent: родительский корень для данной итерации
    @param root: главный корень дерева
    @return: на каждой итерации возвращает родительский корень с возможным добавлением к нему новый найденных связей
    """
    for relation in request.get('rels', []):
        temp_list = []
        if len(relation.get('request', '')) != 0:
            rec_ids = find_reliable_http(relation.get('object_id'), relation.get('request', ''),
                                         relation.get('actual'), group_id)
            fl = False
            for rec_id in rec_ids:
                temp_result = search_rel_with_key_http(relation.get('rel').get('id'),
                                                       parent.get('object_id'),
                                                       parent.get('rec_id'),
                                                       relation.get('object_id'),
                                                       rec_id,
                                                       relation.get('rel').get('value'),
                                                       relation.get('rel').get('date_time_start'),
                                                       relation.get('rel').get('date_time_end'),
                                                       group_id,
                                                       )
                if len(temp_result) > 0:
                    temp = {'object_id': relation.get('object_id'), 'rec_id': int(rec_id), 'rels': [], 'parent': parent}
                    parent['rels'].append(temp)
                    temp_list.append(temp)
                    fl = True
            if not fl:
                remove_path(parent.get('parent'), parent)
        else:
            rec_ids = search_rel_with_key_http(relation.get('rel').get('id'),
                                               relation.get('object_id'),
                                               0,
                                               parent.get('object_id'),
                                               parent.get('rec_id'),
                                               relation.get('rel').get('value'),
                                               relation.get('rel').get('date_time_start'),
                                               relation.get('rel').get('date_time_end'),
                                               group_id,
                                               )
            if len(rec_ids) == 0:
                remove_path(parent.get('parent'), parent)
            for rec_id in rec_ids:
                if len([item for item in temp_list if item['rec_id'] == int(rec_id['rec_id'])]) > 0:
                    continue
                temp = {'object_id': relation.get('object_id'), 'rec_id': int(rec_id['rec_id']), 'rels': [],
                        'parent': parent}
                parent['rels'].append(temp)
                temp_list.append(temp)
        if len(relation.get('rels', [])) > 0:
            for temp_parent in temp_list:
                temp_parent['rels_size'] = len(relation.get('rels', []))
                search_relations_recursive(group_id, relation, temp_parent, root)
    return parent


def get_unique_objects(object_tree, path=None, objects=None) -> list:
    """
    Функция для филтрации дерева объектов с занесением всех уникальных объектов в objects
    @param objects: результирующий список
    @param object_tree: дерево объетов построенное при поиске связей
    @param path: путь к объекту
    """
    if objects is None:
        objects = []
    if path is None:
        path = []
    for item in object_tree:
        if item.get('degenerated') and \
                item['degenerated'] >= item['rels_size'] and item['degenerated'] >= len(item['rels']):
            continue
        if len([temp for temp in objects if temp['object_id'] == item['object_id'] and
                                            temp['rec_id'] == item['rec_id']]) == 0:
            objects.append({'object_id': item['object_id'], 'rec_id': item['rec_id'], 'path': path})
        if len(item.get('rels', [])) != 0:
            new_path = path.copy()
            new_path.append({'object_id': item['object_id'], 'rec_id': item['rec_id']})
            get_unique_objects(item['rels'], new_path, objects)
    return objects


def get_unique_objects_dict(object_tree, path=None, objects=None) -> dict:
    """
    Функция для филтрации дерева объектов с занесением всех уникальных объектов в objects
    @param objects: результирующий словарь
    @param object_tree: дерево объетов построенное при поиске связей
    @param path: путь к объекту
    """
    if objects is None:
        objects = {}
    if path is None:
        path = []
    for item in object_tree:
        if item.get('degenerated') and \
                (item['degenerated'] >= len(item['rels'])):
            continue
        if len([temp for temp in objects.values() if temp['object_id'] == item['object_id'] and
                                                     temp['rec_id'] == item['rec_id']]) == 0:
            objects[str(item['object_id']) + '_' + str(item['rec_id'])] = {'object_id': item['object_id'],
                                                                           'rec_id': item['rec_id'], 'path': path}
        if len(item.get('rels', [])) != 0:
            new_path = path.copy()
            new_path.append({'object_id': item['object_id'], 'rec_id': item['rec_id']})
            get_unique_objects_dict(item['rels'], new_path, objects)
    return objects


def get_objects_process(group_id, object_id, rec_id, depth, value):
    """
    Функция для работы в отдельном процессе для поиска уникальных связанных объектов и путей к ним
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param depth: глубина поиска
    @param value: словарь для сохранения результата
    """
    object_relation = get_rel_cascade(group_id, object_id, rec_id, depth)
    value[str(object_id) + '_' + str(rec_id)] = get_unique_objects_dict(object_relation['rels'])


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


def search_relations(group_id, request):
    """
    Функция для поиска связей по запросу
    @param group_id: идентификатор группы пользователя
    @param request: запрос в формате:
        {object_id, rec_id, rels:[
            {object_id, rel:{id, value, date_time_start, date_time_end}, request, actual, rels:[{},{},...,{}]},
            {},
            ...,
            {}
        ]}
    @return: словарь в формате:
        {object_id, rec_id, params, rels:[
            {object_id, rec_id, params, rels:[{},{},...,{}]},
            {},
            ...,
            {}
        ]}
    """
    if len(request.get('rels')) == 0:
        result = get_unique_objects(
            get_rel_cascade(group_id, request.get('object_id'), request.get('rec_id'), 1)['rels'])
        return [item for item in result if item['object_id'] != 1]
    else:
        parent = {'object_id': request.get('object_id'), 'rec_id': request.get('rec_id')}
        parent['rels'] = []
        temp = search_relations_recursive(group_id, request, parent, parent)['rels']
        result = get_unique_objects(temp)
        result.append({'object_id': request.get('object_id'), 'rec_id': request.get('rec_id')})
        return [item for item in result if item['object_id'] != 1]


def get_relations_list():
    """
    Функция для получения списка возможных связей по типу связываемых объектов
    @param object1: имя или id первого объекта
    @param object2: имя или id второго объекта
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
                       'type': relation_type, 'object_id_1': item['rel_obj_1_id'], 'object_id_2': item['rel_obj_2_id']})
    return result
