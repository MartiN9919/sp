from data_base_driver.constants.const_trigger import BASE_PATH_TO_USER_TRIGGERS, IMPORTS


def parse_trigger_text_to_python(name, text, variables):
    path = BASE_PATH_TO_USER_TRIGGERS + name + '.py'
    file = open(path, 'w')
    file.write(IMPORTS + '\n\n')
    file.write('def ' + name + '(group_id, object_id, rec_id, params):\n')
    for variable in variables.split('\n'):
        file.write(
            '\t' + variable.split(';')[0] + ' = params.get(\'' + variable.split(';')[0] + '\',{}).get(\'value\',[])\n')
    index = text.find('\n')
    while index != -1:
        str = text[:index + 1]
        file.write('\t' + str)
        text = text[index + 1:]
        index = text.find('\n')
    str = text
    file.write('\t' + str + '\n')
    file.close()