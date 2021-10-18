import copy

from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_KEY, DAT_SYS_ID


###########################################
# СПИСОК ОБЪЕКТОВ
###########################################
def obj_list():
    temp_list = [item for item in sorted(copy.deepcopy(DAT_SYS_OBJ.DUMP.get_all()), key=lambda x: x[DAT_SYS_OBJ.TITLE])
            if item.get('id') != 1]
    keys = DAT_SYS_KEY.DUMP.get_rec(obj_id=1, only_first=False)
    for temp in temp_list:
        temp_rels = []
        temp_keys_1 = list(set([key['rel_obj_2_id'] for key in keys if key['rel_obj_1_id'] == temp['id']]))
        temp_keys_2 = list(set([key['rel_obj_1_id'] for key in keys if key['rel_obj_2_id'] == temp['id']]))
        temp_rels.extend(temp_keys_1)
        temp_rels.extend(temp_keys_2)
        temp['rels'] = temp_rels
    return temp_list


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


def get_object_new_rec_id(object_type):
    sql = 'SELECT ' + DAT_SYS_ID.ID + ' FROM '\
                    + DAT_SYS_ID.TABLE + ' WHERE ' \
                    + DAT_SYS_ID.OBJ_ID + ' = ' + str(object_type) + ';'
    return db_sql(sql)[0][0] + 1
