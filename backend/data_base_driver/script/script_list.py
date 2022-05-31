from data_base_driver.additional_functions import parse_type
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_SCRIPT, DAT_OWNER
from data_base_driver.script.get_script_info import get_script_variables


def sort_by_type(item):
    """
    Функция для сортировки по типу скрипт/папка
    @param item: скрипт/папка
    @return: True если скрипт, False если файл
    """
    if item.get('icon', 0) != 0:
        return False
    else:
        return True


def get_script_sql(parent_id, script_type):
    """
    Функция для получения строки sql запроса по выводу всех предков данной папки
    @param parent_id: идентификатор папки
    @param script_type: тип скрипта (карта или отчеты)
    @return: строка sql запроса
    """
    return "SELECT " + \
           DAT_SYS_SCRIPT.ID + ", " + \
           DAT_SYS_SCRIPT.TITLE + ", " + \
           DAT_SYS_SCRIPT.VARIABLES + ", " + \
           DAT_SYS_SCRIPT.HINT + ", " + \
           DAT_SYS_SCRIPT.ICON + ", " + \
           DAT_SYS_SCRIPT.OWNER_LINE + "_id " + \
           "FROM " + DAT_SYS_SCRIPT.TABLE_SHORT + " " + \
           "WHERE " + \
           DAT_SYS_SCRIPT.PARENT_ID + '_id ' + \
           parent_id + " AND " + \
           DAT_SYS_SCRIPT.TYPE + ' = \'' +\
           script_type + '\';'


def script_list(group_id, parent_id, script_type):
    """
    Функция для получения списка скриптов из базы данных
    @param parent_id: родительский id для данного набора скриптов
    @param group_id: идентификатор группы пользователя
    @param script_type: тип скрипта (карта или отчеты)
    @return: список скриптов в формате
    {"id":id,"text":text,"variables":variables},
    где id это уникальный номер скрипта в базе данных,
    text - название скрипта, variables - его переменные и их типы
    """
    parent = f" = {parent_id}" if parent_id > 0 else ' is NULL'
    sql = get_script_sql(parent_id=parent, script_type=script_type)
    scripts = db_sql(sql)
    scripts = list(filter(lambda x: DAT_OWNER.DUMP.valid_line_group(group_id=group_id, line_id=x[-1]), scripts))
    response_with_scripts = []
    for row in scripts:
        variables = get_script_variables(int(row[0]))
        variables_result = []
        for variable in variables:
            variables_dict = {'name': variable[0],
                              'title': variable[1],
                              'hint': variable[2],
                              'type': parse_type(variable[3], variable[4], variable[5]),
                              'necessary': True if variable[6] == 1 else False}
            variables_result.append(variables_dict)
        if row[4] is not None:
            if len(db_sql(get_script_sql(parent_id=' = ' + str(row[0]), script_type=script_type))) == 0:
                continue
            response_with_scripts.append({
                "id": row[0],
                "name": row[1],
                "icon": row[4],
                "children": [],
            })
        else:
            response_with_scripts.append({
                "id": row[0],
                "name": row[1],
                "variables": variables_result,
                "hint": row[3],
            })
    response_with_scripts = sorted(sorted(response_with_scripts, key=lambda k: k['name'].lower()), key=sort_by_type)
    return response_with_scripts


def get_script_tree(group_id, script_type, parent_id=0):
    scripts = script_list(group_id, parent_id, script_type)
    for script in scripts:
        if script.get('children') is not None:
            script['children'] = get_script_tree(group_id, script_type, script['id'])
    return scripts
