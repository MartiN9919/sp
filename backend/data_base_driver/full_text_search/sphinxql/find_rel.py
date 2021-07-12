from data_base_driver.connect.connect_manticore import db_shinxql


def get_sphinxql_two_object_1(object_1_type, object_1_id, object_2_type, object_2_id, key_id=0, list_id=0):
    tmp = 'SELECT rec_id_1 FROM rel WHERE MATCH(\'@obj_id_1 ' + str(object_1_type) + ' ' \
                                                                            '@rec_id_1 ' + str(object_1_id) + ' ' \
                                                                            '@obj_id_2 ' + str(object_2_type) + ' ' \
                                                                            '@rec_id_2 ' + str(object_2_id)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    tmp += '\');'
    return tmp


def get_sphinxql_two_object_2(object_1_type, object_1_id, object_2_type, object_2_id, key_id=0, list_id=0):
    tmp = 'SELECT rec_id_2 FROM rel WHERE MATCH(\'@obj_id_1 ' + str(object_2_type) + ' ' \
                                                                            '@rec_id_1 ' + str(object_2_id) + ' ' \
                                                                            '@obj_id_2 ' + str(object_1_type) + ' ' \
                                                                            '@rec_id_2 ' + str(object_1_id)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    tmp += '\');'
    return tmp


def get_sphinxql_without_first_object_1(object_1_type, object_2_type, object_2_id, key_id=0, list_id=0):
    tmp = 'SELECT rec_id_1 FROM rel WHERE MATCH(\'@obj_id_1 ' + str(object_1_type) + ' ' \
                                                                            '@obj_id_2 ' + str(object_2_type) + ' ' \
                                                                            '@rec_id_2 ' + str(object_2_id)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    tmp += '\');'
    return tmp


def get_sphinxql_without_first_object_2(object_1_type, object_2_type, object_2_id, key_id=0, list_id=0):
    tmp = 'SELECT rec_id_2 FROM rel WHERE MATCH(\'@obj_id_2 ' + str(object_1_type) + ' ' \
                                                                            '@obj_id_1 ' + str(object_2_type) + ' ' \
                                                                            '@rec_id_1 ' + str(object_2_id)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    tmp += '\');'
    return tmp


def get_sphinxql_without_second_object_1(object_1_type, object_1_id, object_2_type, key_id=0, list_id=0):
    tmp = 'SELECT rec_id_1 FROM rel WHERE MATCH(\'@obj_id_1 ' + str(object_1_type) + ' ' \
                                                                            '@rec_id_1 ' + str(object_1_id) + ' ' \
                                                                            '@obj_id_2 ' + str(object_2_type)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    tmp += '\');'
    return tmp


def get_sphinxql_without_second_object_2(object_1_type, object_1_id, object_2_type, key_id=0, list_id=0):
    tmp = 'SELECT rec_id_2 FROM rel WHERE MATCH(\'@obj_id_2 ' + str(object_1_type) + ' ' \
                                                                            '@rec_id_2 ' + str(object_1_id) + ' ' \
                                                                            '@obj_id_1 ' + str(object_2_type)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    tmp += '\');'
    return tmp


def get_sphinxql_without_objects_1(object_1_type, object_2_type, key_id=0, list_id=0):
    tmp = 'SELECT rec_id_1 FROM rel WHERE MATCH(\'@obj_id_1 ' + str(object_1_type) + ' ' \
                                                                            '@obj_id_2 ' + str(object_2_type)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    tmp += '\');'
    return tmp


def get_sphinxql_without_objects_2(object_1_type, object_2_type, key_id=0, list_id=0):
    tmp = 'SELECT rec_id_2 FROM rel WHERE MATCH(\'@obj_id_1 ' + str(object_2_type) + ' ' \
                                                                            '@obj_id_2 ' + str(object_1_type)
    if key_id != 0:
        tmp += ' @key_id ' + str(key_id)
    if list_id != 0:
        tmp += ' @val ' + str(list_id)
    tmp += '\');'
    return tmp


def search_rel_with_key(rel_key, object_1_type, object_1_id, object_2_type, object_2_id, list_id):
    """
    Функция для поиска связей между двумя конкретными объектами
    @param rel_key: тип связи
    @param object_1_type: тип первого объекта
    @param object_1_id: идентификационный номер первого объекта
    @param object_2_type: тип второго объекта
    @param object_2_id: идентификационный номер второго объекта
    @param list_id: идентификационный в списке если есть
    @return: список идентификационных номеров объектов
    """
    if object_1_id != 0 and object_2_id != 0:
        result = set(
            db_shinxql(get_sphinxql_two_object_1(object_1_type, object_1_id, object_2_type, object_2_id,
                                                 rel_key, list_id)))
        result = result.union(set(db_shinxql(get_sphinxql_two_object_2(object_1_type, object_1_id, object_2_type,
                                                                   object_2_id, rel_key, list_id))))
    elif object_1_id == 0 and object_2_id != 0:
        result = set(
            db_shinxql(get_sphinxql_without_first_object_1(object_1_type, object_2_type, object_2_id,
                                                           rel_key, list_id)))
        result = result.union(set(db_shinxql(get_sphinxql_without_first_object_2(object_1_type, object_2_type,
                                                                                 object_2_id, rel_key, list_id))))
    elif object_1_id != 0 and object_2_id == 0:
        result = set(
            db_shinxql(get_sphinxql_without_second_object_1(object_1_type, object_1_id, object_2_type,
                                                            rel_key, list_id)))
        result = result.union(set(db_shinxql(get_sphinxql_without_second_object_2(object_1_type, object_1_id,
                                                                                  object_2_type, rel_key, list_id))))
    else:
        result = set(
            db_shinxql(get_sphinxql_without_objects_1(object_1_type, object_2_type, rel_key, list_id)))
        result = result.union(set(db_shinxql(get_sphinxql_without_objects_2(object_1_type, object_2_type,
                                                                            rel_key, list_id))))
    return [item[0] for item in list(result)]


def get_relations_with_object(object_type, object_id):
    """
    функция для получения всех связей для одного объекта
    @param object_type: тип объекта
    @param object_id: идентификационный номер объекта
    @return: список кортежей в формате [(rel_id,date,obj_id1,rec_id1,obj_id2,rec_id2),(),...,()]
    """
    sql = 'SELECT key_id, date, obj_id_1, rec_id_1, obj_id_2, rec_id_2 FROM rel WHERE MATCH(' \
          '\'@obj_id_1 ' + str(object_type) + ' @rec_id_1 ' + str(object_id) + '\');'
    result = set(db_shinxql(sql))
    sql = 'SELECT key_id, date, obj_id_1, rec_id_1, obj_id_2, rec_id_2 FROM rel WHERE MATCH(' \
          '\'@obj_id_2 ' + str(object_type) + ' @rec_id_2 ' + str(object_id) + '\');'
    result2 = set(db_shinxql(sql))
    result = result.union(result2)
    return [(int(item[0]), item[1], int(item[2]), int(item[3]), int(item[4]), int(item[5])) for item in list(result)]
