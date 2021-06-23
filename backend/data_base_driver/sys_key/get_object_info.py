import copy

from data_base_driver.constants.const_dat import DAT_SYS_OBJ


###########################################
# СПИСОК ОБЪЕКТОВ
###########################################
def obj_list():
    return [item for item in sorted(copy.deepcopy(DAT_SYS_OBJ.DUMP.get_all()), key=lambda x: x[DAT_SYS_OBJ.TITLE])
            if item.get('id') != 1]


# из rel-записей получить множество obj_id/rec_id: {(25, 34), (20, 1), (25, 33)}
# rel_recs - список rel-записей, можно генератор
def rel_rec_to_el(rel_recs):
    ret = set()
    for item in rel_recs:
        ret.add((item[2], item[3]))
        ret.add((item[4], item[5]))
    return ret


# из пар obj_id/rec_id для obj_id оставить только rec_id
def el_to_rec_id(obj, els):
    obj_id = DAT_SYS_OBJ.DUMP.to_id(val=obj)
    return [item[1] for item in els if item[0] == obj_id]
