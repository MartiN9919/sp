import json
import geojson
import requests

from data_base_driver.additional_functions import get_date_time_from_sec
from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_KEY, DAT_OBJ_ROW
from data_base_driver.constants.const_fulltextsearch import FullTextSearch
from data_base_driver.input_output.input_output import io_get_obj, io_get_rel
from data_base_driver.input_output.input_output_mysql import io_get_obj_mysql_tuple, io_get_rel_mysql_generator
from data_base_driver.input_output.io_class import IO
from data_base_driver.sys_key.get_key_dump import get_key_by_id
from data_base_driver.sys_key.get_object_info import rel_rec_to_el, el_to_rec_id


def feature_collection_by_geometry(group_id, object_type, rec_id, keys, time_interval):
    """
    Функция для получения feature collection в формате geojson для конкретных экземпляров геометрий
    @param group_id: идентификатор группы пользователя
    @param object_type: идентификатор типа объекта (25 - точка, 30 - геометрия)
    @param rec_id: список идентификаторов объектов
    @param keys: список идентификаторов ключей классификатора которые необходимо вынести в properties
    @param time_interval: интервал времени в который должны были быть созданы искомые записи
    @return: feature collection содержащая информацию о искомых геометриях
    """
    if object_type == 25:
        keys.append(25204)
    elif object_type == 30:
        keys.append(30304)
    if len(rec_id) == 0:
        return geojson.FeatureCollection(features=[])
    records = io_get_obj(group_id, object_type, keys, rec_id, 1000, '', time_interval)
    objects = {}
    for record in records:
        if not objects.get(record[DAT_OBJ_ROW.ID]):
            objects[record[DAT_OBJ_ROW.ID]] = {}
        if get_key_by_id(record[DAT_OBJ_ROW.KEY_ID])[DAT_SYS_KEY.TYPE_VAL] == 'geometry':
            if not objects[record[DAT_OBJ_ROW.ID]].get('geometry'):
                objects[record[DAT_OBJ_ROW.ID]]['geometry'] = []
            objects[record[DAT_OBJ_ROW.ID]]['geometry'].append({DAT_OBJ_ROW.KEY_ID: record[DAT_OBJ_ROW.KEY_ID],
                                                                DAT_OBJ_ROW.VAL: record[DAT_OBJ_ROW.VAL],
                                                                DAT_OBJ_ROW.SEC: record[DAT_OBJ_ROW.SEC]})
            objects[record[DAT_OBJ_ROW.ID]]['geometry'].sort(key=lambda x: x[DAT_OBJ_ROW.SEC], reverse=True)
        else:
            if not objects[record[DAT_OBJ_ROW.ID]].get('params'):
                objects[record[DAT_OBJ_ROW.ID]]['params'] = []
            objects[record[DAT_OBJ_ROW.ID]]['params'].append({DAT_OBJ_ROW.KEY_ID: record[DAT_OBJ_ROW.KEY_ID],
                                                              DAT_OBJ_ROW.VAL: record[DAT_OBJ_ROW.VAL],
                                                              DAT_OBJ_ROW.SEC: record[DAT_OBJ_ROW.SEC]})
    temp = []
    for object in objects:
        if objects[object].get('geometry'):
            geometry = json.loads(objects[object].get('geometry')[0]['val'])
            params = {}
            for param in objects[object].get('params', []):
                params[get_key_by_id(param[DAT_OBJ_ROW.KEY_ID])[DAT_SYS_KEY.NAME]] = \
                    [param[DAT_OBJ_ROW.VAL], get_date_time_from_sec(param[DAT_OBJ_ROW.SEC])]
            feature = geojson.Feature(geometry=geometry, properties=params)
            feature['id'] = object
            temp.append(feature)
    return geojson.FeatureCollection(temp)


def relations_to_geometry_id(group_id, geometry_type, object_type, rec_id, keys_relation, time_interval):
    """
    Функция для преобразования связей в идентификаторы геометрий
    @param group_id: идентификатор группы пользователя
    @param geometry_type: идентификатор типа геометрии (25 - точка, 30 - геометрия)
    @param object_type: идентификатор связи объекта связь с которым мы ищем
    @param rec_id: идентификатор объекта, если не известен то 0
    @param keys_relation: список идентификаторов типов связей между геометрией и объектом
    @param time_interval: временной интервал установления связи в секундах
    @return: список идентифкаторов наденных геометрических объектов
    """
    if rec_id == 0:
        object = [object_type]
    else:
        object = [object_type, rec_id]
    relations = io_get_rel(group_id, keys_relation, object, [geometry_type, ], [], time_interval, True)
    objects = [(int(item['obj_id_1']), int(item['rec_id_1'])) for item in relations] + \
              [(int(item['obj_id_2']), int(item['rec_id_2'])) for item in relations]
    geo_ids = el_to_rec_id(obj=geometry_type, els=objects)
    return geo_ids


def build_tree_rec(geometry, geometry_list):
    """
    Рекурсивная функция построения дерева геометрий
    @param geometry: геометрия на данном шаге
    @param geometry_list: список возможных наследников
    """
    child_items = [item for item in geometry_list if item['parent_id'] == geometry['id']]
    if len(child_items) > 0:
        if not geometry.get('children'):
            geometry['children'] = []
        geometry['children'] += child_items
    temp_geometry_list = [item for item in geometry_list if item not in child_items]
    for child in child_items:
        build_tree_rec(child, temp_geometry_list)


def build_tree_from_list(geometry_list):
    """
    Функция точка входа для построения дерева геометрий
    @param geometry_list: список геометрий
    @return: дерево геометрий
    """
    root = [item for item in geometry_list if item['parent_id'] == 0]
    temp_geometry_list = [item for item in geometry_list if item not in root]
    for item in root:
        build_tree_rec(item, temp_geometry_list)
    return root


def get_geometry_tree(group_id):
    """
    Функция для получения дерева геометрий
    @param group_id: идентификатор группы пользователя
    @return: дерево геометрий
    """
    data = json.dumps({
        'index': 'obj_geometry_col',
        'limit': 10000
    })
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    geometries = [{'id': item['_source']['rec_id'], 'name': item['_source']['name'], 'icon': item['_source']['icon'],
                   'parent_id': item['_source']['parent_id'], 'sec': item['_source']['sec']}
                  for item in json.loads(response.text)['hits']['hits']]
    geometries.sort(key=lambda x: x['id'])
    temp_result = []
    for geometry in geometries:
        temp_item = [item for item in temp_result if item['id'] == geometry['id']]
        if len(temp_item) == 0:
            temp_result.append(geometry)
        else:
            if (len(geometry['name']) > 0 and temp_item[0]['sec'] < geometry['sec']) or len(temp_item[0]['name']) == 0:
                temp_item[0]['name'] = geometry['name']
            if (len(geometry['icon']) > 0 and temp_item[0]['sec'] < geometry['sec']) or len(temp_item[0]['icon']) == 0:
                temp_item[0]['icon'] = geometry['icon']
            if (geometry['parent_id'] > 0 and temp_item[0]['sec'] < geometry['sec']) or temp_item[0]['parent_id'] == 0:
                temp_item[0]['parent_id'] = geometry['parent_id']
            if temp_item[0]['sec'] < geometry['sec']:
                temp_item[0]['sec'] = geometry['sec']
    return build_tree_from_list(temp_result)




###########################################
# POINT_FC, СВЯЗАННЫЕ ПО keys_rel
###########################################
# IN
#     obj_name        гео-объект                          'point' или 'geometry' или id
#     group_id        id группы пользователя
#     keys_rel        name or id: ('ngg_tmc', 1)
#     keys_obj        ('address',)
#
# OUT
#     FeatureCollection (id, properties = { 'address':, }, geometry)
def io_get_geometry_tree_layer2(group_id, parent_id, write=True, ):
    """
    Функция для получения одного уровня дерева геометрий по идентификатору родителя
    @param group_id: идентификатор группы пользователя
    @param parent_id: идентификатор родителя
    @param write: флаг записи
    @return: список кортежей с информацией о отдельных геометриях
    """
    return tuple(IO(group_id=group_id).get_geometry_tree(
        parent_id=parent_id,
        write=write,
    ))


def rel_to_geo_fc(obj, group_id, keys_rel, keys_obj, where_dop=[]):
    obj_id = DAT_SYS_OBJ.DUMP.to_id(val=obj)

    # записи rel
    rel_recs = io_get_rel_mysql_generator(
        group_id=group_id,
        keys=keys_rel,
        obj_rel_1=(obj_id,),  # (DAT_SYS_OBJ.NAME_POINT,),
        where_dop=where_dop,
    )

    # уникальные связанные объекты (obj_id, rec_id)
    # {(25, 34), (20, 1), (25, 33)}
    els = rel_rec_to_el(rel_recs=rel_recs)

    # оставить только geo_ids id: [34, 33, ...]
    geo_ids = el_to_rec_id(obj=obj_id, els=els)

    # результат в FC
    return geo_id_to_fc(obj=obj_id, group_id=group_id, geo_ids=geo_ids, keys=keys_obj)


###########################################
# IN
#     group_id        id группы пользователя
#     geo_ids         id гео-объектов             (33, 34)
#     keys:           ключи из SYS_KEY, location не указывать, т.к. задается автоматически
#
# OUT ITEM
#     id:         ...,
#     properties: { 'key_name_0':' (val, Null), 'key_name_N': (val, dat), ...}    все ключи в properties
#     geometry:   ...
###########################################
def geo_id_to_fc(obj, group_id, geo_ids, keys):
    REC_ID = 0
    REC_KEY = 1
    REC_VAL = 2
    REC_DAT = 3

    FC_ID = 'id'
    FC_PROPERTIES = 'properties'
    FC_GEOMETRY = 'geometry'

    obj_id = DAT_SYS_OBJ.DUMP.to_id(val=obj)
    obj_name = DAT_SYS_OBJ.DUMP.to_name(val=obj)
    if obj_name == DAT_SYS_OBJ.NAME_POINT:
        keys = (DAT_SYS_KEY.NAME_POINT_LOCATION,) + tuple(keys)
    elif obj_name == DAT_SYS_OBJ.NAME_GEOMETRY:
        keys = (DAT_SYS_KEY.NAME_GEOMETRY_LOCATION,) + tuple(keys)
    else:
        raise Exception('Unknow obj [' + obj + ']')

    # читать записи point по id
    # recs = ((42, 30303, 'Тест 41'), (42, 81, '-1', None), (42, 'location', '{"type": "GeometryCollection", "geometries": [{"type": "Polygon", "coordinates": []}]}'), ... )
    recs = io_get_obj_mysql_tuple(
        group_id=group_id,
        obj=obj_id,
        keys=keys,
        ids=geo_ids,
    ) if len(geo_ids) > 0 else []

    # группировка по id в словарь d {id1: {id: id1, ...}, ...}
    d = {}
    for rec in recs:
        id = rec[REC_ID]
        # d_item: прочитать
        d_item = d.get(id, {FC_ID: str(id), FC_PROPERTIES: {}, })

        # запомнить ключ в d_item
        if rec[1] == 'location':
            # исключение в FC_GEOMETRY
            d_item[FC_GEOMETRY] = json.loads(rec[REC_VAL])
            # остальное в FC_PROPERTIES
        else:
            key_name = DAT_SYS_KEY.DUMP.to_name(obj_id=obj_id, val=rec[REC_KEY])
            d_item[FC_PROPERTIES][key_name] = (rec[REC_VAL], (None if len(rec) <= 3 else rec[REC_DAT]))

        # d_item: запомнить
        d[id] = d_item

    # словарь d в FeatureCollection
    features = []
    for d_key in d:
        feature = geojson.Feature(**d[d_key])
        features.append(feature)
    return geojson.FeatureCollection(features)
