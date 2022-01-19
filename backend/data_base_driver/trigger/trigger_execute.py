import importlib

from data_base_driver.trigger.get_trigger_info import get_trigger_by_id


def check_triggers(triggers, group_id, object_id, rec_id):
    result = []
    for trigger in triggers:
        trigger_info = get_trigger_by_id(int(trigger.get('id')))
        if trigger_info['object_id'] != int(object_id):
            continue
        name = 'trigger_' + str(trigger.get('id'))
        if execute_trigger(name, group_id, object_id, rec_id, trigger.get('variables')):
            result.append(int(trigger['id']))
    return result


def execute_trigger(name, group_id, object_id, rec_id, params):
    importlib.invalidate_caches()
    try:
        my_module = importlib.import_module('script.user_triggers.' + name)
        result = getattr(my_module, name)(group_id, object_id, rec_id, params)
        return result
    except:
        return False