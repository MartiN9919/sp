from django.http import HttpResponse
import json, time

from fun.funSys import logger

#####################################################
# РЕЗУЛЬТАТ В JSON
#####################################################
class json2:
    def __init__(self, function):
        self._f = function

    def __call__(self, *args, **kwargs):
        response = self._f(*args, **kwargs)
        return HttpResponse(json.dumps(response), content_type='application/json')



#####################################################
# ВРЕМЯ ВЫПОЛНЕНИЯ ФУНКЦИИ
#####################################################
class decorTimer:
    def __init__(self, function):
        self._f = function

    def __call__(self, *args, **kwargs):
        t = time.time()
        res = self._f(*args, **kwargs)
        logger.info('Время выполнения ['+self._f.__name__+']: '+str(round(time.time() - t, 3))+' сек.')
        return res
