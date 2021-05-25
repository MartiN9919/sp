
# pip install rply
# parsegenerator.py - need to swith off warnings
# https://github.com/joshsharp/python-braid
# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html


##### `rel_to_geo_fc`
```txt
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

```

____


##### `geo_id_to_fc`
```txt
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
```

____


##### `print` *вывод в терминал*
```txt
param
    '..., ..., ...'
ret
    NULL
```

____


##### `mysql` *ЗАПРОС К MYSQL.VEC_DATA*
```txt
param
    sql
        текст SQL-запроса

    wait=False
        повторять пока SQL-запрос не выполнится, ждать завершения

    read=True
        SQL-запрос на чтение?
ret
    ((...), ...)
```

____


##### `var_exist` *существует ли переменная*
```txt
param
    'var_name'
ret
    'Boolean'
```

____








#####  РАЗНОЕ


```txt
list_rec = fun_mysql( \
    "\
        SELECT \
            id, \
            address, \
            ST_AsGeoJSON(PointFromText(CONCAT('POINT(',lon,' ',lat,')'),1)) AS location \
        FROM obj_point_col \
    ", \
    False, \
    True \
)
ret = fun_point_fc(list_rec)


#######################################

ret = fun_rec_col_get('geometry', '', ['id', 'category', 'name'])


print('!!!!!', k)

# IF
if id1>=(8-id2): \
    id3=3; \
    print(id1*id2);

# MATH
id3=3.2
print(id2+2*3-1)
id1=(8-id2)
d = False
m = not s and d
k = [87, 'kkk', True, False, True]
s = k[key][2]

# MYSQL
dat = fun_mysql("SELECT id, address FROM obj_point_col WHERE id="+"4"+"5")
dat = fun_mysql( \
    "\
        SELECT \
            id, \
            address, \
            ST_AsGeoJSON(PointFromText(CONCAT('POINT(',lon,' ',lat,')'),1)) AS location \
        FROM obj_point_col" \
)

# ID связанных записей
dat = fun_mysql("\
    SELECT \
        rel_dop.id \
    FROM \
        rel_top INNER JOIN rel_dop USING(id) \
    WHERE \
        rel_top.key_id=key_id AND \
        rel_dop.obj_id=obj_id \
")
ret = points_to_features(dat)


#######################################
list_rec = fun_mysql( \
    "\
        SELECT \
            id, \
            address, \
            ST_AsGeoJSON(PointFromText(CONCAT('POINT(',lon,' ',lat,')'),1)) AS location \
        FROM obj_point_col \
    ", \
    False, \
    True \
)
ret = fun_point_fc(list_rec)
#######################################
```
