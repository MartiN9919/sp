import json

from core.projectSettings.decorators import login_check, request_wrap, request_get, write_permission, \
    request_post
from data_base_driver.constants.const_dat import DAT_OWNER
from data_base_driver.constants.const_map_tiles import MAP_TILES
from objects.record.get_record import get_object_record_by_id_http
from data_base_driver.input_output.io_geo import get_geometry_search, feature_collection_by_geometry
from data_base_driver.osm.osm_lib import osm_search, osm_fc
from objects.record.add_record import add_data, add_geometry, add_data_from_form
from objects.record.get_record import get_keys
from data_base_driver.sys_key.get_list import get_lists
from data_base_driver.sys_key.get_object_info import objects_list
from objects.record.search import search
from objects.relations.add_rel import add_rel
from objects.relations.find_rel import search_relations
from objects.relations.get_rel import get_relations_list, get_objects_relation, get_object_relations


@login_check
@request_wrap
@request_get
def aj_object_type_list(request):
    """
    Функция API для получения списка типов объектов с информацией о них
    @param request: запрос на получение списка
    @return: json содержащих информации по ключу data в формате:
    [{id, name, title, title_single, icon, descript},...{}]
    """
    return objects_list()


@login_check
@request_wrap
@request_get
def aj_lists(request):
    """
    Функция для обработки запроса на получение всех списков
    @param request: GET запрос на получение всех списков
    @return: json в формате: {id:{name,title,hint,values}, ..., id_n:{}}
    """
    return get_lists()


@login_check
@request_wrap
@request_get
def aj_list_classifier(request):
    """
    Функция API для получения списка классификаторов для отдельного объекта
    @param request: запрос на получение списка, может быть только GET и должен содержать в url object_id
    @return: json содержащих информации по ключу data в формате:
    [{id,obj_id,col,need,type,list_id:{name,val:[]},name,title,hint,descript}, ...,{}]
    """
    return get_keys()


@login_check
@request_wrap
@request_get
def aj_list_relations(request):
    """
    Функция API для получения списка связей между двумя объектами
    @param request: запрос на получение списка, может быть только GET и должен содержать в url object_1_id и object_2_id
    @return: json содержащих информации по ключу data в формате:
    [{id,title,hint,list:{}},...,{}]
    """
    return get_relations_list()


@login_check
@write_permission
@request_wrap
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
    triggers = json.loads(request.headers.get('Set-Cookie', '[]'))
    if request.method == 'GET':
        try:
            return get_object_record_by_id_http(object_id=int(request.GET['object_id']),
                                                rec_id=int(request.GET['rec_id']),
                                                group_id=group_id,
                                                triggers=triggers)
        except Exception as e:
            raise e
    if request.method == 'POST':
        try:
            data = json.loads(request.POST['data'])
            result = add_data(user=request.user, group_id=group_id, object=data, files=request.FILES)
            if result.get('objects'):
                return result['objects']
            elif result.get('object'):
                return get_object_record_by_id_http(object_id=data.get('object_id'),
                                                    rec_id=result.get('object'),
                                                    group_id=group_id,
                                                    triggers=triggers)
            else:
                raise Exception(497, 'ошибка добавления')
        except Exception as e:
            if e.args[0] == 1:
                raise Exception(452, e.args[1])
            elif e.args[0] == 2:
                raise Exception(453, e.args[1])
            else:
                raise Exception(491, 'Проверьте корректность введенных данных')
    else:
        raise Exception(480, 'Некорректный формат запроса')


@login_check
@request_wrap
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
                             params=data.get('params'),
                             doc_rec_id=data.get('doc_rec_id'))
            return result
        except Exception as e:
            raise e
    else:
        raise Exception(480, 'Некорректный формат запроса')


@login_check
@request_wrap
@request_get
def aj_objects_relation(request):
    """
    Функция обработки запроса на получение связей между 2 объектами
    @param request: запрос содержащий идентификаторы 2-х объектов
    @return: список объектов через которые могут быть связаны 2 начальных объекта
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    return get_objects_relation(group_id, int(request.GET['object_id_1']), int(request.GET['rec_id_1']),
                                int(request.GET['object_id_2']), int(request.GET['rec_id_2']),
                                int(request.GET['search_deep'] if len(request.GET['search_deep']) else 5),
                                int(request.GET['search_count']) if len(request.GET['search_count']) else None,
                                True if request.GET['search_short'] == 'true' else False)


@login_check
@request_wrap
def aj_object_relation(request):
    """
    Функция обработки запроса получения связей объекта
    @param request: идентификаторы объекта и список объектов с которыми возможна связь
    @return: список связей
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = get_object_relations(group_id, int(data.get('object_id')), int(data.get('rec_id')),
                                         data.get('objects'))
            return result
        except Exception as e:
            raise e
    else:
        raise Exception(480, 'Некорректный формат запроса')


@login_check
@request_wrap
def aj_search_relations(request):
    """
    Функция обработки запроса рекурсивного поиска связей
    @param request: древовидный запрос для поиска связей
    @return: список объектов связи с которыми найдены
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return search_relations(group_id, data)
        except Exception as e:
            raise e
    else:
        raise Exception(480, 'Некорректный формат запроса')


@login_check
@request_wrap
def aj_search_objects(request):
    """
    Функция API для поиска объектов в базе данных
    @param request: POST запрос содержащий по ключу data древовидный json следующего формата:
    {obj_id, request, key_id, list_id, rels:[{obj_id, request, key_id, list_id, rels},...,{}]}
    @return: json с информацией о объекте в формате [{rec_id, obj_id, params:[{id,val},...,{}]},...,{}]
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    triggers = json.loads(request.headers.get('Set-Cookie', '{}'))
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return search(data, group_id, triggers)
        except Exception as e:
            raise e
    else:
        raise Exception(480, 'Некорректный формат запроса')


@login_check
@request_wrap
@request_get
def aj_geometry_search(request):
    """
    Функция API для получения дерева геометрий, отфильтрованного по text
    @param request: запрос, поддерживаемый тип - GET
    @param request: text - поисковая строка
    @return:  json дерево в формате: [{id,name,icon,child:[{},{},...,{}]},{},...,{}]
    """
    return get_geometry_search(text=request.GET.get('text', ''))


@login_check
@request_wrap
@write_permission
def aj_geometry_fc(request):
    """
    Функция API для получения геометрии по ее идентификатору
    @param request: GET запрос содержащий идентификатор геометрии по ключу rec_id
                    POST запрос для создания/изменения геометрии
    @return: feature collection из базы данных соответствующий данному идентификатору
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    if request.method == 'GET':
        try:
            geometry = feature_collection_by_geometry(group_id, 30, [request.GET['rec_id']], [30303], {})
            return geometry
        except Exception as e:
            raise e
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = add_geometry(
                user=request.user,
                group_id=group_id,
                rec_id=data.get('rec_id', 0),
                location=data.get('location'),
                name=data.get('name'),
                parent_id=data.get('parent_id'),
            )
            return result
        except Exception as e:
            raise e
    else:
        raise Exception(480, 'Некорректный формат запроса')


@login_check
@request_wrap
@request_get
def aj_groups(request):
    """
    Функция для получения списка групп пользователей
    @param request: GET запрос без параметров
    @return: список групп пользователей
    """
    return DAT_OWNER.DUMP.get_groups()


@login_check
@request_wrap
@request_get
def aj_map_tiles(request):
    return MAP_TILES.TILES


@login_check
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
    return osm_search(text=request.GET.get('text', ''), geometry=geometry)


@login_check
@request_wrap
@request_get
def aj_osm_fc(request):
    """
    OSM: по id вернуть геометрию
    @param request: id - идентификатор геометрии
    @return: fc
    """
    return osm_fc(id=request.GET['id'])


@login_check
@request_wrap
@request_post
def aj_load_from_form(request):
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    files = request.FILES
    meta = json.loads(request.POST['data'])
    return add_data_from_form(request.user, group_id, files.popitem()[1][0], meta)


