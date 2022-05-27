import importlib

from data_base_driver.additional_functions import date_client_to_server, date_time_client_to_server


def parse_variables(variables):
    for variable in variables:
        if variables[variable]['type']['title'] == 'date':
            variables[variable]['value'] = date_client_to_server(variables[variable]['value'])
        if variables[variable]['type']['title'] == 'datetime':
            variables[variable]['value'] = date_time_client_to_server(variables[variable]['value'])
    return variables


def execute_script_map(name, group_id, params):
    importlib.invalidate_caches()
    try:
        my_module = importlib.import_module('script.user_scripts.' + name)
        result = getattr(my_module, name)(params, group_id)
        return result
    except Exception as e:
        raise e


