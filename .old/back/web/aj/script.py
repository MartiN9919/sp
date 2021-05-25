# -*- coding: utf-8 -*-

import json

from   django.contrib.auth.decorators import login_required
from   web.lib.decor                  import decor_json, decor_required_ajax, decor_log_request  # , decor_required_superuser

from   lib.db.const.const_dat         import DAT_SYS_SCRIPT, DAT_OWNER
from   lib.db.script.script_list      import script_list
from   lib.db.script.script_exec      import script_exec



###########################################
# СКРИПТ: СПИСОК ДОСТУПНЫХ СКРИПТОВ
###########################################
@login_required(login_url='/auth/login/')
@decor_required_ajax
@decor_log_request
@decor_json
def aj_script_list(request):
    data = json.loads(request.body)
    return script_list(
    	group_id  = DAT_OWNER.DUMP.get_group(user_id=request.user.id),
    	parent_id = data.get('parent_id', -1)
    )



###########################################
# СКРИПТ: ВЫПОЛНИТЬ
###########################################
@login_required(login_url='/auth/login/')
@decor_required_ajax
@decor_log_request
@decor_json
def aj_script_exec(request):
    var_start = json.loads(request.body)
    var_start[DAT_SYS_SCRIPT.VAR_USER_ID]  = request.user.id
    var_start[DAT_SYS_SCRIPT.VAR_GROUP_ID] = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    return script_exec(
    	group_id  = DAT_OWNER.DUMP.get_group(user_id=request.user.id),
    	var_start = var_start
    )
