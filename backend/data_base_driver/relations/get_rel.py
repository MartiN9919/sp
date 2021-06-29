from data_base_driver.full_text_search.sphinxql.find_rel import get_relations_with_object
from data_base_driver.sys_key.get_object_dump import get_object_by_id
from data_base_driver.sys_key.get_object_dump import get_object_by_name


def get_rel_by_object(group_id, object, id, parents):
    """
    вспомогательная функция получения связей с определенной записью таблицы событий-связей,
    точка входа get_rel_cascade
    :param object: id или имя типа объекта
    :param id: id объекта в базе данных
    :param parents: уже участвующие в линии связи
    :return: список связей в формате [record,id[ [object1,id1],[object2,id2],...,[objectN,idN]]]
    """
    if not (isinstance(object, int)) and not (object.isdigit()):
        object = get_object_by_name(object)['id']
    # rels = io_get_rel(group_id=group_id, keys=[], obj_rel_1=None, obj_rel_2=[int(object), id], where_dop=[],
    #                   is_unique=False)
    rels = get_relations_with_object(int(object), id)
    first_data = [{'object_type': rel[2], 'rel_type': rel[0], 'rec_id': rel[3]} for rel in rels if
                  (rel[4] == object and rel[5] == id) and len(
                      [temp for temp in parents if int(temp[0]) == rel[2] and temp[1] == rel[3]]) == 0]
    second_data = [{'object_type': rel[4], 'rel_type': rel[0], 'rec_id': rel[5]} for rel in rels if
                   (rel[2] == object and rel[3] == id) and len(
                       [temp for temp in parents if int(temp[0]) == rel[4] and temp[1] == rel[5]]) == 0]
    return {'object_type': get_object_by_id(object)['id'], 'rel_type': 'parent', 'rec_id': id,
            'rels': first_data + second_data}


def get_rel_rec(group_id, rels, depth, parents):
    """
    вспомогательная функция рекурсивного обхода по графу связей, точка входа get_rel_cascade
    :param rels: связи уже найденные на данном шаге
    :param depth: глубина рекурсии на данном шаге
    :param parents: связи уже встреченные в графе
    :return: функция производит до запись в rels по ссылке и не возвращает значения
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
    :param object: id или имя типа объекта
    :param id: id объекта
    :param depth: глубина рекурсивного обхода, чем больше тем больше найденных связей
    :return: список связей в формате [record,id [o,i[]...[]],[],..,[] ]
    """
    if depth <= 0: return []
    rels = get_rel_by_object(group_id, object, id, parents=[])
    get_rel_rec(group_id, rels['rels'], depth - 1, parents=[[rels['object_type'], rels['rec_id']]])
    return rels


def get_rel_rec_find(group_id, rels, depth, parents, searchedObject, searchedId):
    """
    вспомогательная функция рекурсивного обхода поиска, аналогична get_rel_by_object, за исключением выхода при нахождении
    связи с целевым объектом, точка входа get_rel_with_object
    :param rels: уже найденные на данном шаге связи
    :param depth: глибина рекурсии на данном шаге
    :param parents: уже встреченные в графе связи
    :param searchedObject: тип искомого объекта
    :param searchedId: id искомого объекта
    :return: возвращает True при обнаружении искомого объекта и None при отсутствии связи
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
    :param rels: граф связей
    :param path: уже построенный путь на данном ребре графа
    :return: кортеж из состояния выполнения True/False  и списка связей в формате [[record,id],[object1,id1],...,[objectN,idN]]
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
    :param object: id или имя типа связи начального объекта
    :param id: id начального объекта
    :param searchedObject: id или имя типа связи искомого объекта
    :param searchedId: id искомого объекта
    :param depth: глубина рекурсии поиска, по умолчанию 10
    :return: кортеж из состояния выполнения True/False  и списка связей в формате [[record,id],[object1,id1],...,[objectN,idN]]
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
