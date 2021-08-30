from data_base_driver.constants.const_dat import DAT_SYS_TRIGGER
from data_base_driver.sys_key.get_list import get_list_by_name
from data_base_driver.connect.connect_mysql import db_sql


def parse_variables(variables):
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
    result = {}
    sql = 'SELECT ' + DAT_SYS_TRIGGER.ID + ', '\
                    + DAT_SYS_TRIGGER.OBJECT_ID + ', '\
                    + DAT_SYS_TRIGGER.TITLE + ', '\
                    + DAT_SYS_TRIGGER.VARIABLES + '  FROM ' + DAT_SYS_TRIGGER.TABLE + ';'
    temp_result = db_sql(sql)
    for temp in temp_result:
        if not result.get(temp[1]):
            result[temp[1]] = []
        result[temp[1]].append({'id': temp[0], 'name': temp[2], 'hint': '', 'variables': parse_variables(temp[3])})
    return result
