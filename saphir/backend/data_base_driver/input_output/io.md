# ОПЕРАЦИИ ВВОДА/ВЫВОДА (input/output)

## МОДУЛИ
* io.py - содержит функции для взаимодействия с БД, извне обращаться только к ним
* io_org_sql.py - логический уровень работы с MySQL (последовательность действий)
* io_org_sql.py - базовый уровень работы с MySQL (соединение, создание и выполнение SQL запросов)
* io_pars.py - инструмент работы с парами ключ/значение

## АРГУМЕНТ OBJ / ОБЪЕКТЫ
* указывает наименование объекта
* список допустимых объектов содержится в классификаторе объектов DAT_SYS_OBJ (таблица 'sys_obj')
* формат obj: str (из DAT_SYS_OBJ.NAME) или int (из DAT_SYS_OBJ.ID)
* каждый объект описывается в двух таблицах: col и row
* таблицы состоят из пар: ключей (col/row-ключи) и значений, соответствующих этим ключам
* col-таблица:
    * содержит ключи:
        * исключительные по важности
        * которые не могут быть определены в row-таблице из-за ограничений формата (str 255)
    * все col-пары принадлежат ОДНОЙ записи в БД (одна запись - несколько ключей)
    * поле id должно быть УНИКАЛЬНЫМ
* row-таблица:
    * содержит все остальные ключи
    * все row-пары принадлежат РАЗНЫМ записям в БД (одна запись - один ключ)
    * может ТОЛЬКО дополнятся записями, корректировка не допускается (принцип досье)
    * уникальность записей обеспечивается средствами базы данных
* col/row-записи связаны общим значением поля id
* при создании нового объекта его порядковый id предоставляется функцией io_sql.obj_rec_id_new
* free_row - специальная таблица, free_col не существует

## АРГУМЕНТ REL / СВЯЗИ-СОБЫТИЯ
* по принципу хранения данных это row-таблица

## АРГУМЕНТ DATA / КЛЮЧИ
* необходим для операций с БД (чтение, запись, обновление, поиск и т.д.)
* формат data: [ [key, val], ... ], т.е. список пар ключ/значение
* список ключей содержится в классификаторе ключей DAT_SYS_KEY (таблица 'sys_key')
* отнесение ключа к col/row производится автоматически и определяется полем DAT_SYS_KEY.COL классификатора ключей
* требования к ключу:
    * лучше всего указывать поле id (int) классификатора ключей, но не обязательно
    * для data-col допустимо указывать:
        * поле name (str) классификатора ключей. В результатах будет кеу=id (int)
    * для data-row допустимо указывать:
        * поле name (str) классификатора ключей. В результатах будет кеу=id (int)
        * если поле классификатора name не задано (null), то можно id (str). В результатах будет кеу=id (int)
        * несколько элементов с одинаковым key: [ [key: val_1], [key: val_2], ... ]
* ключ key='id':
    * не относится ни к data-col, ни к data-row
    * может указываться ТОЛЬКО для существующих записей
    * если требуется операция с КОНКРЕТНОЙ записью (чтение, обновление):
        * указание id желательно, но не обязательно
        * если id не задан, то он определяется автоматически (дополнительное обращение к БД)
        * поиск ведется по известным кеу-col, а key-row не учитывается
* особенности для rel-таблиц:
    * только col-пары
    * специальные поля: IO_PARS_DATA.FIELD_OBJ_1, IO_PARS_DATA.FIELD_OBJ_2: ['obj_1', 5, 100] или ['obj_1', 5]
    * обязательных полей нет
    * перед вставкой записи по умолчанию проверяется БД на наличие подобной

### пример
```python
obj = 'file',
data = [
   #['key_id',   10],
    ['type',     4],                        # col
    ['path',     'tests/new2'],              # col
    ['owner_id', 255],                      # col
    ['tests',     '77777'],                  # row
    [40405,      'val_1', '2019-01-01'],    # row
    ['40405',    'val_2']]                  # row

obj = 1,                                    # == 'rel'
data = [
    ['key_id',   10],
    ['key_id',   'ngg_smoke'],
    ['dat',      '2020-09-07'],
    # ВАРИАНТ 1
    ['obj_id_1', 'geometry'],               # == ['obj_id_1', 5],
    ['rec_id_1', 100],
    # ВАРИАНТ 2
    ['obj_2',    'file', 200],              # == ['obj_2', 4, 200],
    # ВАРИАНТ 3
    ['geometry', 100],                      # == [3, 100]
    ['file',     200]]                      # == [4, 200]
```

## IO_PARS_DATA
* наследование объекта dict. Содержит дополнительные функции и методы
* основа для операций с БД
* формируется из obj и data
* содержит полный перечень свойств объекта и ключей, а также пар key/val (для включения в SQL), а также дополнительные функции и методы:
    * rec_id
    * col_exist(), row_exist()
    * col_equ(), row_equ()
    * col_equ_flat(), row_equ_flat()
    * row_key_flat()
    * val(type, val)
* осуществляется проверка на уникальность ключей и наличие обязательных ключей (только rel)
* для rel:
    * obj_id с меньшим индексом всегда obj_id_1
    * если obj_id равны: rec_id с меньшим индексом всегда rec_id_1



### пример
```python
from lib.db.io.io_dat_pars import IO_PARS_DATA
data_pars = IO_PARS_DATA(obj=obj, data=data)

###########################################
# OBJ
###########################################
{
    OBJ_ID:     /int,                           # self.obj_id
    OBJ_NAME:   /str,                           # self.obj_name
    REC_ID:     /int,                           # self.rec_id
    COL_KEY:    [ record, ... ],                # DAT_SYS_KEY.DUMP; ссылка на запись классификатора
    COL_DIC:    [ {                             # только один dict, только одна пара, так как пара = запись в БД
                    key_name1: val /str,
                }, ... ],
    COL_TABLE:    /str,                         # self.col_table

    ROW_KEY:    [ record, ... ],                # DAT_SYS_KEY.DUMP; ссылка на запись классификатора
    ROW_DIC:    [ {                             # много один dict, кроме ID
                    DAT_OBJ_ROW.KEY_ID: /str,
                    DAT_OBJ_ROW.VAL:    val  /str,
                    DAT_OBJ_ROW.DAT:    date /str,
                }, ... ],
    ROW_TABLE:    /str,                         # self.row_table
}

###########################################
# REL
###########################################
{
    OBJ_ID:     /int,                           # self.obj_id
    OBJ_NAME:   /str,                           # self.obj_name
    REC_ID:     None,
    COL_KEY:    [],                             # self.col_key

    ROW_KEY:    [ record, ... ],                # DAT_SYS_KEY_COL.DUMP (если задан KEY_ID, иначе None); ссылка на запись классификатора
    ROW_DIC:    [ {                             # только один dict, кроме ID
                    DAT_REL.KEY_ID:   /str,
                    DAT_REL.DAT:      /date,
                    DAT_REL.OBJ_ID_1: /int,
                    DAT_REL.REC_ID_1: /int,
                    DAT_REL.OBJ_ID_2: /int,
                    DAT_REL.REC_ID_2: /int,
                }, ... ],
    ROW_TABLE:    /str,                         # self.row_table
}
```

## IO_PARS_KEYS
* наследование объекта dict. Содержит дополнительные функции и методы
* основа для запроса информации в БД
* формируется из obj_id и get
* список NAME (str) или ID (int) читаемых ключей
* если не задан - включить все доступные ключи
* для col допустимо '... as ...' - важно при чтении POINT и GEOMETRY. В результатах будет кеу=alias
* результат:
    * sels_col/sels_row - список аргументов SELECT
    * keys_col/keys_row - список ключей для формированя результата в data-формате


### пример
```python
from lib.db.io.pars.io_pars_keys import IO_PARS_KEYS
keys_pars = IO_PARS_KEYS(obj_id=dat_pars.obj_id, get=get)
keys_pars: {'sels_col': ['name', 'ST_AsGeoJSON(location) AS location'], 'sels_row': [ 'key_id', 'val', 'dat'], 'keys_col': ['40302', 'location'], 'keys_row': ['40304'], }
{
    COL_SELECT: [...],                          # self.col_select
    COL_KEY:    [...],                          # self.col_key
    COL_TABLE:  /str,                           # self.col_table

    ROW_SELECT: [...],                          # self.row_select
    ROW_KEY:    [...],                          # self.row_key
    ROW_TABLE:  /str,                           # self.row_table

    ALL_KEY:    /bool,                          # self.all_key
}
```




## IO_PARS_RELS
* наследование объекта dict
* результат: equ_1, [equ_2] - варианты условий для SQL запроса только по obj_id и rec_id
* анализируется порядок расположения объектов:
    * obj_id с меньшим индексом всегда equ_1
    * если obj_id равны: rec_id с меньшим индексом всегда в equ_1
    * если obj_id и rec_id равны: ошибка - связь объекта с самим собой не существует
    * если obj_id один, то в equ_1

### пример
```python
from lib.db.io.pars.io_pars_rels import IO_PARS_RELS
rels_pars = IO_PARS_RELS(obj_rel_1=obj_rel_1, obj_rel_2=obj_rel_2)
rels_pars: {'equ_1': ['obj_id_1=2', 'rec_id_1=33', 'obj_id_2=4', 'rec_id_2=100'], 'equ_2': []}
```




## GET_OBJ
* **ids**  = []
    * не обязательный аргумент
    * list [int или str]
* **ids_max_block** = 1000
    * максимальное количество запрашиваемых id в одном запросе (для большого количества id)
* **keys** = []
    * не обязательный аргумент
    * list [int или str]
* **where_dop_row** = []
    * дополнительные условия отбора в SQL запросе
    * не обязательный аргумент
* **ret** = [[id, key_id(int)/'location'(str), val, dat], ...]
    * основа: формат data
    * элемент 1: id записи obj
    * элемент 2: key_id (int), исключение для col: ... as ... : указывается alias (str)
    * элемент 3: val
    * элемент 4: dat, только row, при отсутствии значения = None

### примеры
```python
io_get_obj(
    group_id      = 0,
    obj           = 'file',
    ids           = [45, 89],
    keys          = ['type', 'path', 'tests', 40405],
    where_dop_row = ['not (dat is null)', 'dat<"2019-02-01"'],)
[(45, 40401, 2), (45, 40402, 'Hello'), (89, 40402, 'tests/new2'), (89, 40404, '77777', None), (89, 40405, 'zzz', '2019-01-01')]

io_get_obj(
    group_id = 0,
    obj      = 'point',
    ids      = [33,],
    keys     = [40204, "ST_AsGeoJSON(PointFromText(CONCAT('POINT(',lon,' ',lat,')'),1)) AS location"], )
[(33, 40204, 'Брест, ул.Русакова,124'), (33, 'location', '{"type": "Point", "coordinates": [23.650415, 52.0839356]}')]

io_get_obj(
    group_id = 0,
    obj      = 'geometry',
    ids      = [8, ],
    keys     = [40302, "ST_AsGeoJSON(location) AS location", 'color'], )
[(8, 40302, '558'), (8, 'location', '{"type": "GeometryCollection", "geometries": [{"type": "Point", "coordinates": [27.355957, 54.584797]}, {"type": "Polygon", "coordinates": [[[26.938477, 55.621793], [26.938477, 55.621793]]]}]}'), (8, 40304, '0.1', None)]
```

## GET_REL
* **keys** = []
    * не обязательный аргумент
    * list [int или str]
* **obj_rel_1**, **obj_rel_2**
    * не обязательный аргумент
    * list [int или str, [int]]:
        * ['file', 100]
        * ['file']
        * [4]
* **where_dop**
    * не обязательный аргумент
    * list [str]:
        * ['dat<"2020-09-09"',]
### пример
```python
io_get_rel(
    keys      = ['ngg_smoke', 104],
    obj_rel_1 = ['file',      100],
    obj_rel_2 = ['point',     ],
    where_dop = ['dat<"2020-09-09"',])
```


## PERMIT
* key_id:
    * owner_add_rw - разрешить чтение и запись
    * owner_add_ro - разрешить только чтение (установка связей с этим объектом запрещена)
    * owner_add_ro_limit - разрешить только чтение на неделю
    * owner_del - аннулировать разрешение
* dat
    * при отсутствии - '2000-01-01'
    * недопустимо две одинаковые записи в один день
    * для избежания возможных парадоксов дату запрета старых разрешений и дату нового разрешения делать РАЗНЫМИ
* проверяется:
    * для read - permit_rw ИЛИ permit_ro
    * для write - permit_rw
    * при отсутствии permit_rw И permit_ro разрешено всем
