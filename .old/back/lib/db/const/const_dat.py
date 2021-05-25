# -*- coding: utf-8 -*-

from   lib.db.const.const_connect import CONNECT


##################################################################################
# DAT_SYS_SCRIPT
##################################################################################
class DAT_SYS_SCRIPT:
    TABLE_SHORT      = 'sys_script'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
    ID               = 'id'
    PARENT_ID        = 'parent_id'
    NAME             = 'name'
    TITLE            = 'title'
    ICON             = 'icon'
    HINT             = 'hint'
    CONTENT          = 'content'
    DESCRIPT         = 'descript'
    ENABLED          = 'enabled'
    OWNER_LINE       = 'owner_line'

    # имена переменных при запуске скрипта
    VAR_USER_ID      = 'sys_var_user_id'
    VAR_GROUP_ID     = 'group_id'



##################################################################################
# DAT_SYS_ID
##################################################################################
class DAT_SYS_ID:
    TABLE_SHORT      = 'sys_id'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
    OBJ_ID           = 'obj_id'
    ID               = 'id'



##################################################################################
# DAT_SYS_OBJ
##################################################################################
# !!! SYNC PARTITION REL_DOP !!!
# !!! FIELDS CHANGE DUMP !!!
##################################################################################
class DAT_SYS_OBJ:
    TABLE_SHORT      = 'sys_obj'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
    DUMP             = None         # заполняется в lib.db.const.const_dat - КОПИЯ ТАБЛИЦЫ В ПАМЯТИ
    ID               = 'id'
    NAME             = 'name'
    TITLE            = 'title'
    TITLE_SINGLE     = 'title_single'
    ICON             = 'icon'
    DESCRIPT         = 'descript'

    ID_REL           = 1
    ID_FREE          = 10

    NAME_REL         = 'rel'
    NAME_POINT       = 'point'
    NAME_GEOMETRY    = 'geometry'
    NAME_VAL         = 'val'                       # ?????



##################################################################################
# DAT_SYS_KEY
##################################################################################
# !!! FIELDS CHANGE DUMP !!!
##################################################################################
class DAT_SYS_KEY:
    TABLE_SHORT      = 'sys_key'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
    DUMP             = None         # заполняется в lib.db.const.const_dat - КОПИЯ ТАБЛИЦЫ В ПАМЯТИ
    ID               = 'id'
    OBJ_ID           = 'obj_id'
    COL              = 'col'
    NEED             = 'need'
    TYPE_VAL         = 'type_val'
    LIST_ID          = 'list_id'
    NAME             = 'name'
    TITLE            = 'title'
    HINT             = 'hint'

    TYPE_STR         = 'str'
    TYPE_INT         = 'int'
    TYPE_FLOAT       = 'float'
    TYPE_BIT         = 'bit'
    TYPE_DATA        = 'data'
    TYPE_DATATIME    = 'datatime'
    TYPE_GEOMETRY    = 'geometry'

    TYPE_LIST        = (
        TYPE_STR,
        TYPE_INT,
        TYPE_FLOAT,
        TYPE_BIT,
        TYPE_DATA,
        TYPE_DATATIME,
        TYPE_GEOMETRY,
    )

    NAME_REL_KEY_ID         = 'key_id'

    NAME_OWNER_ADD_RW       = 'owner_add_rw'
    NAME_OWNER_ADD_RO       = 'owner_add_ro'
    NAME_OWNER_ADD_RO_LIMIT = 'owner_add_ro_limit'
    NAME_OWNER_DEL          = 'owner_del'
    NAME_OWNER_LIST         = (NAME_OWNER_ADD_RW, NAME_OWNER_ADD_RO, NAME_OWNER_ADD_RO_LIMIT, NAME_OWNER_DEL)

    NAME_POINT_LOCATION     = "ST_AsGeoJSON(PointFromText(CONCAT('POINT(',lon,' ',lat,')'),1)) AS location"
    NAME_POINT_ADDRESS      = 'address'

    NAME_GEOMETRY_PARENT_ID = 'parent_id'
    NAME_GEOMETRY_NAME      = 'name'
    NAME_GEOMETRY_ICON      = 'icon'
    NAME_GEOMETRY_LOCATION  = "ST_AsGeoJSON(location) AS location"



##################################################################################
# DAT_OWNER
##################################################################################
# !!! FIELDS CHANGE DUMP !!!
##################################################################################
class DAT_OWNER:
    DUMP             = None         # заполняется в lib.db.const.const_dat - КОПИЯ ТАБЛИЦ В ПАМЯТИ

class DAT_OWNER_USERS:
    TABLE_SHORT      = 'owner_users'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
    ID               = 'id'
    OWNER_GROUPS_ID  = 'owner_groups_id'
    ENABLED          = 'enabled'
    DESCRIPT         = 'descript'

class DAT_OWNER_GROUPS:
    TABLE_SHORT      = 'owner_groups'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
    ID               = 'id'
    OWNER_REGIONS_ID = 'owner_regions_id'                   # не доступно в dump
    OWNER_LINES_ID   = 'owner_lines_id'                     # не доступно в dump
    TITLE            = 'title'
    DESCRIPT         = 'descript'

    GROUPS_ID        = 'groups_id'                          # доступно только в dump
    REGIONS_ID       = 'regions_id'                         # доступно только в dump
    LINES_ID         = 'lines_id'                           # доступно только в dump
    ID_ADMIN         = 1


class DAT_OWNER_BASE:
    ID               = 'id'
    PARENT_ID        = 'parent_id'
    TITLE            = 'title'
class DAT_OWNER_REGIONS(DAT_OWNER_BASE):
    TABLE_SHORT      = 'owner_regions'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
class DAT_OWNER_LINES(DAT_OWNER_BASE):
    TABLE_SHORT      = 'owner_lines'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT




##################################################################################
# DAT_SYS_LIST
##################################################################################
class DAT_SYS_LIST_TOP:
    TABLE_SHORT      = 'sys_list_top'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
    ID               = 'id'
    NAME             = 'name'
    TITLE            = 'title'
    STRONG           = 'strong'

class DAT_SYS_LIST_DOP:
    TABLE_SHORT      = 'sys_list_dop'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
    ID               = 'id'
    KEY_ID           = 'key_id'
    VAL              = 'val'




##################################################################################
# DAT_OBJ
##################################################################################
class DAT_OBJ_COL:
    table_name       = lambda group: 'obj_'+group+'_col'
    ID               = 'id'

class DAT_OBJ_ROW:
    table_name       = lambda group: 'obj_'+group+'_row'
    ID               = 'id'
    KEY_ID           = 'key_id'
    VAL              = 'val'
    DAT              = 'dat'
    LIST             = (KEY_ID, VAL, DAT,)




##################################################################################
# DAT_REL
##################################################################################
class DAT_REL:
    TABLE_SHORT      = 'rel'
    TABLE            = CONNECT.DATA.NAME+'.'+TABLE_SHORT
    #ID               = 'id'
    KEY_ID           = 'key_id'
    DAT              = 'dat'
    OBJ_ID_1         = 'obj_id_1'
    REC_ID_1         = 'rec_id_1'
    OBJ_ID_2         = 'obj_id_2'
    REC_ID_2         = 'rec_id_2'
    LIST             = (KEY_ID, DAT, OBJ_ID_1, REC_ID_1, OBJ_ID_2, REC_ID_2,)




##################################################################################
# DAT_SYS_ALERT
##################################################################################
class DAT_SYS_ALERT:
    TABLE_SHORT  = 'sys_alert'
    TABLE        = CONNECT.DATA.NAME+'.'+TABLE_SHORT

    ID           = 'id'
    TYPE         = 'type'
    CONTENT      = 'content'
    WAIT         = 'wait'
    OWNER        = 'owner'
    USERS        = 'users'
    GROUPS       = 'group_user'
    ENABLED      = 'enabled'
    DESCRIPT     = 'descript'

    TYPE_ERROR   = 'error'
    TYPE_INFO    = 'info'
    TYPE_WARN    = 'warn'
    TYPE_LIST    = (
        (TYPE_INFO,  'информация'),
        (TYPE_WARN,  'предупреждение'),
        (TYPE_ERROR, 'ошибка'),
    )




##################################################################################
# DUMP INI
##################################################################################
from lib.db.dump.dump_obj   import DUMP_OBJ
from lib.db.dump.dump_key   import DUMP_KEY
from lib.db.dump.dump_owner import DUMP_OWNER

DAT_SYS_OBJ.DUMP = DUMP_OBJ()
DAT_SYS_KEY.DUMP = DUMP_KEY()
DAT_OWNER.DUMP   = DUMP_OWNER()
