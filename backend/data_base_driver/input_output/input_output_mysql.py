from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_OBJ
from data_base_driver.input_output.io_class import IO
from data_base_driver.input_output.valid_permission_manticore import check_object_permission


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


def get_total_objects(group_id, object_id):
    """
    Функция для получения объектов заданного типа
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @return: словарь содержащий информацию об общем количестве объектов заданного типа в базе и до 200 последних
    добавленных идентификаторов
    """
    object_data = DAT_SYS_OBJ.DUMP.get_rec(id=object_id)
    table = 'obj_' + object_data['name'] + '_row'
    sql_total = f"SELECT COUNT(*) FROM (SELECT rec_id from {table} GROUP BY rec_id ) dt;"
    total = db_sql(sql_total)[0][0]
    sql_objects = f"SELECT rec_id,  TO_DAYS(DATE_FORMAT(max(dat), '%Y-%m-%d'))*86400 + " \
                  f"TIME_TO_SEC(DATE_FORMAT(max(dat),'%H:%i:%s')) sec  from {table} " \
                  f"GROUP BY rec_id order by sec DESC LIMIT 200;"
    objects = db_sql(sql_objects)
    rec_ids = [(item[0], item[1]) for item in objects if check_object_permission(group_id, object_id, item[0])]
    return {'total': total, 'objects': rec_ids}