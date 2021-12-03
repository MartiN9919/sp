import geojson

from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple, \
	io_get_rel
from data_base_driver.record.get_record import get_object_param_by_key
from data_base_driver.record.search import search
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec



def script_116(request, group_id):
	try:
		rels = io_get_rel(group_id, [50214], [25], [35], [], {}, True)
		points = [{'rec_id': item['rec_id_1'], 'person_id': item['rec_id_2'], 'sec': item['sec']} for item in rels]
		fc_points = feature_collection_by_geometry(group_id, 25, [item['rec_id'] for item in points], [], {})
		for feature in fc_points['features']:
			person_id = [item['person_id'] for item in points if int(item['rec_id']) == feature['rec_id']][0]
			feature['properties']['hint'] = 'Место задержания ' + get_object_param_by_key(group_id, 35, person_id,
																						  35001)
		return fc_points
	except Exception as e:
		raise e