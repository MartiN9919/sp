from data_base_driver.additional_functions import date_client_to_server, date_time_client_to_server


def parse_variables(variables):
    for variable in variables:
        if variables[variable]['type']['title'] == 'date':
            variables[variable]['value'] = date_client_to_server(variables[variable]['value'])
        if variables[variable]['type']['title'] == 'datetime':
            variables[variable]['value'] = date_time_client_to_server(variables[variable]['value'])
    return variables


