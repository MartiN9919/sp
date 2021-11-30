import geojson

from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple, io_get_rel
from data_base_driver.record.search import search
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString



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