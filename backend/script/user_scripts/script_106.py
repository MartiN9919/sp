import json
import geojson
import geopandas

from objects.geometry.geometry_transformations import get_polygon_from_lines
from objects.relations.get_rel import get_related_objects
from data_base_driver.sys_key.get_key_info import get_key_by_id
from data_base_driver.sys_key.get_list import get_item_list_value
from document_driver.exel_driver import get_xlsx_document_from_template
from objects.record.get_record import get_object_record_by_id_http, get_record_title
from objects.record.get_record import get_object_param_by_key
from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple, io_get_rel, io_get_obj
from objects.record.search import search
from data_base_driver.sys_key.get_object_info import objects_list
from data_base_driver.input_output.io_geo import relations_to_geometry_id, feature_collection_by_geometry, get_geometries, get_points_inside_polygon
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from objects.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_line_buffer_polygon, get_distance_between_point_math
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, get_document_date_format
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString, MultiPoint
from docx import Document
from docx.shared import RGBColor
from synonyms_manager.get_synonyms import get_synonyms
from document_driver.classifier_driver import get_exel_document
from core.projectSettings.constant import MEDIA_ROOT, DOCUMENT_ROOT



def script_106(request, group_id):
	try:
		date_start = request.get('date_start',{}).get('value',[])
		date_end = request.get('date_end',{}).get('value',[])
		time_interval = get_second_range(date_start, date_end)
		rels = io_get_rel(group_id, [50209], [25], [35], [], time_interval, True)
		persons = [{'rec_id': item['rec_id_2'], 'sec': item['sec']} for item in rels]
		points = [{'rec_id': item['rec_id_1'], 'sec': item['sec']} for item in rels]
		result_path_list = []
		for person in persons:
		    paths = io_get_rel(group_id, [50208], [35, person['rec_id']], [30], [], time_interval, True)
		    paths = [{'rec_id': item['rec_id_1'], 'sec': item['sec']} for item in paths]
		    result_path_list += paths
		features = []
		for temp in result_path_list:
		    temp_fc = feature_collection_by_geometry(group_id, 30, [temp['rec_id']], [], {})[0]
		    temp_fc['properties']['date'] = get_date_time_from_sec(temp['sec'])
		    # temp_fc['properties']['class'] = 'ant'
		    features.append(temp_fc)
		for temp in points:
		    temp_fc = feature_collection_by_geometry(group_id, 25, [temp['rec_id']], [], {})[0]
		    temp_fc['properties']['date'] = get_date_time_from_sec(temp['sec'])
		    temp_fc['properties']['class'] = 'icon-svg-point_detention_inside'
		    features.append(temp_fc)
		fc_geometry = feature_collection_by_geometry(group_id, 30, [item['rec_id'] for item in result_path_list], [], {})
		fc_geometry['features'] = features
		return fc_geometry
	except Exception as e:
		raise e