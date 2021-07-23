import datetime

from data_base_driver.constants.fulltextsearch import FullTextSearch
from data_base_driver.full_text_search.http_api.find_object import get_object_record_by_id_http, find_reliable_http
from data_base_driver.full_text_search.http_api.find_rel import get_relations_with_object_http, search_rel_with_key_http
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
    # rels = io_get_rel(group_id=group_id, keys=[], obj_rel_1=None, obj_rel_2=[int(object), id], where_dop=[],
    #                   is_unique=False)
    rels = get_relations_with_object_http(int(object), id)
    first_data = [{'object_type': rel[2], 'rel_type': rel[0], 'rec_id': rel[3],
                   'params': get_object_record_by_id_http(rel[2], rel[3])['params']} for rel in rels if
                  (rel[4] == object and rel[5] == id) and len(
                      [temp for temp in parents if int(temp[0]) == rel[2] and temp[1] == rel[3]]) == 0]
    second_data = [{'object_type': rel[4], 'rel_type': rel[0], 'rec_id': rel[5],
                    'params': get_object_record_by_id_http(rel[4], rel[5])['params']} for rel in rels if
                   (rel[2] == object and rel[3] == id) and len(
                       [temp for temp in parents if int(temp[0]) == rel[4] and temp[1] == rel[5]]) == 0]
    return {'object_type': object, 'rel_type': 'parent', 'rec_id': id,
            'params': get_object_record_by_id_http(object, id)['params'],
            'rels': first_data + second_data}


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
        newRels = get_rel_by_object(group_id, rel['object_type'], rel['rec_id'], newParents)
        newParents.append([newRels['object_type'], newRels['rec_id']])
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
    get_rel_rec(group_id, rels['rels'], depth - 1, parents=[[rels['object_type'], rels['rec_id']]])
    return rels


def get_rel_rec_find(group_id, rels, depth, parents, searchedObject, searchedId):
    """
    вспомогательная функция рекурсивного обхода поиска, аналогична get_rel_by_object, за исключением выхода при нахождении
    связи с целевым объектом, точка входа get_rel_with_object
    :@param rels: уже найденные на данном шаге связи
    :@param depth: глибина рекурсии на данном шаге
    :@param parents: уже встреченные в графе связи
    :@param searchedObject: тип искомого объекта
    :@param searchedId: id искомого объекта
    :@return: возвращает True при обнаружении искомого объекта и None при отсутствии связи
    """
    if depth == 0 or len(rels) == 0: return rels
    for rel in rels:
        newParents = parents.copy()
        newRels = get_rel_by_object(group_id, rel[0], rel[2], newParents)
        if len(newRels[3]) != 0:
            mas = [t for t in newRels[3] if
                   int(get_object_by_name(t[0])['id']) == searchedObject and t[2] == searchedId]
            if len(mas) > 0:
                rel.append(mas)
                return True
        newParents.append([newRels[0], newRels[2]])
        rel.append(newRels[3])
        if get_rel_rec_find(newRels[3], depth - 1, newParents, searchedObject, searchedId):
            return True


def getRelPath(rels, path=[]):
    """
    вспомогательная функция для возвращения точного пути между связанными объектами, точка входа get_rel_with_object
    :@param rels: граф связей
    :@param path: уже построенный путь на данном ребре графа
    :@return: кортеж из состояния выполнения True/False  и списка связей в формате [[record,id],[object1,id1],...,[objectN,idN]]
    """
    if len(rels) <= 3:
        return False, ''
    if len(rels[3]) == 0:
        return False, ''
    for rel in rels[3]:
        newPath = path.copy()
        if len(rel) == 3:
            newPath.append([rel[0], rel[1], rel[2]])
            return True, newPath
        newPath.append([rel[0], rel[1], rel[2]])
        res, resultPath = getRelPath(rel, newPath)
        if res:
            return True, resultPath
    return False, ''


def get_rel_with_object(group_id, object, id, searchedObject, searchedId, depth):
    """
    функция для писка связи между двумя объектами
    :@param object: id или имя типа связи начального объекта
    :@param id: id начального объекта
    :@param searchedObject: id или имя типа связи искомого объекта
    :@param searchedId: id искомого объекта
    :@param depth: глубина рекурсии поиска, по умолчанию 10
    :@return: кортеж из состояния выполнения True/False  и списка связей в формате [[record,id],[object1,id1],...,[objectN,idN]]
    """
    if not (isinstance(searchedObject, int)) and not (searchedObject.isdigit()):
        searchedObject = get_object_by_name(searchedObject)['id']
    rels = get_rel_by_object(group_id, object, id)
    mas = [t for t in rels[3] if t[0] == searchedObject and t[2] == searchedId]
    if len(mas) > 0:
        return rels
    if get_rel_rec_find(group_id, rels[3], depth, parents=[[rels[0], rels[2]]], searchedObject=searchedObject,
                        searchedId=searchedId):
        return getRelPath(rels, [[object, 'parent', id]])
    else:
        return False


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
                                           mode=2
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
            rec_ids = find_reliable_http(FullTextSearch.TABLES[relation.get('object_id')], relation.get('request', ''),
                                         relation.get('actual'))
            for rec_id in rec_ids:
                temp_result = search_rel_with_key_http(relation.get('rel').get('id'),
                                                       parent.get('object_id'),
                                                       parent.get('rec_id'),
                                                       relation.get('object_id'),
                                                       rec_id,
                                                       relation.get('rel').get('value'),
                                                       relation.get('rel').get('date_time_start'),
                                                       relation.get('rel').get('date_time_end'),
                                                       mode=2
                                                       )
                if len(temp_result) > 0:
                    temp = get_object_record_by_id_http(relation.get('object_id'), rec_id)
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
                                               mode=2
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
        return search_relations_recursive(group_id, request, parent, parent)


# request = {'object_id': 35, 'rec_id': 1, 'rel': None, 'rels': [
#     {'object_id': 35, 'rel': {'id': 0, 'value': 0, 'date_time_start': None, 'date_time_end': '2021-07-20 12:00'},
#      'request': '', 'actual': True, 'rels': []},
#     {'object_id': 45, 'rel': {'id': 1102, 'value': 0, 'date_time_start': None, 'date_time_end': '2021-07-20 12:00'},
#      'request': 'АД', 'actual': True, 'rels': [
#         {'object_id': 30, 'rel': {'id': 0, 'value': 0, 'date_time_start': None, 'date_time_end': '2021-07-20 12:00'},
#          'request': '', 'actual': False, 'rels': []}
#     ]}
# ]}
# a = search_relations(0, request)
# b = 12
