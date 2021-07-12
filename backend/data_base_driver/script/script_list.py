from data_base_driver.connect import connect_mysql
from data_base_driver.constants.const_dat import DAT_SYS_SCRIPT, DAT_OWNER


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


def get_sql(parent_id, script_type):
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


def script_list(parent_id, group_id, script_type):
    """
    получения списка скриптов из базы данных
    @param parent_id: родительский id для данного набора скриптов
    @param group_id: идентификатор группы пользователя
    @param script_type: тип скрипта (карта или отчеты)
    @return: список скриптов в формате
    {"id":id,"text":text,"variables":variables},
    где id это уникальный номер скрипта в базе данных,
    text - название скрипта, variables - его переменные и их типы
    """
    parent = ' is NULL'
    if parent_id > 0:
        parent = ' = ' + str(parent_id)
    sql = get_sql(parent_id=parent, script_type=script_type)
    scripts = connect_mysql.db_sql(sql)

    scripts = list(filter(lambda x: DAT_OWNER.DUMP.valid_line_group(group_id=group_id, line_id=x[-1]), scripts))
    response_with_scripts = []
    for row in scripts:
        if row[4] is not None:
            if len(connect_mysql.db_sql(get_sql(parent_id=' = ' + str(row[0]), script_type=script_type))) == 0:
                continue
            response_with_scripts.append({
                "id": row[0],
                "name": row[1],
                "icon": row[4],
                "children": [],
            })
        else:
            variables = row[2].replace('\r', '').split('\n')
            variables_list = [
                {'name': variable.split(';')[0], 'title': variable.split(';')[1], 'hint': variable.split(';')[2],
                 'type': variable.split(';')[3]} for variable in variables]
            response_with_scripts.append({
                "id": row[0],
                "name": row[1],
                "variables": variables_list,
                "hint": row[3],
            })
    response_with_scripts = sorted(response_with_scripts, key=lambda k: k['name'].lower())
    response_with_scripts.sort(key=sort_by_type)
    return response_with_scripts


def get_script_tree_recursive(group_id, previous_list, script_type):
    """
    Функция для рекурсивного обхода дерева скриптов
    @param group_id: идентификационный номер группы доступа
    @param previous_list: дерево уже полученное к данной итерации
    @param script_type:
    """
    for item in previous_list:
        if item.get('icon', 0) != 0:
            child_list = script_list(item.get('id'), group_id=group_id, script_type=script_type)
            item['children'] = child_list
            if len(child_list) != 0:
                get_script_tree_recursive(group_id=group_id, previous_list=child_list, script_type=script_type)


def get_script_tree(group_id, script_type):
    """
    Функция для получения полного дерева скриптов
    @param group_id: идентификационный номер группы доступа
    @param script_type:
    @return: полное дерево скриптов
    """
    base_list = script_list(parent_id=0, group_id=group_id, script_type=script_type)
    get_script_tree_recursive(group_id=group_id, previous_list=base_list, script_type=script_type)
    return base_list
