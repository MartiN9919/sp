from core.settings import BASE_DIR


ENVIRONMENT_VARIABLES = [
    "PATH",
    "SYSTEM",
    "BYTE",
    "import"
]


IMPORTS = \
    "import json\n"\
    "import geojson\n" \
    "import geopandas\n"\
    "\n" \
    "from objects.geometry.geometry_transformations import get_polygon_from_lines\n"\
    "from objects.relations.get_rel import get_related_objects\n"\
    "from data_base_driver.sys_key.get_key_dump import get_key_by_id\n"\
    "from data_base_driver.sys_key.get_list import get_item_list_value\n"\
    "from document_driver.exel_driver import get_xlsx_document_from_template\n"\
    "from objects.record.get_record import get_object_record_by_id_http, get_record_title\n"\
    "from objects.record.get_record import get_object_param_by_key\n" \
    "from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple, io_get_rel, io_get_obj\n" \
    "from objects.record.search import search\n" \
    "from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id\n" \
    "from data_base_driver.input_output.io_geo import relations_to_geometry_id, \
feature_collection_by_geometry, get_geometries, get_points_inside_polygon\n"\
    "from data_base_driver.sys_notifications.set_notifications_info import add_notification\n"\
    "from datetime import datetime\n"\
    "from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path\n"\
    "from objects.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_line_buffer_polygon, get_distance_between_point_math\n"\
    "from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, get_document_date_format\n"\
    "from document_driver.word_driver import get_document_from_template, get_dossier_for_object\n"\
    "from shapely.geometry import Polygon, Point, LineString, MultiPoint\n"\
    "from docx import Document\n"\
    "from docx.shared import RGBColor\n"\
    "from synonyms_manager.get_synonyms import get_synonyms\n"\
    "from document_driver.classifier_driver import get_exel_document\n"\
    "from core.projectSettings.constant import MEDIA_ROOT, DOCUMENT_ROOT\n\n"



ENABLED_FUNCTIONS = [
    'io_set',
    'io_get_obj_mysql_tuple',
    'io_get_rel_mysql_tuple',
    'io_get_geometry_tree',
    'obj_list',
    'key_list',
    'rel_rec_to_el',
    'el_to_rec_id',
    'int',
    'set',
    'str',
    'list',
    'len',
    'sorted',
    'keys',
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
    'Feature',
    'FeatureCollection',
    'append',
    'get',
    'print',
    'search',
    'io_get_rel',
    'io_get_obj',
    'int',
    'get_date_time_from_str',
    'get_related_objects',
    'get_dossier_for_object',
    'Polygon',
    'Point',
    'LineString',
    'MultiPoint',
    'get_line_buffer_polygon',
    'contains',
    'intersects',
    'get_second_range',
    'get_date_time_from_sec',
    'get_object_param_by_key',
    'get_object_record_by_id_http',
    'get_xlsx_document_from_template',
    'get_document_date_format',
    'get_key_by_id',
    'get_item_list_value',
    'overlaps',
    'intersection',
    'GeoSeries',
    'get_document_from_template',
    'range',
    'get_geometries',
    'get_polygon_from_lines',
    'loads',
    'get_distance_between_point_math',
    'Document',
    'get_synonyms',
    'RGBColor',
    'save',
    'get_person_info',
    'get_record_title',
    'get_exel_document'
]

PATH_TO_REPORTS_DIR = '/reports/'

BASE_PATH_TO_USER_SCRIPTS = str(BASE_DIR) + '/script/user_scripts/'

