from core.settings import BASE_DIR


ENVIRONMENT_VARIABLES = [
    "PATH",
    "SYSTEM",
    "BYTE",
    "import"
]

IMPORTS = "from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple\n" \
          "from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id\n" \
          "from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc\n"\
          "from data_base_driver.sys_notifications.set_notifications_info import add_notification\n"\
          "from datetime import datetime\n"\
          "from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path\n\n"

ENABLED_FUNCTIONS = [
    'io_set',
    'io_get_obj_mysql_tuple',
    'io_get_rel_mysql_tuple',
    'io_get_geometry_tree',
    'obj_list',
    'key_list',
    'rel_rec_to_el',
    'el_to_rec_id',
    'rel_to_geo_fc',
    'geo_id_to_fc',
    'int',
    'list',
    'find',
    'split',
    'open',
    'close',
    'write',
    'set_file_path'
]

PATH_TO_REPORTS_DIR = '/reports/'

BASE_PATH_TO_USER_SCRIPTS = str(BASE_DIR) + '/script/user_scripts/'

