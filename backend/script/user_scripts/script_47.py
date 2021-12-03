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



def script_47(request, group_id):
	try:
		date_start = request.get('date_start',{}).get('value',[])
		date_end = request.get('date_end',{}).get('value',[])
		list_id = request.get('list_id',{}).get('value',[])
		date_time_start = date_start + ' 00:00:00'
		date_time_end = date_end + ' 00:00:00'
		time_interval = {'second_start': str_to_sec(date_time_start), 'second_end': str_to_sec(date_time_end)}
		relations = io_get_rel(group_id, [50122], [20], [45], [list_id], {}, True)
		docs = []
		for relation in relations:
		    docs.append(int(relation['rec_id_1']))
		persons = []
		for doc in docs:
		    rels = io_get_rel(group_id, ['role_in_unlegal_working'], ['person_p'], ['doc', doc], [], {}, True)
		    if len(rels) > 0:
		        for rel in rels:
		            persons.append(int(rel['rec_id_2']))
		persons = list(set(persons))
		geometries = []
		for person in persons:
		    geometries += relations_to_geometry_id(group_id, 30, 35, person, [50147], time_interval)
		fc_new = feature_collection_by_geometry(group_id, 30, geometries, [30303], {})
		points = []
		for person in persons:
		    points += relations_to_geometry_id(group_id, 25, 35, person, [50127], {})
		fc_points = feature_collection_by_geometry(group_id, 25, points, [50163], {})
		fc_new['features'] += fc_points['features']
		return fc_new
	except Exception as e:
		raise e