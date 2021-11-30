import geojson

from document_driver.exel_driver import get_xlsx_document_from_template
from data_base_driver.record.get_record import get_object_record_by_id_http
from data_base_driver.record.get_record import get_object_param_by_key
from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple, io_get_rel
from data_base_driver.record.search import search
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, get_document_date_format
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString



def script_118(request, group_id):
	try:
		fc_geometries = feature_collection_by_geometry(group_id, 30, [59, 60, 61, 62, 63], [50212], {})
		max = 0
		for feature in fc_geometries['features']:
		    if int(feature['properties']['hint']) > max:
		        max = int(feature['properties']['hint'])
		for feature in fc_geometries['features']:
		    feature['properties']['value'] = (int(feature['properties']['hint']) / max) * 100
		fc_geometries['style'] = {'coloring': "green_max"}
		return fc_geometries
	except Exception as e:
		raise e