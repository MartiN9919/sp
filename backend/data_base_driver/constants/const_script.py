from core.settings import BASE_DIR


ENVIRONMENT_VARIABLES = [
    "PATH",
    "SYSTEM",
    "BYTE",
    "import"
]

IMPORTS = "from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple\n" \
          "from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id\n" \
          "from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, \
feature_collection_by_geometry\n"\
          "from data_base_driver.sys_notifications.set_notifications_info import add_notification\n"\
          "from datetime import datetime\n"\
          "from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path\n"\
          "from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon\n"\
          "from data_base_driver.additional_functions import str_to_sec, get_document_date_format\n"\
          "from document_driver.word_driver import get_document_from_template\n\n"\


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
    'set_file_path',
    'relations_to_geometry_id',
    'get_points_inside_polygon',
    'feature_collection_to_manticore_polygon',
    'feature_collection_by_geometry',
    'str_to_sec',
    'get_document_from_template',
    'get_document_date_format'
]

PATH_TO_REPORTS_DIR = '/reports/'

BASE_PATH_TO_USER_SCRIPTS = str(BASE_DIR) + '/script/user_scripts/'

