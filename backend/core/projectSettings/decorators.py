# -*- coding: utf-8 -*-
import os
import time
import json
import logging
import traceback

from django.http import JsonResponse
from core.projectSettings.logging_settings import PROJECT_LOG_SCRIPT_ERROR
from core.projectSettings.constant import MEDIA_ROOT

from data_base_driver.constants.const_dat import DAT_OWNER
from data_base_driver.input_output.valid_permission_manticore import check_object_permission
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from files.additional_function import convert_file_path


def request_wrap(f):
    """
    Функция обертка для обработки всех запросов
    @param f: оборачиваемая функция обработки запроса
    @return: если exception - Json с кодом ошибки и статусом, в противном случае результат исходной функции в Json
    """
    def wrap(request, *args, **kwargs):
        try:
            return JsonResponse(f(request, *args, **kwargs), status=200, safe=False)
        except Exception as e:
            if len(e.args) > 1:
                return JsonResponse({'status': ' ' + str(e)}, status=e.args[0])
            else:
                return JsonResponse({'status': str(e)}, status=498)

    return wrap


logger_script_error = logging.getLogger(PROJECT_LOG_SCRIPT_ERROR)


def script_wrap(f):
    """
    Функция обертка для всех функций вызова скриптов
    @param f: оборачиваемая функция вызова скрипта
    @return: результат выполнения функции, в случае любого exception - оповещения и дополнительный лог об ошибке
    """
    def wrap(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except Exception as e:
            data = json.loads(request.body).get('variables')
            data = [str(key) + ':' + str(data[key]['value']) for key in data.keys()]
            message = '\n'.join(data) + '\n' + ''.join(traceback.format_tb(e.__traceback__)) + str(e)
            logger_script_error.info('user_id: ' + str(
                request.user.id) + ', info: \n' + message + '\n' + '-'*86)
            add_notification(request.user.id, 'warning', message, from_id=1, file_id=None)
            raise e

    return wrap


def request_get(f):
    """
    Функция обертка пропускающая только GET запрос
    @param f: оборачиваемая функция
    @return: в случае GET запроса результат выполнения функции
    """
    def wrap(request, *args, **kwargs):
        if request.method != 'GET':
            raise Exception('доступен только GET-запрос')
        return f(request, *args, **kwargs)

    return wrap


def request_post(f):
    """
    Функция обертка пропускающая только POST запрос
    @param f: оборачиваемая функция
    @return: в случае POST запроса результат выполнения функции
    """
    def wrap(request, *args, **kwargs):
        if request.method != 'POST':
            raise Exception('доступен только POST-запрос')
        return f(request, *args, **kwargs)

    return wrap


def request_download(f):
    """
    Функция обертка для проверки доступа загрузки файла
    @param f: оборачиваемая функция
    @return: результат выполнения функции в случае прохождения проверки доступа, если нет - 403 или 404(нет файла) ошибка
    """
    def wrap(request, *args, **kwargs):
        group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
        path = request.path.split('download')[1]
        path_start_directory = path.split('/')[1]
        if path_start_directory != 'files':
            raise Exception(403, 'Нет доступа к файлу')
        object_id = int(path.split('/')[2])
        rec_id = int(path.split('/')[3])
        if not check_object_permission(group_id, object_id, rec_id, False):
            raise Exception(403, 'Нет доступа к файлу')
        file_path = MEDIA_ROOT + '/' + convert_file_path(path)
        if os.path.exists(file_path):
            return f(request, *args, **kwargs)
        else:
            raise Exception(404, 'Файл не найден')

    return wrap


def write_permission(f):
    """
    Функция декоратор для проверки прав на запись в базу данных
    @param f: оборачиваемая функция
    @return: результат оборачиваемой функции или  json с кодом 454
    """
    def wrap(request, *args, **kwargs):
        if request.method == 'POST' and not request.user.is_write:
            return JsonResponse({'status': 'у вас нет прав на запись в базу данных'}, status=454)
        return f(request, *args, **kwargs)

    return wrap


def decor_timeit(method):
    """
    Функция обертка для замера времени выполнения
    @param method: обертываемая функция
    @return: результат выполнения функции и print() с временем выполнения в секундах
    """
    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        print('%2.2f sec %r (%r, %r)' % (te - ts, method.__name__, args, kwargs))
        return result

    return timed


def login_check(function):
    """
    Функция обертка для проверки аутентификации пользователя
    @param function: обертываемая функция
    @return: если пользователь аутентифицирован - результат выполнения исходной функции, если нет - 401 код
    """
    def is_auth(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return JsonResponse({}, status=401)

    return is_auth
