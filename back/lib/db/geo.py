# -*- coding: utf-8 -*-

import json
import geojson

from   lib.db.const.const_dat     import DAT_SYS_OBJ, DAT_SYS_KEY
from   lib.db.io.io               import io_get_obj, io_get_rel_generator
from   lib.db.obj                 import rel_rec_to_el, el_to_rec_id


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
###########################################
def rel_to_geo_fc(obj, group_id, keys_rel, keys_obj, where_dop=[]):
    obj_id = DAT_SYS_OBJ.DUMP.to_id(val=obj)

    # записи rel
    rel_recs = io_get_rel_generator(
        group_id  = group_id,
        keys      = keys_rel,
        obj_rel_1 = (obj_id,), #(DAT_SYS_OBJ.NAME_POINT,),
        where_dop = where_dop,
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
    REC_ID        = 0
    REC_KEY       = 1
    REC_VAL       = 2
    REC_DAT       = 3

    FC_ID         = 'id'
    FC_PROPERTIES = 'properties'
    FC_GEOMETRY   = 'geometry'

    obj_id        = DAT_SYS_OBJ.DUMP.to_id  (val=obj)
    obj_name      = DAT_SYS_OBJ.DUMP.to_name(val=obj)
    if    obj_name==DAT_SYS_OBJ.NAME_POINT:    keys = (DAT_SYS_KEY.NAME_POINT_LOCATION,   )+tuple(keys)
    elif  obj_name==DAT_SYS_OBJ.NAME_GEOMETRY: keys = (DAT_SYS_KEY.NAME_GEOMETRY_LOCATION,)+tuple(keys)
    else: raise Exception('Unknow obj ['+obj+']')

    # читать записи point по id
    # recs = ((42, 30303, 'Тест 41'), (42, 81, '-1', None), (42, 'location', '{"type": "GeometryCollection", "geometries": [{"type": "Polygon", "coordinates": []}]}'), ... )
    recs = io_get_obj(
        group_id = group_id,
        obj      = obj_id,
        keys     = keys,
        ids      = geo_ids,
    ) if len(geo_ids)>0 else []

    # группировка по id в словарь d {id1: {id: id1, ...}, ...}
    d = {}
    for rec in recs:
        id = rec[REC_ID]
        # d_item: прочитать
        d_item = d.get(id, { FC_ID: str(id), FC_PROPERTIES: {}, })

        # запомнить ключ в d_item
        if rec[1]=='location':
            # исключение в FC_GEOMETRY
            d_item[FC_GEOMETRY] = json.loads(rec[REC_VAL])
            # остальное в FC_PROPERTIES
        else:
            key_name = DAT_SYS_KEY.DUMP.to_name(obj_id=obj_id, val=rec[REC_KEY])
            d_item[FC_PROPERTIES][key_name] = ( rec[REC_VAL], (None if len(rec) <= 3 else rec[REC_DAT]) )

        # d_item: запомнить
        d[id] = d_item

    # словарь d в FeatureCollection
    features = []
    for d_key in d:
        feature = geojson.Feature(**d[d_key])
        features.append(feature)
    return geojson.FeatureCollection(features)


