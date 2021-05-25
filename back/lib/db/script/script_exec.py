from .script_params import IMPORTS, ENABLED_FUNCTIONS, ENVIRONMENT_VARIABLES

import os

DEBUG = False


def is_function(str):
    if str.endswith(')'): return True


def get_function_name(str):
    return str[:str.find('(')]


def default_checker(str):
    if len(list(set(str.split()) & set(ENVIRONMENT_VARIABLES))) > 0: return False
    if len(set([get_function_name(func) for func in filter(is_function, str.split(' '))]).difference(
        set(ENABLED_FUNCTIONS))) > 0: return False


def parse_text_to_python(name, text, params):
    path = '../lib/db/script/user_script/' + name + '.py'
    file = open(path, 'w')
    file.write(IMPORTS + '\n\n')
    file.write('def ' + name + '(request):\n')
    file.write('\ttry:\n')
    for param in params.split('; '):
        file.write('\t\t' + param.split(':')[0] + ' = request.get(\'' + param.split(':')[0] + '\',[])\n')
    index = text.find('\n')
    while index != -1:
        str = text[:index + 1]
        if default_checker(str) == False:
            file.close()
            os.remove(path)
            return
        else:
            file.write('\t\t' + str)
            text = text[index + 1:]
            index = text.find('\n')
    str = text
    if default_checker(str) == False:
        file.close()
        os.remove(path)
        return
    else:
        file.write('\t\t' + str + '\n')
        file.write('\texcept BaseException:\n\t\treturn \'error\'')
    file.close()
