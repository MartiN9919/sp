# -*- coding: utf-8 -*-

from   lib.db.const.const_dat       import DAT_SYS_OBJ, DAT_SYS_KEY



###########################################
# СПИСОК ОБЪЕКТОВ
###########################################
def obj_list():
    return [ {
        DAT_SYS_OBJ.ID:           x[DAT_SYS_OBJ.ID],
        DAT_SYS_OBJ.NAME:         x[DAT_SYS_OBJ.NAME],
        DAT_SYS_OBJ.TITLE:        x[DAT_SYS_OBJ.TITLE],
        DAT_SYS_OBJ.TITLE_SINGLE: x[DAT_SYS_OBJ.TITLE_SINGLE],
        DAT_SYS_OBJ.ICON:         x[DAT_SYS_OBJ.ICON],
    } for x in DAT_SYS_OBJ.DUMP.get_all() ]



###########################################
# ИНФОРМАЦИЯ ОБ ОБЪЕКТЕ OBJ И ЕГО КЛЮЧАХ
###########################################
# IN
#     obj  объект (int или str)
# OUT
#     obj  {}    инфо об объекте SYS_OBJ
#     keys []    инфо о  ключах  SYS_KEY
def key_list(obj):
    obj_id = DAT_SYS_OBJ.DUMP.to_id(val=obj)
    return {
        'obj':  DAT_SYS_OBJ.DUMP.get_rec(id=obj_id),
        'keys': DAT_SYS_KEY.DUMP.get_rec(obj_id=obj_id, only_first=False),
    }



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


