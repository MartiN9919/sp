from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_key import TYPES
from data_base_driver.constants.const_dat import DAT_SYS_KEY


def set_key(id, obj_id, col, need, type_val, title, list_id='NULL', name='NULL', hint='NULL', description='NULL',
            rel_obj_1='NULL', rel_obj_2='NULL'):
    """
    добавление нового ключа в базу данных
    @param id: id ключа в числовом или строковом формате
    @param obj_id: id характеризуемого объекта в числовом или строковом формате
    @param col: bit дополнительного параметра, при его наличие параметр заносится в col таблицу соответствующего объекта
    @param need: обязательность ключа для объекта
    @param type_val: тип ключа
    @param title: название ключа для отображения
    @param list_id: ?
    @param name: имя ключа для идентификации
    @param hint: описание
    @param description: развернутое описание
    @param rel_obj_1: если ключ-связь то id первого объекта связи
    @param rel_obj_2: если ключ-связь то id второго объекта связи
    @return: код ошибки в формате списка со строковым значением при ошибке и пустой список при успешном добавлении(учитываются только внутренние проверки)
    """
    if not (isinstance(id, int)) and not (id.isdigit()): return ['error id type']
    if not (isinstance(obj_id, int)) and not (obj_id.isdigit()):  return ['error obj_id_type']
    if (not (isinstance(col, int)) and not (col.isdigit())) or (int(col) != 0 and int(col) != 1): return [
        'error col type']
    if (not (isinstance(need, int)) and not (need.isdigit())) or (int(need) != 0 and int(need) != 1):  return [
        'error need type']
    if rel_obj_1 != 'NULL' and not (isinstance(rel_obj_1, int)) and not (rel_obj_1.isdigit()): return [
        'error rel_obj_1 type']
    if rel_obj_2 != 'NULL' and not (isinstance(rel_obj_2, int)) and not (rel_obj_2.isdigit()): return [
        'error rel_obj_2 type']
    if list_id != 'NULL' and not (isinstance(list_id, int)) and not (list_id.isdigit()): return ['error list_id type']
    try:
        TYPES.index(type_val)
    except ValueError:
        return ['error type val']
    if not (isinstance(title, str)): return ['error title']
    if not (isinstance(name, str)): return ['error name']
    if not (isinstance(hint, str)): return ['error hint']
    if not (isinstance(description, str)): return ['error description']
    if name != 'NULL': name = '\'' + name + '\''
    if hint != 'NULL': hint = '\'' + hint + '\''
    if description != 'NULL': description = '\'' + description + '\''

    sql_request = 'INSERT INTO ' + DAT_SYS_KEY.TABLE_SHORT + ' (' + \
                  DAT_SYS_KEY.ID + ', ' + \
                  DAT_SYS_KEY.OBJ_ID + ', ' + \
                  DAT_SYS_KEY.COL + ', ' + \
                  DAT_SYS_KEY.NEED + ', ' + \
                  DAT_SYS_KEY.TYPE_VAL + ', ' + \
                  DAT_SYS_KEY.LIST_ID + ', ' + \
                  DAT_SYS_KEY.NAME + ', ' + \
                  DAT_SYS_KEY.TITLE + ', ' + \
                  DAT_SYS_KEY.HINT + ', ' + \
                  DAT_SYS_KEY.DESCRIPT + ', ' + \
                  DAT_SYS_KEY.REL_OBJ_1_ID + ', ' + \
                  DAT_SYS_KEY.REL_OBJ_2_ID + ') values (' \
                  + str(id) + ', ' + str(obj_id) + ', b\'' + str(col) \
                  + '\', b\'' + str(need) + '\', \'' + str(type_val) + '\' ,' \
                                                                       '' + str(
        list_id) + ', ' + name + ', \'' + title + '\', ' \
                  + hint + ', ' + description + ', ' + str(rel_obj_1) + '' \
                                                                        ', ' + str(rel_obj_2) + ');'
    return db_sql(sql_request, read=False)
