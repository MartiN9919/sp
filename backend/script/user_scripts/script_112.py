import geojson
import geopandas

from data_base_driver.sys_key.get_key_dump import get_key_by_id
from data_base_driver.sys_key.get_list import get_item_list_value
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
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon, get_line_buffer_polygon
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, get_document_date_format
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString, MultiPoint



def script_112(request, group_id):
	try:
		rels = io_get_rel(group_id, [50210], [25], [35], [], {}, True)
		points = [{'rec_id': item['rec_id_1'], 'sec': item['sec'], 'key_id': item['key_id'], 'val': item['val']} for
		            item in rels]
		fc_points = feature_collection_by_geometry(group_id, 25, [item['rec_id'] for item in points], [50100], {})
		result = {}
		for feature in fc_points['features']:
		    if not result.get(feature['properties']['hint']):
		        result[feature['properties']['hint']] = []
		    result[feature['properties']['hint']].append(feature['geometry']['coordinates'])
		temp = []
		for res in result:
		    if len(result[res]) < 3:
		        continue
		    temp.append({'type': 'Feature', 'geometry': MultiPoint(result[res]).convex_hull.__geo_interface__, 'properties': {'hint': 'Всего нарушений: ' + str(len(result[res]))}})
		fc_points['features'] = temp
		return fc_points
	except Exception as e:
		raise e