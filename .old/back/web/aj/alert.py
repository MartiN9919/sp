# -*- coding: utf-8 -*-

import json

from   django.contrib.auth.decorators import login_required
from   web.lib.decor                  import decor_json, decor_required_ajax, decor_log_request, decor_required_superuser

from   lib.sys                        import tuple_to_dict
from   lib.db.const.const_connect     import CONNECT
from   lib.db.const.const_dat         import DAT_SYS_ALERT
from   lib.db.connect.connect_mysql   import DB_read_lines, db_sql


########################################################
# ОПОВЕЩЕНИЕ ПРИНЯТЬ
########################################################
# return [{...}, {...}]
# 'id', 'content', 'type', 'wait'
########################################################
@login_required(login_url='/auth/login/')
@decor_required_ajax
@decor_log_request
@decor_json
def aj_alert_get(request):
    ret = []
    for item in DB_read_lines(
        sql=
            'SELECT '+
                DAT_SYS_ALERT.TABLE+'.'+DAT_SYS_ALERT.ID      +', '+
                DAT_SYS_ALERT.TABLE+'.'+DAT_SYS_ALERT.CONTENT +', '+
                DAT_SYS_ALERT.TABLE+'.'+DAT_SYS_ALERT.TYPE    +', '+
                DAT_SYS_ALERT.TABLE+'.'+DAT_SYS_ALERT.WAIT    +', '+
                DAT_SYS_ALERT.TABLE+'.'+DAT_SYS_ALERT.USERS   +', '+
                DAT_SYS_ALERT.TABLE+'.'+DAT_SYS_ALERT.GROUPS  +' '+
            'FROM ' +DAT_SYS_ALERT.TABLE+' '+
            'WHERE '+DAT_SYS_ALERT.TABLE+'.'+DAT_SYS_ALERT.ENABLED +'=1',
        database=CONNECT.DATA):
        users  = item[4].split()
        groups = item[5].split()
        if (not request.user.is_superuser) and len(groups)>0 and (not request.user.groups.filter(name__in=groups).exists()): continue
        ret.append(tuple_to_dict(item, [
            DAT_SYS_ALERT.ID, 
            DAT_SYS_ALERT.CONTENT, 
            DAT_SYS_ALERT.TYPE, 
            DAT_SYS_ALERT.WAIT,
        ]))
    return ret



########################################################
# ОПОВЕЩЕНИЕ УСТАНОВИТЬ
########################################################
@login_required(login_url='/auth/login/')
@decor_required_superuser
@decor_required_ajax
@decor_log_request
@decor_json
def aj_alert_set(request):
    data = json.loads(request.body)
    param_content  = str(data.get('content',  '')).strip()
    param_type     = str(data.get('type',     'info')).strip()
    param_wait     = int(data.get('wait',     0))
    param_users    = str(data.get('users',    '')).strip()
    param_groups   = str(data.get('groups',   '')).strip()
    param_descript = str(data.get('descript', '')).strip()
    if param_content=='' or (not param_type in ('info', 'warn', 'error')): return None

    ret = db_sql(
        sql=
            "INSERT IGNORE INTO "  +
                DAT_SYS_ALERT.TABLE   +" ("+
                DAT_SYS_ALERT.CONTENT +", "+
                DAT_SYS_ALERT.TYPE    +", "+
                DAT_SYS_ALERT.WAIT    +", "+
                DAT_SYS_ALERT.OWNER   +", "+
                DAT_SYS_ALERT.USERS   +", "+
                DAT_SYS_ALERT.GROUPS  +", "+
                DAT_SYS_ALERT.DESCRIPT+", "+
                DAT_SYS_ALERT.ENABLED +") "+
            "VALUES ("+
                "'"+param_content .replace("'", '"')+"', "+
                "'"+param_type    .replace("'", '"')+"', "+
                str(param_wait)                     +", "+
                "'"+str(request.user.id)+"', "+
                "'"+param_users   .replace("'", '"')+"', "+
                "'"+param_groups  .replace("'", '"')+"', "+
                "'"+param_descript.replace("'", '"')+"', "+
                "1)"
                ,
        read=False
    )
    return ret
