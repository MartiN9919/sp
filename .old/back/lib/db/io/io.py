# -*- coding: utf-8 -*-

from   lib.db.const.const_dat      import DAT_SYS_OBJ
from   lib.db.io.io_class          import IO


###########################################
# ЗАПИСЬ OBJ / REL
###########################################
def io_set(
    group_id,
    obj,
    data,
):
    return IO(group_id=group_id).set(
        obj      = obj,
        data     = data,
    )



###########################################
# ЧТЕНИЕ OBJ
###########################################
def io_get_obj_generator(
    group_id,
    obj,
    keys          = [],
    ids           = [],
    ids_max_block = None,
    where_dop_row = [],
):
    yield from IO(group_id=group_id).get_obj(
        obj           = obj,
        keys          = keys,
        ids           = ids,
        ids_max_block = ids_max_block,
        where_dop_row = where_dop_row,
    )

def io_get_obj(
    group_id,
    obj,
    keys          = [],
    ids           = [],
    ids_max_block = None,
    where_dop_row = [],
):
    return tuple(IO(group_id=group_id).get_obj(
        obj           = obj,
        keys          = keys,
        ids           = ids,
        ids_max_block = ids_max_block,
        where_dop_row = where_dop_row,
    ))



###########################################
# ЧТЕНИЕ REL
###########################################
# generator: (DAT_REL.KEY_ID, DAT_REL.DAT, DAT_REL.OBJ_ID_1, DAT_REL.REC_ID_1, DAT_REL.OBJ_ID_2, DAT_REL.REC_ID_2)
def io_get_rel_generator(
    group_id,
    keys      = [],
    obj_rel_1 = None,
    obj_rel_2 = None,
    where_dop = [],
):
    yield from IO(group_id=group_id).get_rel(
        keys      = keys,
        obj_rel_1 = obj_rel_1,
        obj_rel_2 = obj_rel_2,
        where_dop = where_dop,
    )

# tuple: (DAT_REL.KEY_ID, DAT_REL.DAT, DAT_REL.OBJ_ID_1, DAT_REL.REC_ID_1, DAT_REL.OBJ_ID_2, DAT_REL.REC_ID_2)
def io_get_rel(
    group_id,
    keys      = [],
    obj_rel_1 = None,
    obj_rel_2 = None,
    where_dop = [],
    is_unique = False,       # проверять записи на уникальность
):
    ret = tuple(IO(group_id=group_id).get_rel(
        keys      = keys,
        obj_rel_1 = obj_rel_1,
        obj_rel_2 = obj_rel_2,
        where_dop = where_dop,
    ))
    if is_unique: ret = tuple(set(ret))
    return ret



###########################################
# ЧТЕНИЕ GEOMETRY_TREE
###########################################
# ret = [ {id: , name: , icon: }, ... ]
def io_get_geometry_tree(
    group_id,
    parent_id,
    write = True,
):
    return tuple(IO(group_id=group_id).get_geometry_tree(
        parent_id = parent_id,
        write     = write,
    ))

