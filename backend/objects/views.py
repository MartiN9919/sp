import json

from django.http import JsonResponse
from core.projectSettings.decoraters import login_check, request_log, request_wrap, request_get, write_permission
from data_base_driver.constants.const_dat import DAT_OWNER
from data_base_driver.record.get_record import get_object_record_by_id_http
from data_base_driver.input_output.io_geo import get_geometry_tree, feature_collection_by_geometry
from data_base_driver.osm.osm_lib import osm_search, osm_fc
from data_base_driver.record.search import search
from data_base_driver.record.add_record import add_data, add_geometry
from data_base_driver.relations.add_rel import add_rel
from data_base_driver.relations.get_rel import get_object_relation
from data_base_driver.sys_key.get_key_dump import get_keys_by_object, get_relations_list
from data_base_driver.sys_key.get_object_info import obj_list


@login_check
@request_log
def aj_object_type_list(request):
    """
    Функция API для получения списка типов объектов с информацией о них
    @param request: запрос на получение списка
    @return: json содержащих информации по ключу data в формате:
    [{id, name, title, title_single, icon, descript},...{}]
    """
    return JsonResponse({'data': obj_list()}, status=200)


@login_check
@request_log
@request_wrap
@request_get
def aj_list_classifier(request):
    """
    Функция API для получения списка классификаторов для отдельного объекта
    @param request: запрос на получение списка, может быть только GET и должен содержать в url object_id
    @return: json содержащих информации по ключу data в формате:
    [{id,obj_id,col,need,type,list_id:{name,val:[]},name,title,hint,descript}, ...,{}]
    """
    return {'data': get_keys_by_object(request.GET['object_id'])}


@login_check
@request_log
@request_wrap
@request_get
def aj_list_rels(request):
    """
    Функция API для получения списка связей между двумя объектами
    @param request: запрос на получение списка, может быть только GET и должен содержать в url object_1_id и object_2_id
    @return: json содержащих информации по ключу data в формате:
    [{id,title,hint,list:{}},...,{}]
    """
    return {'data': get_relations_list(request.GET['object_1_id'], request.GET['object_2_id'])}


@login_check
@write_permission
@request_log
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
            return JsonResponse({'data': get_object_record_by_id_http(object_id=int(request.GET['object_id']),
                                                                      rec_id=int(request.GET['record_id']),
                                                                      group_id=group_id)}, status=200)
        except:
            return JsonResponse({'status': 'неверный номер объекта'}, status=496)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = add_data(user=request.user, group_id=group_id, object=data)
            if not result.get('object') or not result.get('objects'):
                return JsonResponse({'data': result}, status=200)
            else:
                return JsonResponse({'data': 'ошибка добавления'}, status=497)
        except Exception as e:
            if e.args[0] == 1:
                return JsonResponse({'data': ''}, status=452)
            elif e.args[0] == 2:
                return JsonResponse({'data': ''}, status=453)
            else:
                return JsonResponse({'data': 'ошибка добавления'}, status=498)
    else:
        return JsonResponse({'data': 'неизвестный тип запроса'}, status=480)


@login_check
@request_log
def aj_relation(request):
    """
    Функция API для работы со связями
    @param request: запрос на действие со связями
    @return: статус выполнения или результат в зависимости от типа запроса
    POST запрос на добавление связи между двумя объектами, должен содержать в url key_id, object_1_id, rec_1_id,
        object_2_id, rec_2_id, val, date_time
    GET запрос на получение связей для одного объекта со списком других объектов. должен содержать object_id, rec_id и
    objects в формате [{object_id, key_id},...,{}]
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            result = add_rel(group_id=group_id, object_1_id=data.get('object_1_id'), rec_1_id=data.get('rec_1_id'),
                             object_2_id=data.get('object_2_id'), rec_2_id=data.get('rec_2_id'),
                             params=data.get('params'))
            return JsonResponse({'data': result}, status=200)
        except:
            return JsonResponse({'data': 'ошибка добавления'}, status=497)
    if request.method == 'GET':
        try:
            result = get_object_relation(group_id, int(request.GET['object_id']), int(request.GET['rec_id']),
                                         json.loads(request.GET['objects']))
            return JsonResponse({'data': result}, status=200)
        except:
            return JsonResponse({'status': 'неверный номер объекта'}, status=496)
    else:
        return JsonResponse({'data': 'неизвестный тип запроса'}, status=480)


@login_check
@request_log
def aj_object_relation(request):
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = get_object_relation(group_id, int(data.get('object_id')), int(data.get('rec_id')),
                                         data.get('objects'))
            return JsonResponse({'data': result}, status=200)
        except:
            return JsonResponse({'status': 'неверный номер объекта'}, status=496)
    else:
        return JsonResponse({'data': 'неизвестный тип запроса'}, status=480)


@login_check
@request_log
def aj_search_objects(request):
    """
    Функция API для поиска объектов в базе данных
    @param request: POST запрос содержащий по ключу data древовидный json следующего формата:
    {obj_id, request, key_id, list_id, rels:[{obj_id, request, key_id, list_id, rels},...,{}]}
    @return: json с информацией о объекте в формате [{rec_id, obj_id, params:[{id,val},...,{}]},...,{}]
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({'data': search(data, group_id)}, status=200)
        except:
            return JsonResponse({'status': ' ошибка выполнения запроса'}, status=496)
    else:
        return JsonResponse({'data': 'неизвестный тип запроса'}, status=480)


@login_check
@request_log
@request_wrap
@request_get
def aj_geometry_tree(request):
    """
    Функция API для получения дерева геометрий
    @param request: запрос, поддерживаемый тип - GET, дополнительная нашрузка не требуется
    @return:  json дерево в формате: [{id,name,icon,child:[{},{},...,{}]},{},...,{}]
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    return {'data': get_geometry_tree(group_id=group_id)}


@login_check
@request_log
@request_wrap
@write_permission
def aj_geometry(request):
    """
    Функция API для получения геометрии по ее идентификатору
    @param request: GET запрос содержащий идентификатор геометрии по ключу rec_id
    @return: feature collection из базы данных соответствующий данному идентификатору
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'GET':
        try:
            geometry = feature_collection_by_geometry(group_id, 30, [request.GET['rec_id']], [30301, 30303], {})
            return {'data': geometry}
        except:
            return JsonResponse({'status': ' ошибка выполнения запроса'}, status=496)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = add_geometry(
                user = request.user,
                group_id = group_id,
                rec_id = data.get('rec_id', 0),
                location = data.get('location'),
                name = data.get('name'),
                parent_id = data.get('parent_id'),
                icon = data.get('icon'),
            )
            return {'data': result}
        except:
            return JsonResponse({'status': ' ошибка выполнения запроса'}, status=496)
    else:
        return JsonResponse({'data': 'неизвестный тип запроса'}, status=480)


@login_check
@request_log
@request_wrap
@request_get
def aj_groups(request):
    return {'data': DAT_OWNER.DUMP.get_groups_list()}



@login_check
@request_log
@request_wrap
@request_get
def aj_osm_search(request):
    """
    Поиск osm-записей
    @param request: text - поисковая строка
    @return: json [{id,name,icon,},...]
    """
    geometry = False
    if request.GET.get('geometry', 'False') == 'true':
        geometry = True
    return {'data': osm_search(text=request.GET.get('text', ''), geometry=geometry)}



@login_check
@request_log
@request_wrap
@request_get
def aj_osm_fc(request):
    """
    OSM: по id вернуть геометрию
    @param request: id - идентификатор геометрии
    @return: fc
    """
    return {'data': osm_fc(id=request.GET['id'])}


