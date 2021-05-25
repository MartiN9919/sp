# -*- coding: utf-8 -*-

from   web.lib.decor                  import decor_json



###########################################
# ОШИБОЧНЫЙ ПУТЬ AJAX
###########################################
@decor_json
def aj_sys_error(request): 
	return request.method+' '+request.path+' not found'

