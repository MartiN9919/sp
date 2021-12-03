import geojson

from data_base_driver.record.get_record import get_object_param_by_key
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



def script_111(request, group_id):
	try:
		region = request.get('region',{}).get('value',[])
		polygon = feature_collection_to_manticore_polygon(region)
		rels = io_get_rel(group_id, [50211], [25], [35], [], {}, True)
		points = get_points_inside_polygon(polygon['in_polygon'][0], [], group_id)
		persons = [{'rec_id': item['rec_id_2'], 'sec': item['sec']} for item in rels]
		points_id = []
		for person in persons:
		    point_id = relations_to_geometry_id(group_id, 25, 35, int(person['rec_id']), [50162], {})
		    if point_id[0] in points:
		        points_id.append({'person_id': person['rec_id'],
		                            'point_id': point_id})
		fc_points = feature_collection_by_geometry(group_id, 25, [item['point_id'][0] for item in points_id], [], {})
		for feature in fc_points['features']:
		    person_id = [int(item['person_id']) for item in points_id if int(item['point_id'][0]) == feature['rec_id']][
		        0]
		    feature['properties']['hint'] = 'Место жительства ' + get_object_param_by_key(group_id, 35, person_id,
		                                                                                    35001)
		return fc_points
	except Exception as e:
		raise e