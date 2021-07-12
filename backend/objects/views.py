import json

from django.http import JsonResponse
from core.projectSettings.decoraters import login_check, decor_log_request
from data_base_driver.constants.const_dat import DAT_OWNER
from data_base_driver.full_text_search.http_api.find_object import get_object_record_by_id_http
from data_base_driver.full_text_search.search import search
from data_base_driver.input_output.io import io_set
from data_base_driver.record.add_record import add_data
from data_base_driver.relations.add_rel import add_rel
from data_base_driver.sys_key.get_key_dump import get_keys_by_object, get_relations_list
from data_base_driver.sys_key.get_object_info import obj_list


@login_check
@decor_log_request
def aj_object_type_list(request):
    """
    Функция API для получения списка типов объектов с информацией о них
    @param request: запрос на получение списка
    @return: json содержащих информации по ключу data в формате:
    [{id, name, title, title_single, icon, descript},...{}]
    """
    return JsonResponse({'data': obj_list()}, status=200)


@login_check
@decor_log_request
def aj_list_classifier(request):
    """
    Функция API для получения списка классификаторов для отдельного объекта
    @param request: запрос на получение списка, может быть только GET и должен содержать в url object_id
    @return: json содержащих информации по ключу data в формате:
    [{id,obj_id,col,need,type,list_id:{name,val:[]},name,title,hint,descript},...,{}]
    """
    if request.method == 'GET':
        try:
            return JsonResponse({'data': get_keys_by_object(request.GET['object_id'])}, status=200)
        except:
            return JsonResponse({'status': 'неверный номер объекта'}, status=496)
    else:
        return JsonResponse({'status': 'неверный тип запроса'}, status=480)


@login_check
@decor_log_request
def aj_list_rels(request):
    """
    Функция API для получения списка связей между двумя объектами
    @param request: запрос на получение списка, может быть только GET и должен содержать в url object_1_id и object_2_id
    @return: json содержащих информации по ключу data в формате:
    [{id,title,hint,list:{}},...,{}]
    """
    if request.method == 'GET':
        try:
            return JsonResponse({'data': get_relations_list(request.GET['object_1_id'], request.GET['object_2_id'])},
                                status=200)
        except:
            return JsonResponse({'status': 'некорректные id объектов'}, status=496)
    else:
        return JsonResponse({'status': 'неверный тип запроса'}, status=480)


@login_check
@decor_log_request
def aj_object(request):
    """
    Функция API для работы с объектами
    @param request: http запрос от клиента
    @return: статус выполнения или результат при запросе на получение
    GET получение объекта по его идентификатору в формате {rec_id, obj_id, params:[{id,val},...,{}]}
    POST  добавление нового объекта или информации о старом, запрос имеет данные по ключу data в формате:\
    {rec_id, obj_id, params:[{id,val},...,{}]} если объект новый rec_id не задается
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'GET':
        try:
            return JsonResponse({'data': get_object_record_by_id_http(object_id=request.GET['object_id'],
                                                                      rec_id=request.GET['record_id'])}, status=200)
        except:
            return JsonResponse({'status': 'неверный номер объекта'}, status=496)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = add_data(group_id=group_id, object=data)
            if result.get('status', -1) != -1:
                return JsonResponse({'data': result}, status=200)
            else:
                return JsonResponse({'data': 'ошибка добавления'}, status=497)
        except Exception as e:
            if e.args[0] == 1:
                return JsonResponse({'data': ''}, status=452)
            else:
                return JsonResponse({'data': 'ошибка добавления'}, status=498)
    else:
        return JsonResponse({'data': 'неизвестный тип запроса'}, status=480)


@login_check
@decor_log_request
def aj_relation(request):
    """
    Функция API для работы со связями
    @param request: запрос на действие со связями
    @return: статус выполнения или результат в зависимости от типа запроса
    POST запрос на добавление связи между двумя объектами, должен содержать в url key_id, object_1_id, rec_1_id,
        object_2_id, rec_2_id
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            add_rel(group_id=group_id, key_id=data.get('key_id'), object_1_id=data.get('object_1_id'),
                    rec_1_id=data.get('rec_1_id'), object_2_id=data.get('object_2_id'), rec_2_id=data.get('rec_2_id'),
                    val=data.get('val'), date_time=data.get('date_time'))
            return JsonResponse({'data': 'связь добавлена'}, status=200)
        except:
            return JsonResponse({'data': 'ошибка добавления'}, status=497)
    else:
        return JsonResponse({'data': 'неизвестный тип запроса'}, status=480)


@login_check
@decor_log_request
def aj_search_objects(request):
    """
    Функция API для поиска объектов в базе данных
    @param request: POST запрос содержащий по ключу data древовидный json следующего формата:
    {obj_id, request, key_id, list_id, rels:[{obj_id, request, key_id, list_id, rels},...,{}]}
    @return: json с информацией о объекте в формате [{rec_id, obj_id, params:[{id,val},...,{}]},...,{}]
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({'data': search(data)}, status=200)
        except:
            return JsonResponse({'status': ' ошибочный запрос'}, status=496)
    else:
        return JsonResponse({'data': 'неизвестный тип запроса'}, status=480)


@login_check
@decor_log_request
def aj_set_geometry(request):
    """

    @param request:
    @return:
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    data = json.loads(request.body)
    try:
        for geometry_object in data['data']['features']:
            io_set(group_id=group_id, obj='geometry', data=[['id', geometry_object['id']],
                                                            ['location', geometry_object['geometry']]])
        return JsonResponse({'data': 'изменено'}, status=200)
    except:
        return JsonResponse({'data': 'ошибка добавления'}, status=480)
