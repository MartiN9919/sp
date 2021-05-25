import json

from django.contrib.auth.decorators import login_required
from web.lib.decor import decor_json, decor_required_ajax, decor_log_request
from lib.db.script.script_list import script_list
from .pythonScriptExec import callfunc


###########################################
# СКРИПТ: СПИСОК ДОСТУПНЫХ СКРИПТОВ
###########################################
@login_required(login_url='/auth/login/')
@decor_required_ajax
@decor_log_request
@decor_json
def aj_script_list(request):
    print(request.body)
    return script_list(json.loads(request.body).get('id'))

###########################################
# СКРИПТ: ВЫПОЛНИТЬ
###########################################
@login_required(login_url='/auth/login/')
@decor_required_ajax
@decor_log_request
@decor_json
def aj_script_exec(request):
    body = json.loads(request.body)
    name = 'script_' + body['script']
    return callfunc(name, body)
