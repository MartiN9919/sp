from data_base_driver.connect.connect_manticore import db_shinxql


def get_sphinxql(object_1_type, object_1_id, object_2_type, object_2_id):
    """
    Вспомогательная функция для формирования запроса sphinxql нахождения связи между двумя конкретными объектами
    @param object_1_type: тип первого объекта
    @param object_1_id: идентификационный номер первого объекта
    @param object_2_type: тип второго объекта
    @param object_2_id: идентификационный номер второго объекта
    @return: строка запроса
    """
    return 'SELECT id FROM rel WHERE MATCH(\'@obj_id_1 ' + str(object_1_type) + ' ' \
                                                                                '@rec_id_1 ' + str(object_1_id) + ' ' \
                                                                                                                  '@obj_id_2 ' + str(
        object_2_type) + ' ' \
                         '@rec_id_2 ' + str(object_2_id) + '\');'


def get_sphinxql_with_key(key_id, object_1_type, object_1_id, object_2_type, object_2_id):
    """
    Вспомогательная функция для формирования запроса sphinxql нахождения связи между двумя конкретными объектами
    @param key_id: тип связи
    @param object_1_type: тип первого объекта
    @param object_1_id: идентификационный номер первого объекта
    @param object_2_type: тип второго объекта
    @param object_2_id: идентификационный номер второго объекта
    @return: строка запроса
    """
    return 'SELECT id FROM rel WHERE MATCH(\'@key_id ' + str(key_id) + ' '\
                                               '@obj_id_1 ' + str(object_1_type) + ' ' \
                                               '@rec_id_1 ' + str(object_1_id) + ' ' \
                                               '@obj_id_2 ' + str(object_2_type) + ' ' \
                                               '@rec_id_2 ' + str(object_2_id) + '\');'


def search_rel(object_1_type, object_1_id, object_2_type, object_2_id):
    """
    Функция для поиска связей между двумя конкретными объектами
    @param object_1_type: тип первого объекта
    @param object_1_id: идентификационный номер первого объекта
    @param object_2_type: тип второго объекта
    @param object_2_id: идентификационный номер второго объекта
    @return: список идентификационных номеров объектов
    """
    result = set(db_shinxql(get_sphinxql(object_1_type, object_1_id, object_2_type, object_2_id)))
    result = result.union(set(db_shinxql(get_sphinxql(object_2_type, object_2_id, object_1_type, object_1_id))))
    return [item[0] for item in list(result)]


def search_rel_with_key(rel_key, object_1_type, object_1_id, object_2_type, object_2_id):
    """
    Функция для поиска связей между двумя конкретными объектами
    @param rel_key: тип связи
    @param object_1_type: тип первого объекта
    @param object_1_id: идентификационный номер первого объекта
    @param object_2_type: тип второго объекта
    @param object_2_id: идентификационный номер второго объекта
    @return: список идентификационных номеров объектов
    """
    result = set(db_shinxql(get_sphinxql_with_key(rel_key, object_1_type, object_1_id, object_2_type, object_2_id)))
    result = result.union(set(db_shinxql(get_sphinxql_with_key(rel_key, object_2_type, object_2_id, object_1_type, object_1_id))))
    return [item[0] for item in list(result)]


def get_rel_with_object(object_type, object_id):
    """
    функция для получения всех связей для одного объекта
    @param object_type: тип объекта
    @param object_id: идентификационный номер объекта
    @return: список кортежей в формате [(rel_id,date,obj_id1,rec_id1,obj_id2,rec_id2),(),...,()]
    """
    sql = 'SELECT key_id, dat, obj_id_1, rec_id_1, obj_id_2, rec_id_2 FROM rel WHERE MATCH(' \
          '\'@obj_id_1 ' + str(object_type) + ' @rec_id_1 ' + str(object_id) + '\');'
    result = set(db_shinxql(sql))
    sql = 'SELECT key_id, dat, obj_id_1, rec_id_1, obj_id_2, rec_id_2 FROM rel WHERE MATCH(' \
          '\'@obj_id_2 ' + str(object_type) + ' @rec_id_2 ' + str(object_id) + '\');'
    result2 = set(db_shinxql(sql))
    result = result.union(result2)
    return [(item[0], item[1], item[2], item[3], item[4], item[5]) for item in list(result)]
