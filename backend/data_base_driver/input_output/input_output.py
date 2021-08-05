from data_base_driver.input_output.input_output_manticore import io_get_obj_row_manticore, io_get_obj_col_manticore, \
    io_get_rel_manticore
from data_base_driver.input_output.io_class import IO


def io_set(group_id, obj, data):
    """
    функция для добавление объекта в базу данных
    @param group_id: группа привилегий пользователя
    @param obj: тип добавляемого объекта
    @param data: вносимая информация об объекте в формате вложенного списков [[key1,value1],[key2,value2],...,[keyN,valueN]],
    для того что бы добавить значение уже существующему элементу необходимо передать по ключу id его идентификационный номер
    @return: кортеж где 0 элемент это статус выполнения True/False, 1 элемент - rec_id добавленного/дополненного объекта
    """
    return IO(group_id=group_id).set(
        obj=obj,
        data=data,
    )


def io_get_obj_generator(group_id, obj, keys=[], ids=[], ids_max_block=None, where_dop_row=[]):
    """
    Функция аналогична функции io_get_obj, за исключением типа возвращаемого значения, в данном случае возвращается
    генератор, а не кортеж
    """
    yield from IO(group_id=group_id).get_obj(
        obj=obj,
        keys=keys,
        ids=ids,
        ids_max_block=ids_max_block,
        where_dop_row=where_dop_row,
    )


def io_get_obj(group_id, obj, keys=[], ids=[], ids_max_block=None, where_dop_row=[]):
    """
    Функция для получения информации об объекте/объектах
    @param group_id: группа привилегий пользователя
    @param obj: тип искомого объекта/объектов
    @param keys: искомые типы значений для искомых объектов, если необходима вся информация передать пустой список
    @param ids: номер либо номера искомых объектов, если необходимы все, передать пустой список
    @param ids_max_block: максимальное количество найденных объектов
    @param where_dop_row: дополнительные sql фильтры если необходимы, передавать как список строк
    @return: список кортежей в формате ((rec_id1,key_id1,val1,date1),(),...,())
    """
    return tuple(IO(group_id=group_id).get_obj(
        obj=obj,
        keys=keys,
        ids=ids,
        ids_max_block=ids_max_block,
        where_dop_row=where_dop_row,
    ))


def io_get_obj_manticore_dict(group_id, object_type, keys, ids, ids_max_block, where_dop_row, time_interval):
    """
    Функция для получения информации о объекте из мантикоры в формате списка словарей
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта, формат int
    @param keys: список содержащий идентификаторы ключей
    @param ids: список содержащий идентификаторы объектов
    @param ids_max_block: максимальное количество записей в ответе
    @param where_dop_row: аргументы полнотекстового поиска (блок match запроса sphinx/manticore)
    @param time_interval: временной интервал записи в формате словаря с ключами second_start и second_end
    @return: список словарей в формате [{rec_id,sec,key_id,val},{},...,{}]
    """
    if not ids:
        ids = []
    if not keys:
        keys = []
    if not where_dop_row:
        where_dop_row = ''
    if not ids_max_block:
        ids_max_block = 1000
    if not time_interval:
        time_interval = {}
    row_records = io_get_obj_row_manticore(group_id, object_type, keys, ids, ids_max_block, where_dop_row,
                                           time_interval)
    col_records = io_get_obj_col_manticore(group_id, object_type, keys, ids, ids_max_block)
    result = row_records + col_records
    result.sort(key=lambda x: x['rec_id'])
    return result


def io_get_obj_manticore_tuple(group_id, object_type, keys, ids, ids_max_block, where_dop_row, time_interval):
    """
    Функция для получения информации о объекте из мантикоры в формате списка кортежей
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта, формат int
    @param keys: список содержащий идентификаторы ключей
    @param ids: список содержащий идентификаторы объектов
    @param ids_max_block: максимальное количество записей в ответе
    @param where_dop_row: аргументы полнотекстового поиска (блок match запроса sphinx/manticore)
    @param time_interval: временной интервал записи в формате словаря с ключами second_start и second_end
    @return: список словарей в формате [(rec_id,sec,key_id,val),(),...,()]
    """
    return [(item['rec_id'], int(item['sec']), item['key_id'], item['val'])
            for item in io_get_obj_manticore_dict(group_id,
                                                  object_type,
                                                  keys,
                                                  ids,
                                                  ids_max_block,
                                                  where_dop_row,
                                                  time_interval)]


def io_get_rel_generator(group_id, keys=[], obj_rel_1=None, obj_rel_2=None, where_dop=[]):
    """
    Функция аналогична функции io_get_rel, за исключением типа возвращаемого значения, в данном случае возвращается
    генератор, а не кортеж
    """
    yield from IO(group_id=group_id).get_rel(
        keys=keys,
        obj_rel_1=obj_rel_1,
        obj_rel_2=obj_rel_2,
        where_dop=where_dop,
    )


def io_get_rel(group_id, keys=[], obj_rel_1=None, obj_rel_2=None, where_dop=[], is_unique=False):
    """
    Функция для получения списка связей
    @param group_id: группа привилегий пользователя
    @param keys: типы связей, передавать в виде списка строк либо номеров
    @param obj_rel_1: тип и id первого связываемого объекта в формате [type,id]
    @param obj_rel_2: тип и id второго связываемого объекта в формате [type,id]
    @param where_dop: дополнительные параметры sql фильтры, передавать в виде списка строк
    @param is_unique: уникальна ли данная связь
    @return: список кортежей в формате ((rel_id,date,obj_id1,rec_id1,obj_id2,rec_id2),(),...,())
    """
    ret = tuple(IO(group_id=group_id).get_rel(
        keys=keys,
        obj_rel_1=obj_rel_1,
        obj_rel_2=obj_rel_2,
        where_dop=where_dop,
    ))
    if is_unique: ret = tuple(set(ret))
    return ret


def io_get_rel_manticore_dict(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique):
    """
    Функция для получения информации о связях в формате списка словарей
    @param group_id: идентификатор группы пользователя
    @param keys: список идентификаторов типов связей
    @param obj_rel_1: информация о первом объекте для связи в формате списка [object_type(int), rec_id(int)],
    может быть пустым или содержать только тип объекта
    @param obj_rel_2: информация о втором объекте для связи в формате списка [object_type(int), rec_id(int)]
    может быть пустым или содержать только тип объекта
    @param val: список с возможными идентификаторами значений закрепленных списков
    @param time_interval: словарь хранящий промежуток времени в секундах: {second_start, second_end}
    @param is_unique: флаг проверки результирующего списка на уникальность входящих элементов
    @return: список словарей в формате [{sec,key_id,obj_id_1,rec_id_1,obj_id_2,rec_id_2,val},{},...,{}]
    """
    if not keys:
        keys = []
    if not val:
        val = []
    if not time_interval:
        time_interval = {}
    return io_get_rel_manticore(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique)


def io_get_rel_manticore_tuple(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique):
    """
    Функция для получения информации о связях в формате списка кортежей
    @param group_id: идентификатор группы пользователя
    @param keys: список идентификаторов типов связей
    @param obj_rel_1: информация о первом объекте для связи в формате списка [object_type(int), rec_id(int)],
    может быть пустым или содержать только тип объекта
    @param obj_rel_2: информация о втором объекте для связи в формате списка [object_type(int), rec_id(int)]
    может быть пустым или содержать только тип объекта
    @param val: список с возможными идентификаторами значений закрепленных списков
    @param time_interval: словарь хранящий промежуток времени в секундах: {second_start, second_end}
    @param is_unique: флаг проверки результирующего списка на уникальность входящих элементов
    @return: список словарей в формате [(key_id,sec,obj_id_1,rec_id_1,obj_id_2,rec_id_2,val),(),...,()]
    """
    temp_result = io_get_rel_manticore_dict(group_id, keys, obj_rel_1, obj_rel_2, val, time_interval, is_unique)
    return [(int(item['key_id']),
             item['sec'],
             int(item['obj_id_1']),
             int(item['rec_id_1']),
             int(item['obj_id_2']),
             int(item['rec_id_2']),
             item['val']
             ) for item in temp_result]


###########################################
# ЧТЕНИЕ GEOMETRY_TREE
###########################################
# ret = [ {id: , name: , icon: }, ... ]
def io_get_geometry_tree(
        group_id,
        parent_id,
        write=True,
):
    return tuple(IO(group_id=group_id).get_geometry_tree(
        parent_id=parent_id,
        write=write,
    ))



