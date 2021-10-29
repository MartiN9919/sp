# -*- coding: utf-8 -*-
import os
import time
import json
import logging
import traceback

from django.http import JsonResponse
from core.projectSettings.logging_settings import PROJECT_LOG_REQUESTS, PROJECT_LOG_SCRIPT_ERROR
from core.settings import MEDIA_ROOT
from data_base_driver.constants.const_dat import DAT_OWNER
from data_base_driver.input_output.valid_permission_manticore import check_object_permission
from data_base_driver.sys_notifications.set_notifications_info import add_notification


def request_wrap(f):
    """
    Функция обертка для обработки всех запросов
    @param f: оборачиваемая функция обработки запроса
    @return: если exception - Json с кодом ошибки и статусом, в противном случае резьтат исходной функции в Json
    """

    def wrap(request, *args, **kwargs):
        try:
            return JsonResponse(f(request, *args, **kwargs), status=200, safe=False)
        except Exception as e:
            if len(e.args) > 1:
                return JsonResponse({'status': ' ' + str(e)}, status=e.args[0])
            else:
                return JsonResponse({'status': str(e)}, status=498)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


logger_script_error = logging.getLogger(PROJECT_LOG_SCRIPT_ERROR)


def script_wrap(f):
    """
    Функция обертка для всех функций вызова скриптов
    @param f: оборачиваемая функция вызова скрипта
    @return: резуьтат выполнения функции, в случае любого exception - оповещения и дополнительный лог об ошибке
    """

    def wrap(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except Exception as e:
            data = json.loads(request.body).get('variables')
            data = [str(key) + ':' + str(data[key]['value']) for key in data.keys()]
            message = '\n'.join(data) + '\n' + ''.join(traceback.format_tb(e.__traceback__)) + str(e)
            logger_script_error.info('user_id: ' + str(
                request.user.id) + ', info: \n' + message + '\n----------------------------------------------------------------------------------------------------------')
            add_notification(request.user.id, 'warning', message, from_id=1, file_id=None)
            raise e

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def request_get(f):
    """
    Функция оберкта пропускающая только GET запрос
    @param f: оборачиваемая функция
    @return: в случае GET запроса результат выполнения функции
    """

    def wrap(request, *args, **kwargs):
        if request.method != 'GET':
            raise Exception('доступен только GET-запрос')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def request_post(f):
    """
    Функция оберкта пропускающая только POST запрос
    @param f: оборачиваемая функция
    @return: в случае POST запроса результат выполнения функции
    """

    def wrap(request, *args, **kwargs):
        if request.method != 'POST':
            raise Exception('доступен только POST-запрос')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def request_download(f):
    """
    Фунцкия обертка для проверки доступа загрузки файла
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
        file_path = MEDIA_ROOT + '/' + path
        if os.path.exists(file_path):
            return f(request, *args, **kwargs)
        else:
            raise Exception(404, 'Файл не найден')

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def write_permission(f):
    """
    Функция декоратор для проверки прав на запись в базу данных
    @param f: оборачиваемая функция
    @return: результат оборачиваемой функции или  json с кодом 454
    """

    def wrap(request, *args, **kwargs):
        if request.method == 'POST' and not request.user.is_write:
            return JsonResponse({'data': 'ошибка добавления'}, status=454)
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


logger = logging.getLogger(PROJECT_LOG_REQUESTS)


def request_log(function):
    """
    Функция обертка для логирования запросов
    @param function: оборачиваемая функция обработки запроса
    @return: результат выполнения функции с обработкой лога
    """

    def _inner(request, *args, **kwargs):
        try:
            logger.info(
                str(request.user) + '.' +
                str(request.user.id) + '|' +
                request.get_host() + '|' +
                request.method + ':' +
                request.path + '|' +
                str(request.body.decode("utf-8"))
            )
        except:
            logger.info(
                str(request.user) + '.' +
                str(request.user.id) + '|' +
                request.get_host() + '|' +
                request.method + ':' +
                request.path + '|' +
                request.POST['data']
            )
        return function(request, *args, **kwargs)

    return _inner


def decor_timeit(method):
    """
    Функция обертка для замера времени выполнения
    @param method: обертываемая функция
    @return: резьтат выполнения функции и print() с временем выполнения в секундах
    """

    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kwargs, te - ts))
        return result

    return timed


def login_check(function):
    """
    Функция обертка для проверки аунтификации пользователя
    @param function: обертываемая функция
    @return: если пользователь аунтифицирован - результат выполнения исходной функции, если нет - 401 код
    """

    def is_auth(request):
        if request.user.is_authenticated:
            return function(request)
        else:
            return JsonResponse({}, status=401)

    return is_auth
