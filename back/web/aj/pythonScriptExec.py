import importlib


def callfunc(method_name,request):
    importlib.invalidate_caches()
    my_module = importlib.import_module('lib.db.script.user_script.' + method_name)
    return getattr(my_module, method_name)(request)
