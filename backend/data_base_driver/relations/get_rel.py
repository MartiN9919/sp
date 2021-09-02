import datetime

from data_base_driver.additional_functions import get_date_time_from_sec
from data_base_driver.record.find_object import find_reliable_http
from data_base_driver.record.get_record import get_object_record_by_id_http
from data_base_driver.relations.find_rel import search_rel_with_key_http
from data_base_driver.input_output.input_output import io_get_rel_tuple
from data_base_driver.sys_key.get_key_dump import get_keys_by_rel
from data_base_driver.sys_key.get_list import get_list_by_top_id
from data_base_driver.sys_key.get_object_dump import get_object_by_name


def get_rel_by_object(group_id, object, id, parents):
    """
    вспомогательная функция получения связей с определенной записью таблицы событий-связей,
    точка входа get_rel_cascade
    :@param object: id или имя типа объекта
    :@param id: id объекта в базе данных
    :@param parents: уже участвующие в линии связи
    :@return: объект и его связи в формате {record_id, object_id, params, rels:[{},...,{}]}
    """
    if not (isinstance(object, int)) and not (object.isdigit()):
        object = get_object_by_name(object)['id']
    rels = io_get_rel_tuple(group_id, [], [int(object), id], [], [], {}, True)
    first_data = [{'object_id': rel[2], 'rel_type': rel[0], 'val': rel[6], 'rec_id': rel[3], 'sec': rel[1],
                   'params': get_object_record_by_id_http(rel[2], rel[3])['params']} for rel in rels if
                  (rel[4] == object and rel[5] == id) and len(
                      [temp for temp in parents if int(temp[0]) == rel[2] and temp[1] == rel[3]]) == 0]
    second_data = [{'object_id': rel[4], 'rel_type': rel[0], 'val': rel[6], 'rec_id': rel[5], 'sec': rel[1],
                    'params': get_object_record_by_id_http(rel[4], rel[5])['params']} for rel in rels if
                   (rel[2] == object and rel[3] == id) and len(
                       [temp for temp in parents if int(temp[0]) == rel[4] and temp[1] == rel[5]]) == 0]
    relations = []
    for relation in first_data + second_data:
        old_relation = [item for item in relations if relation['object_id'] == item['object_id'] and
                        relation['rec_id'] == item['rec_id']]
        if len(old_relation) > 0:
            temp_relation = [item for item in old_relation[0]['relations'] if item['id'] == relation['rel_type']]
            if len(temp_relation) > 0:
                temp_relation[0]['values'].append({'val': relation['val'], 'sec': relation['sec']})
            else:
                old_relation[0]['relations'].append({'id': relation['rel_type'], 'values': [{ 'val': relation['val'],
                                                     'date': get_date_time_from_sec(relation['sec'])[:-3]}]})
        else:
            relations.append(
                {'object_id': relation['object_id'], 'rec_id': relation['rec_id'], 'params': relation['params'],
                 'relations': [{'id': relation['rel_type'],
                                'values': [{'val': relation['val'],
                                            'date': get_date_time_from_sec(relation['sec'])[:-3]}]}]})
    return {'object_id': object, 'relations': [], 'rec_id': id,
            'params': get_object_record_by_id_http(object, id)['params'],
            'rels': relations}


def get_rel_rec(group_id, rels, depth, parents):
    """
    вспомогательная функция рекурсивного обхода по графу связей, точка входа get_rel_cascade
    :@param rels: связи уже найденные на данном шаге
    :@param depth: глубина рекурсии на данном шаге
    :@param parents: связи уже встреченные в графе
    :@return: функция производит до запись в rels по ссылке и не возвращает значения
    """
    if depth == 0 or len(rels) == 0: return rels
    for rel in rels:
        newParents = parents.copy()
        newRels = get_rel_by_object(group_id, rel['object_id'], rel['rec_id'], newParents)
        newParents.append([newRels['object_id'], newRels['rec_id']])
        get_rel_rec(group_id, newRels['rels'], depth - 1, newParents)
        if rel.get('rels'):
            rel['rels'].append(newRels['rels'])
        else:
            rel['rels'] = newRels['rels']


def get_rel_cascade(group_id, object, id, depth):
    """
    функция каскадного обхода графа связей, является точкой входа для получения графа связей
    :@param object: id или имя типа объекта
    :@param id: id объекта
    :@param depth: глубина рекурсивного обхода, чем больше тем больше найденных связей
    :@return: список связей в формате {record_id, object_id, params, rels:[{},...,{}]}
    """
    if depth <= 0: return []
    rels = get_rel_by_object(group_id, object, id, parents=[])
    get_rel_rec(group_id, rels['rels'], depth - 1, parents=[[rels['object_id'], rels['rec_id']]])
    return rels


def get_object_relation(group_id, object_id, rec_id, objects):
    """
    Функция получения всех связей для объекта, с учетом уже имеющихся объектов
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param objects: список объектов связи с которыми требуются в результате
    @return: список словарей в формате [{object_id, rec_id, params, relations:[{key_id, sec, val},...,{}]},...,{}]
    """
    if len(objects) == 0:
        return []
    result = []
    temp_result = get_rel_cascade(group_id, object_id, rec_id, 1)['rels']
    for temp in temp_result:
        if len([item for item in objects if item['object_id'] == temp['object_id'] and
                item['rec_id'] == temp['rec_id']]) > 0:
            temp.pop('params')
            result.append(temp)
    return result


def get_objects_relation(group_id, object_id_1, rec_id_1, object_id_2, rec_id_2):
    """
    Функция для получения связей между двумя объектами
    @param group_id: идентификатор группы пользователя
    @param object_id_1: идентификатор типа первого объекта
    @param rec_id_1: идентификатор первого объекта
    @param object_id_2: идентификатор типа второго объекта
    @param rec_id_2: идентификатор второго объекта
    @return: список связей в формате [{key_id, val, sec},...,{}]
    """
    object_relation = get_rel_cascade(group_id, object_id_1, rec_id_1, 1)['rels']
    result = [item['relations'] for item in object_relation if
              item['object_id'] == object_id_2 and item['rec_id'] == rec_id_2]
    if len(result) > 0:
        return result[0]
    else:
        return []


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
        temp = get_object_record_by_id_http(object_id, rec_id)
        temp['rels'] = []
        temp['key_id'] = []
        temp['checked'] = True
        for result in temp_result:
            temp['key_id'].append(int(result['key_id']))
        root['rels'].append(temp)


def search_relations_recursive(group_id, request, parent, root):
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
        if len(relation.get('request', '')) != 0:
            rec_ids = find_reliable_http(relation.get('object_id'), relation.get('request', ''),
                                         relation.get('actual'), group_id)
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
                    temp = get_object_record_by_id_http(relation.get('object_id'), rec_id, group_id)
                    temp['rels'] = []
                    temp['key_id'] = []
                    for result in temp_result:
                        temp['key_id'].append(int(result['key_id']))
                    parent['rels'].append(temp)
                    check_relation(root, temp.get('object_id'), temp.get('rec_id'))
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
            for rec_id in rec_ids:
                old_result = [item for item in parent['rels'] if item['rec_id'] == rec_id['rec_id']]
                if len(old_result) == 1:
                    old_result[0]['key_id'].append(rec_id['key_id'])
                temp = get_object_record_by_id_http(relation.get('object_id'), int(rec_id['rec_id']))
                temp['rels'] = []
                temp['key_id'] = [int(rec_id['key_id'])]
                parent['rels'].append(temp)
                check_relation(root, temp.get('object_id'), temp.get('rec_id'))
        if len(relation.get('rels', [])) > 0:
            for temp_parent in parent['rels']:
                search_relations_recursive(group_id, relation, temp_parent, root)
    return parent


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
        return get_rel_cascade(group_id, request.get('object_id'), request.get('rec_id'), 1)
    else:
        parent = get_object_record_by_id_http(request.get('object_id'), request.get('rec_id'))
        parent['rels'] = []
        return search_relations_recursive(group_id, request, parent, parent)['rels']


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



# request = {'object_id': 35, 'rec_id': 1, 'rel': None, 'rels': [
#     {'object_id': 35, 'rel': {'id': 0, 'value': 0, 'date_time_start': None, 'date_time_end': '2021-07-20 12:00'},
#      'request': '', 'actual': True, 'rels': []},
#     {'object_id': 45, 'rel': {'id': 1102, 'value': 0, 'date_time_start': None, 'date_time_end': '2021-07-20 12:00'},
#      'request': 'АД', 'actual': False, 'rels': [
#         {'object_id': 30, 'rel': {'id': 0, 'value': 0, 'date_time_start': None, 'date_time_end': '2021-07-20 12:00'},
#          'request': '', 'actual': False, 'rels': []}
#     ]}
# ]}
#
#
# a = search_relations(1, request)
# c = get_object_relation(1,  35, 1, [{'object_id': 35, 'rec_id': 2}])
# b = 12
