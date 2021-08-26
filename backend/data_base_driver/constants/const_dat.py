from data_base_driver.constants.connect_db import VEC_DATA


##################################################################################
# DAT_SYS_SCRIPT
##################################################################################


class DAT_SYS_SCRIPT():
    TABLE_SHORT = 'sys_script'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    ID = 'id'
    PARENT_ID = 'parent'
    NAME = 'name'
    TITLE = 'title'
    ICON = 'icon'
    HINT = 'hint'
    CONTENT = 'content'
    VARIABLES = 'variables'
    DESCRIPT = 'descript'
    ENEBLED = 'enabled'
    OWNER_LINE = 'owner'
    TYPE = 'type'

    TYPE_MAP = 'map'
    TYPE_REPORT = 'report'

    TYPE_LIST = (
        (TYPE_MAP, 'Карты'),
        (TYPE_REPORT, 'Отчеты')
    )

    # имена переменных при запуске скрипта
    VAR_USER_ID = 'sys_var_user_id'
    VAR_GROUP_ID = 'group_id'

    ICON_CHOICES = [
        ('home_icon', 'HOME'),
        ('apple_icon', 'APPLE'),
        ('celery_icon', 'CELERY'),
        ('car_icon', 'CAR'),
        ('cat_icon', 'CAT'),
    ]


##################################################################################
# DAT_SYS_ID
##################################################################################
class DAT_SYS_ID:
    TABLE_SHORT = 'sys_id'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    OBJ_ID = 'obj_id'
    ID = 'id'


##################################################################################
# DAT_SYS_OBJ
##################################################################################
# !!! SYNC PARTITION REL_DOP !!!
# !!! FIELDS CHANGE DUMP !!!
##################################################################################
class DAT_SYS_OBJ:
    TABLE_SHORT = 'sys_obj'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    DUMP = None  # заполняется в lib.db.const.const_dat - КОПИЯ ТАБЛИЦЫ В ПАМЯТИ
    ID = 'id'
    NAME = 'name'
    TITLE = 'title'
    TITLE_SINGLE = 'title_single'
    ICON = 'icon'
    DESCRIPT = 'descript'

    ID_REL = 1
    ID_FREE = 10

    NAME_REL = 'rel'
    NAME_POINT = 'point'
    NAME_GEOMETRY = 'geometry'
    NAME_VAL = 'val'  # ?????


class DAT_SYS_PHONE_NUMBER_FORMAT:
    TABLE_SHORT = 'sys_phone_number_format'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    ID = 'id'
    COUNTRY = 'country'
    COUNTRY_CODE = 'country_code'
    LENGTH = 'length'
    DUMP = None


##################################################################################
# DAT_SYS_KEY
##################################################################################
# !!! FIELDS CHANGE DUMP !!!
##################################################################################
class DAT_SYS_KEY:
    TABLE_SHORT = 'sys_key'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    DUMP = None  # заполняется в lib.db.const.const_dat - КОПИЯ ТАБЛИЦЫ В ПАМЯТИ
    ID = 'id'
    OBJ_ID = 'obj_id'
    COL = 'col'
    NEED = 'need'
    TYPE_VAL = 'type'
    LIST_ID = 'list_id'
    NAME = 'name'
    TITLE = 'title'
    HINT = 'hint'
    DESCRIPT = 'descript'
    REL_OBJ_1_ID = 'rel_obj_1_id'
    REL_OBJ_2_ID = 'rel_obj_2_id'
    REL_OBJ_1 = 'rel_obj_1'
    REL_OBJ_2 = 'rel_obj_2'
    OBJ = 'obj'
    LIST = 'list'
    IND_REL_OBJ_1 = 'ind_rel_obj_1'
    IND_REL_OBJ_2 = 'ind_rel_obj_2'
    GROUP = 'group'
    GROUP_ID = 'group_id'
    PATH = 'path'
    PRIORITY = 'priority'

    TYPE_STR = 'text'
    TYPE_INT = 'number'
    TYPE_BIT = 'checkbox'
    TYPE_DATA = 'date'
    TYPE_DATATIME = 'datetime'
    TYPE_GEOMETRY = 'geometry'
    TYPE_PHONE_NUMBER = 'phone_number'

    TYPE_LIST = (
        (TYPE_INT, "Число"),
        (TYPE_STR, 'Текст'),
        (TYPE_DATATIME, 'Дата/Время'),
        (TYPE_DATA, 'Дата'),
        (TYPE_PHONE_NUMBER, 'Номер телефона'),
        (TYPE_BIT, 'Да/Нет'),
        (TYPE_GEOMETRY, 'Точка/Путь/Полигон'),
    )

    NAME_REL_KEY_ID = 'key_id'
    NAME_OWNER_ADD_RW = 'owner_add_rw'
    NAME_OWNER_ADD_RO = 'owner_add_ro'
    NAME_OWNER_ADD_RO_LIMIT = 'owner_add_ro_limit'
    NAME_OWNER_DEL = 'owner_del'
    NAME_OWNER_LIST = (NAME_OWNER_ADD_RW, NAME_OWNER_ADD_RO, NAME_OWNER_ADD_RO_LIMIT, NAME_OWNER_DEL)
    NAME_POINT_LOCATION = "ST_AsGeoJSON(ST_PointFromText(CONCAT('POINT(',lon,' ',lat,')'),0)) AS location"  # изменем с 1 на 0 в связи с переходом на новую версию mysql
    NAME_POINT_ADDRESS = 'address'

    NAME_GEOMETRY_PARENT_ID = 'parent_id'
    NAME_GEOMETRY_NAME = 'name'
    NAME_GEOMETRY_ICON = 'icon'
    NAME_GEOMETRY_LOCATION = "ST_AsGeoJSON(location) AS location"


##################################################################################
# DAT_OWNER
##################################################################################
# !!! FIELDS CHANGE DUMP !!!
##################################################################################
class DAT_OWNER:
    DUMP = None  # заполняется в lib.db.const.const_dat - КОПИЯ ТАБЛИЦ В ПАМЯТИ


class DAT_OWNER_USERS:
    TABLE_SHORT = 'authentication_modelcustomuser'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    ID = 'id'
    PASSWORD = 'password'
    LAST_LOGIN = 'last_login'
    IS_SUPERUSER = 'is_superuser'
    USERNAME = 'username'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    IS_STAFF = 'is_staff'
    IS_ACTIVE = 'is_active'
    OWNER_GROUPS_ID = 'owner_groups_id'
    OWNER_GROUPS = 'owner_groups'
    ENABLED = 'is_active'
    DESCRIPT = 'descript'
    USER_PERMISSION = 'user_permissions'


class DAT_OWNER_GROUPS:
    TABLE_SHORT = 'owner_groups'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    ID = 'id'
    OWNER_REGIONS_ID = 'owner_regions_id'  # не доступно в dump
    OWNER_LINES_ID = 'owner_lines_id'  # не доступно в dump
    TITLE = 'title'
    DESCRIPT = 'descript'
    OWNER_REGIONS = 'owner_regions'
    OWNER_LINES = 'owner_lines'

    GROUPS_ID = 'groups_id'  # доступно только в dump
    REGIONS_ID = 'regions_id'  # доступно только в dump
    LINES_ID = 'lines_id'  # доступно только в dump
    ID_ADMIN = 1


class DAT_OWNER_BASE:
    ID = 'id'
    PARENT_ID = 'parent_id'
    TITLE = 'title'


class DAT_OWNER_REGIONS(DAT_OWNER_BASE):
    TABLE_SHORT = 'owner_regions'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT


class DAT_OWNER_LINES(DAT_OWNER_BASE):
    TABLE_SHORT = 'owner_lines'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT


##################################################################################
# DAT_SYS_LIST
##################################################################################
class DAT_SYS_LIST_TOP:
    TABLE_SHORT = 'sys_list_top'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    ID = 'id'
    NAME = 'name'
    TITLE = 'title'
    STRONG = 'strong'


class DAT_SYS_LIST_DOP:
    TABLE_SHORT = 'sys_list_dop'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    ID = 'id'
    KEY_ID = 'key_id'
    LIST_ID = 'list_id'
    VAL = 'val'


class DAT_SYS_FILES:
    TABLE_SHORT = 'sys_reports'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    ID = 'id'
    PATH = 'path'
    NAME = 'name'
    OWNER_LINE = 'owner_line'
    OWNER_REGION = 'owner_region'
    OWNER_LINE_ID = 'owner_line_id'
    OWNER_REGION_ID = 'owner_region_id'
    DATE_AUTO_REMOVE = 'date_auto_remove'
    STATUS = 'status'
    PARAMS = 'params'

    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    ERROR = 'error'
    STATUS_LIST = (
        (IN_PROGRESS, "в процессе"),
        (DONE, 'готов'),
        (ERROR, 'ошибка создания отчета'),
    )


##################################################################################
# DAT_OBJ
##################################################################################
class DAT_OBJ_COL:
    table_name = lambda group: 'obj_' + group + '_col'
    ID = 'rec_id'
    DAT = 'dat'


class DAT_OBJ_ROW:
    table_name = lambda group: 'obj_' + group + '_row'
    ID = 'rec_id'
    KEY_ID = 'key_id'
    VAL = 'val'
    DAT = 'dat'
    SEC = 'sec'
    LIST = (KEY_ID, VAL, DAT,)


##################################################################################
# DAT_REL
##################################################################################
class DAT_REL:
    TABLE_SHORT = 'rel'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT
    REC_ID = 'rec_id'
    KEY_ID = 'key_id'
    DAT = 'dat'
    SEC = 'sec'
    OBJ_ID_1 = 'obj_id_1'
    REC_ID_1 = 'rec_id_1'
    OBJ_ID_2 = 'obj_id_2'
    REC_ID_2 = 'rec_id_2'
    VAL = 'val'
    LIST = (KEY_ID, DAT, OBJ_ID_1, REC_ID_1, OBJ_ID_2, REC_ID_2,)


##################################################################################
# DAT_SYS_ALERT
##################################################################################
class DAT_SYS_NOTIFY:
    TABLE_SHORT = 'sys_notify'
    TABLE = VEC_DATA['NAME'] + '.' + TABLE_SHORT

    ID = 'id'
    FROM_ID = 'from_user_id'
    TO_ID = 'to_user_id'
    DATE_TIME = 'date_time'
    TYPE = 'type'
    CONTENT = 'content'
    FILE_ID = 'file_id'
    FILE = 'file'
    GEOMETRY = 'geometry'

    FROM_USER = 'from_user'
    TO_USER = 'to_user'

    TYPE_ERROR = 'error'
    TYPE_INFO = 'information'
    TYPE_WARNING = 'warning'
    TYPE_LIST = (
        (TYPE_INFO, 'информация'),
        (TYPE_WARNING, 'предупреждение'),
        (TYPE_ERROR, 'ошибка'),
    )


class DAT_SYS_TEMPLATES:
    TABLE_SHORT = 'sys_templates'
    TABLE = VEC_DATA['NAME'] + TABLE_SHORT

    ID = 'id'
    GROUP_ID = 'group_id'
    TITLE = 'title'
    ACTIVE_SCRIPTS = 'active_scripts'
    PASSIVE_SCRIPTS = 'passive_scripts'


class DAT_SYS_SCRIPT_RESULT:
    TABLE_SHORT = 'sys_script_result'
    TABLE = VEC_DATA['NAME'] + TABLE_SHORT

    ID = 'id'
    NAME = 'name'
    USER = 'user'
    PARAMS = 'params'
    RESULT = 'result'
    DATE = 'date'


##################################################################################
# DUMP INI
##################################################################################
from data_base_driver.dump.dump_obj import DUMP_OBJ
from data_base_driver.dump.dump_key import DUMP_KEY
from data_base_driver.dump.dump_owner import DUMP_OWNER
from data_base_driver.dump.dump_phone_number import DUMP_PHONE_NUMBER_FORMAT

DAT_SYS_OBJ.DUMP = DUMP_OBJ()
DAT_SYS_KEY.DUMP = DUMP_KEY()
DAT_OWNER.DUMP = DUMP_OWNER()
DAT_SYS_PHONE_NUMBER_FORMAT.DUMP = DUMP_PHONE_NUMBER_FORMAT()
