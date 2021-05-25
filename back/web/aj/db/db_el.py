# -*- coding: utf-8 -*-

import json
import logging

from   django.contrib.auth.decorators import login_required
from   web.lib.decor                  import decor_json, decor_required_ajax, decor_log_request, decor_required_superuser

from   lib.const                      import RET_ERROR
from   lib.db.const.const_dat         import DAT_SYS_OBJ, DAT_SYS_KEY, DAT_OWNER, DAT_OWNER_GROUPS
from   lib.db.io.io                   import io_get_obj
from   lib.sys                        import tuple_to_dict_many



###########################################
# НАЙТИ ЭЛЕМЕНТ ПО ПОИСКОВОЙ ФРАЗЕ
###########################################
# PARAM:
#        obj_id - id объекта
#        search - поисковая строка
# RET:   {ключ top: val, ключ dop: [val1, val2, ...]},
###########################################
@login_required(login_url='/auth/login/')
@decor_required_ajax
@decor_log_request
@decor_json
def aj_el_find(request):
    param  = dict(json.loads(request.body))
    obj_id = int(param['obj_id'])
    search = str(param['search'])
    # keys   = list(map(lambda x: x['id'], DAT_SYS_KEY.DUMP.get_rec(obj_id=obj_id, only_first=False)))
    # return io_get_obj(obj=obj_id, dat=[['id', rec_id]], get=keys)
    data = [
        {'id':1,'title':search+'aaa'},
        {'id':2,'title':search+'aaa1'},
        {'id':3,'title':search+'aaa2'},
        {'id':4,'title':'aaa2'},
        {'id':5,'title':'aaa22'},
        {'id':6,'title':'aaa23'},
        {'id':7,'title':'aaa24'},
        {'id':8,'title':'aaa242'},
        {'id':9,'title':'aaa2e42'},
        {'id':10,'title':'aaa24d2'},
        {'id':11,'title':'aaa24d23'},
        {'id':12,'title':'aaa24d24'},
        {'id':13,'title':'aaa24d244'},
        {'id':14,'title':'aaa24d25'},
    ]
    return data
