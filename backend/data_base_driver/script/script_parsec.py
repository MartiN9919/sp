import os

from data_base_driver.constants.const_script import IMPORTS, ENABLED_FUNCTIONS, ENVIRONMENT_VARIABLES, \
    BASE_PATH_TO_USER_SCRIPTS, PATH_TO_REPORTS_DIR

DEBUG = False


def is_function(string):
    """
    Стандартная функция проверки является ли данное слова функцией
    @param str: строка содержащие проверяемое слово
    @return: True если функция, False если нет
    """
    if string.find('\'') != -1 and string.find('(') != -1 and string.find('(') < string.find('\''):
        return True
    elif string.find('\"') != -1 and string.find('(') != -1 and string.find('(') < string.find('\"'):
        return True
    elif string.find('(') != -1:
        return True


def get_function_name(string):
    """
    Стандартная функция получения названия функции (func() => func)
    @param string: строка содержащие вызов функции
    @return: чистое название функции
    """
    string = string[:string.find('(')+1]
    if string.find('.') != -1:
        return string[string.find('.') + 1:string.find('(')].replace('[', '')
    elif string.find('=') != -1:
        return string[string.find('=') + 1:string.find('(')].replace('[', '')
    else:
        return string[:string.find('(')].replace('[', '')


def default_checker(str):
    """
    проверка содержит ли данная строка запрещенные функции или переменные окружения
    @param str: строка из скрипта
    @return: False если строка не прошла проверку, True если проверка пройдена
    """
    if len(list(
            set(str.split()) & set(
                ENVIRONMENT_VARIABLES))) > 0: return False, 'использование переменной окружения', list(
        set(str.split()) & set(ENVIRONMENT_VARIABLES))
    if len(set([get_function_name(func) for func in filter(is_function, str.split(' '))]).difference(
            set(ENABLED_FUNCTIONS))) > 0:
        return False, ' использование неразрешенной функции ', set(
            [get_function_name(func) for func in filter(is_function, str.split(' '))]).difference(set(ENABLED_FUNCTIONS))
    return True, ''


def parse_text_to_python(name, text, params, type):
    """
    парсинг текста скрипта в файл модуля python
    @param name: имя или id скрипта
    @param text: текст скрипта
    @param params: передаваемые в скрипт параметры
    @param type: тип скрипта
    @return: не возвращает состояние
    """
    path = BASE_PATH_TO_USER_SCRIPTS + name + '.py'
    file = open(path, 'w')
    file.write(IMPORTS + '\n\n')
    if type == 'map':
        file.write('def ' + name + '(request, group_id):\n')
    elif type == 'report':
        file.write('def ' + name + '(request, group_id, file_id, user_id, title, lock):\n')
    file.write('\ttry:\n')
    if type == 'report':
        file.write('\t\tlock.acquire()\n\t\tlock.release()\n')
        file.write('\t\tpath = \'' + PATH_TO_REPORTS_DIR + '\' + title\n')
    for param in params.split('\n'):
        file.write(
            '\t\t' + param.split(';')[0] + ' = request.get(\'' + param.split(';')[0] + '\',{}).get(\'value\',[])\n')
    index = text.find('\n')
    while index != -1:
        str = text[:index + 1]
        if default_checker(str)[0] == False:
            file.close()
            os.remove(path)
            return False, str, default_checker(str)[1], default_checker(str)[2]
        else:
            file.write('\t\t' + str)
            text = text[index + 1:]
            index = text.find('\n')
    str = text
    if default_checker(str)[0] == False:
        file.close()
        os.remove(path)
        return False, str, default_checker(str)[1], default_checker(str)[2]
    else:
        file.write('\t\t' + str + '\n')
        if type == 'report':
            file.write('\t\tset_file_path(file_id, path)\n')
            file.write('\t\tset_file_status(file_id, \'done\')\n')
            file.write(
                '\t\t' + 'add_notification(user_id, \'information\', \'ваш отчет: \' + title + \' - сгенерирован\','
                         ' from_id=1, file_id=file_id)' + '\n')
        if type == 'map':
            file.write('\texcept Exception as e:\n\t\traise e')
        elif type == 'report':
            file.write('\texcept BaseException:\n');
            file.write('\t\tset_file_status(file_id, \'error\')\n')
            file.write('\t\tadd_notification(user_id, \'error\', \'ошибка генерации вашего отчета: \' + title,'
                       ' from_id=1, file_id=file_id)\n')

    file.close()
    return True, 'all ok', '', ''
