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
from shapely.geometry import Polygon, Point, LineString



def script_107(request, group_id):
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
		polygons = []
		for temp in result_path_list:
		    temp_fc = feature_collection_by_geometry(group_id, 30, [temp['rec_id']], [], {})[0]
		    for geometry in temp_fc['geometry']['geometries']:
		        if geometry['type'] == 'LineString':
		            polygons += get_line_buffer_polygon(LineString(geometry['coordinates']))['features']
		result = []
		for temp in polygons:
		    num = 0
		    temp_res = []
		    polygon1 = Polygon(temp['geometry']['coordinates'][0])
		    for temp2 in polygons:
		        polygon2 = Polygon(temp2['geometry']['coordinates'][0])
		        if polygon1.overlaps(polygon2):
		            num += 1
		            temp_res.append(polygon2)
		    if num >= 5:
		        for temp2 in temp_res:
		            if polygon1.intersection(temp2).is_empty:
		                continue
		            polygon1 = polygon1.intersection(temp2)
		        result += geopandas.GeoSeries([polygon1]).__geo_interface__['features']
		fc_geometry = feature_collection_by_geometry(group_id, 30, [], [], {})
		fc_geometry['features'] = result
		return fc_geometry
	except Exception as e:
		raise e