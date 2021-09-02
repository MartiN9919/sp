import importlib


def execute_script_map(name, group_id, params):
    importlib.invalidate_caches()
    try:
        my_module = importlib.import_module('script.user_scripts.' + name)
        result = getattr(my_module, name)(params, group_id)
        return result
    except:
        return 'error'