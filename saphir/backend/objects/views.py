import json

from django.http import JsonResponse
from core.projectSettings.decoraters import login_check, decor_log_request
from data_base_driver.constants.const_dat import DAT_OWNER
from data_base_driver.record.add_record import add_record
from data_base_driver.record.get_record import get_record_by_id, get_records_by_object
from data_base_driver.sys_key.get_key_dump import get_keys_by_object
from data_base_driver.sys_key.get_object_info import obj_list


@login_check
@decor_log_request
def aj_object_type_list(request):
    return JsonResponse({'data': obj_list()}, status=200)


@login_check
@decor_log_request
def aj_object_list(request):
    if request.method == 'GET':
        group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
        return JsonResponse({'data': get_records_by_object(group_id=group_id, object_type=request.GET['object_id'])},
                            status=200)
    else:
        return JsonResponse({'status': 'неверный тип запроса'}, status=400)


@login_check
@decor_log_request
def aj_list_classifier(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'data': get_keys_by_object(request.GET['object_id'])}, status=200)
        except:
            return JsonResponse({'status': 'неверный номер объекта'}, status=404)
    else:
        return JsonResponse({'status': 'неверный тип запроса'}, status=400)


@login_check
@decor_log_request
def aj_object(request):
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'GET':
        try:
            JsonResponse({'data': get_record_by_id(group_id=group_id, object_type=request.GET['object_id'],
                                                   record_id=request.GET['record_id'])}, status=200)
        except:
            return JsonResponse({'status': 'неверный номер объекта'}, status=404)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = add_record(group_id=group_id, object_id=data.get('object', 0), object_info=data.get('info', []))
            if result != -1:
                return JsonResponse({'data': result}, status=200)
            else:
                return JsonResponse({'data': 'ошибка добавления'}, status=403)
        except:
            return JsonResponse({'data': 'ошибка добавления'}, status=403)
    else:
        return JsonResponse({'data': 'неизвестный тип запроса'}, status=404)
