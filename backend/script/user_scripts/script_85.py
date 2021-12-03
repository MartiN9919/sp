import geojson

from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple, io_get_rel
from data_base_driver.record.search import search
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec, get_date_time_from_sec
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString



def script_85(request, group_id):
	try:
		pogz = request.get('pogz',{}).get('value',[])
		rels = io_get_rel(group_id, [], [pogz['objectId'], pogz['recId']], [40], [], {}, True)
		naryads1 = [int(item['rec_id_2']) for item in rels if int(item['rec_id_1']) == pogz['recId']]
		naryads2 = [int(item['rec_id_1']) for item in rels if int(item['rec_id_2']) == pogz['recId']]
		naryads = naryads2 + naryads1
		point_rels = []
		for item in naryads:
		    point_rels += io_get_rel(group_id, [], [40, item], [25], [], {}, True)
		result = []
		for item in point_rels:
		    temp = feature_collection_by_geometry(group_id, 25, [int(item['rec_id_1'])], [50163], {})
		    date_time = get_date_time_from_sec(item['sec'])
		    temp['features'][0]['properties']['date'] = date_time
		    result += temp['features']
		fc_geometries = feature_collection_by_geometry(group_id, 25, [], [30303], {})
		fc_geometries['features'] = result
		return fc_geometries
	except Exception as e:
		raise e