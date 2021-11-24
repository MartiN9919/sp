from data_base_driver.constants.const_dat import DAT_SYS_TRIGGER
from data_base_driver.sys_key.get_list import get_list_by_name
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.trigger.get_trigger_info import get_trigger_variables


def parse_variables(variables):
    """
    Функция для парсинга списка переменных из текста в список словарей
    @param variables: текст содержащий список переменных в формате "name;title;hint;type;list\n..."
    @return: список словарей в формате  [{name,title,hint,type,list},...,{}]
    """
    if not variables or len(variables) == 0:
        return []
    variables = variables.replace('\r', '').split('\n')
    variables_list = []
    for variable in variables:
        variable_params = variable.split(';')
        variable_dict = {'name': variable_params[0], 'title': variable_params[1], 'hint': variable_params[2],
                         'type': variable_params[3]}
        if len(variable_params) > 4:
            variable_dict['list'] = get_list_by_name(variable_params[4])
        else:
            variable_dict['list'] = None
        variables_list.append(variable_dict)
    return variables_list


def get_triggers_list():
    """
    Функция для формирования списка триггеров
    @return: список триггеров в формате [{id,name,hint,variables:[{name,title,hint,type,list},...,{}]},...,{}]
    """
    result = {}
    sql = 'SELECT ' + DAT_SYS_TRIGGER.ID + ', '\
                    + DAT_SYS_TRIGGER.OBJECT_ID + ', '\
                    + DAT_SYS_TRIGGER.TITLE + ', '\
                    + DAT_SYS_TRIGGER.HINT + ', '\
                    + DAT_SYS_TRIGGER.VARIABLES + '  FROM ' + DAT_SYS_TRIGGER.TABLE + ';'
    temp_result = db_sql(sql)
    for temp in temp_result:
        variables = get_trigger_variables(int(temp[0]))
        variables_result = []
        for variable in variables:
            variables_dict = {'name': variable[0],
                              'title': variable[1],
                              'hint': variable[2],
                              'type': {'title': variable[3]},
                              'necessary': True if variable[6] == 1 else False}
            if variable[3] == 'list':
                variables_dict['type']['value'] = int(variable[4])
            elif variable[3] == 'search':
                variables_dict['type']['value'] = int(variable[5]) if variable[5] else None
            else:
                variables_dict['type']['value'] = None
            variables_result.append(variables_dict)
        if not result.get(temp[1]):
            result[temp[1]] = []
        result[temp[1]].append({'id': temp[0], 'name': temp[2], 'hint': temp[3], 'variables': variables_result})
    return result
