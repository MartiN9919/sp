# -*- coding: utf-8 -*-

import time
import json
import logging
import traceback

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from core.projectSettings.logging_settings import PROJECT_LOG_REQUESTS


def request_wrap(f):
    """
    Обертка для упрощения функции
    """
    def wrap(request, *args, **kwargs):
        try:
            return JsonResponse(f(request, *args, **kwargs), status=200)
        except Exception as e:
            if len(e.args) > 1:
                return JsonResponse({'status': ' '+str(e)}, status=e.args[0])
            else:
                return JsonResponse({'status': ' '+str(e)}, status=498)
    wrap.__doc__ =f.__doc__
    wrap.__name__=f.__name__
    return wrap


def request_get(f):
    """
    Доступ только get-запросам
    """
    def wrap(request, *args, **kwargs):
        if request.method!='GET':
            raise Exception('доступен только GET-запрос')
        return f(request, *args, **kwargs)

    wrap.__doc__ =f.__doc__
    wrap.__name__=f.__name__
    return wrap


def request_post(f):
    """
    Доступ только post-запросам
    """
    def wrap(request, *args, **kwargs):
        if request.method!='POST':
            raise Exception('доступен только POST-запрос')
        return f(request, *args, **kwargs)

    wrap.__doc__ =f.__doc__
    wrap.__name__=f.__name__
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

    wrap.__doc__ =f.__doc__
    wrap.__name__=f.__name__
    return wrap



#########################################################################
# ДЕКОРАТОР
# Разрешает доступ в случае нахождения пользователя в одной из групп
# @decor_required_group('group_one', 'group_two') @decor_required_group('group_one')
#########################################################################
def decor_group_verify(user, *group_names):
    if user.is_authenticated:
        if len(group_names) == 0 or user.groups.filter(name__in=group_names).exists() or user.is_superuser:
            return True
    return False


def decor_group_required(*group_names):
    def in_groups(user):
        return decor_group_verify(user, *group_names)

    return user_passes_test(in_groups)


#########################################################################
# ДЕКОРАТОР
# Разрешает доступ только суперпользователю
# @decor_required_superuser
#########################################################################
def decor_required_superuser(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return _inner


#########################################################################
# ДЕКОРАТОР
# Разрешает доступ только персоналу
# @decor_required_staff
#########################################################################
def decor_required_staff(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return _inner


#########################################################################
# ДЕКОРАТОР
# Разрешает доступ только ajax
# @decor_required_ajax
#########################################################################
def decor_required_ajax(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax() or request.method != 'POST':
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


#########################################################################
# ДЕКОРАТОР
# Логирует request.param для ajax
# @request_log
#########################################################################
logger = logging.getLogger(PROJECT_LOG_REQUESTS)


def request_log(function):
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


#########################################################################
# ДЕКОРАТОР
# Время выполнения функции
# @decor_timeit
#########################################################################
def decor_timeit(method):
    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kwargs, te - ts))
        return result

    return timed


#########################################################################
# ДЕКОРАТОР
# результат в JSON
# @decor_json
#########################################################################
def decor_json(function):
    def _inner(request, *args, **kwargs):
        response = function(request, *args, **kwargs)
        return HttpResponse(json.dumps(response), content_type='application/json')

    return _inner


def login_check(function):
    def is_auth(request):
        if request.user.is_authenticated:
            return function(request)
        else:
            return JsonResponse({}, status=401)
    return is_auth