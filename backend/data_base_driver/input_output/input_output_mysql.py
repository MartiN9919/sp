from data_base_driver.input_output.io_class import IO


def io_get_obj_mysql_generator(group_id, obj, keys=[], ids=[], ids_max_block=None, where_dop_row=[]):
    """
    Функция аналогична функции io_get_obj_mysql_tuple, за исключением типа возвращаемого значения, в данном случае возвращается
    генератор, а не кортеж
    """
    yield from IO(group_id=group_id).get_obj(
        obj=obj,
        keys=keys,
        ids=ids,
        ids_max_block=ids_max_block,
        where_dop_row=where_dop_row,
    )


def io_get_obj_mysql_tuple(group_id, obj, keys=[], ids=[], ids_max_block=None, where_dop_row=[]):
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


def io_get_rel_mysql_generator(group_id, keys=[], obj_rel_1=None, obj_rel_2=None, where_dop=[]):
    """
    Функция аналогична функции io_get_rel_mysql_tuple, за исключением типа возвращаемого значения, в данном случае возвращается
    генератор, а не кортеж
    """
    yield from IO(group_id=group_id).get_rel(
        keys=keys,
        obj_rel_1=obj_rel_1,
        obj_rel_2=obj_rel_2,
        where_dop=where_dop,
    )


def io_get_rel_mysql_tuple(group_id, keys=[], obj_rel_1=None, obj_rel_2=None, where_dop=[], is_unique=False):
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