# -*- coding: utf-8 -*-

import logging

from django.shortcuts import render, redirect
from django.contrib   import auth
from django.conf      import settings
from django.template.context_processors import csrf

logger = logging.getLogger(settings.PROJECT_LOG_USERS)


#########################################################################
# ПРЕДУПРЕЖДЕНИЕ
# ИМЕЮЩИЙ ДОСТУП К АДМИНКЕ МОЖЕТ ВОЙТИ В СИСТЕМУ БЕЗ ЗАПИСЕЙ В ЛОГАХ
#########################################################################
def login(request):
    # если пользователь уже залогинен
    if request.user.is_authenticated: redirect('/')

    # логинимся
    args = {'pag_title': settings.PROJECT_TITLE_NAME}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            logger.info('login OK '+request.scheme+':'+request.get_host()+' '+username+'.'+str(request.user.id)+' '+request.META['HTTP_USER_AGENT'])
            return redirect('/')
        else:
            args['login_error'] = 'Неверный логин или пароль'
            logger.info('login ER '+request.get_host()+' '+username)
            return render(request=None, template_name='auth.html', context=args)
    else:
        usr = auth.get_user(request)
        if usr.is_authenticated: sInfo = usr.first_name+' '+usr.last_name
        else: sInfo = ''
        args['username'] = sInfo
        return render(request=None, template_name='auth.html', context=args)

def logout(request):
    logger.info('logout '+request.get_host()+' '+str(request.user)+'.'+str(request.user.id))
    auth.logout(request)
    return redirect('/auth/')

def all(request):
    return redirect('/auth/login/')
