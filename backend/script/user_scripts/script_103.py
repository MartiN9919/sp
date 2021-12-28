import geojson

from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple
from data_base_driver.record.search import search
from data_base_driver.relations.get_rel import get_related_objects
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString



def script_103(request, group_id):
	try:
		pogz = request.get('pogz',{}).get('value',[])
		informaters = get_related_objects(group_id, pogz['objectId'], pogz['recId'], ['information_diller'], [], {})
		places = []
		for informator in informaters:
		    temp = get_related_objects(group_id, informator['object_id'], informator['rec_id'], ['place_of_live'], [], {})
		    if len(temp) > 0:
		        places.append(temp[0])
		result = feature_collection_by_geometry(group_id, 30, [item['rec_id'] for item in places], [], {})
		return result
	except Exception as e:
		raise e