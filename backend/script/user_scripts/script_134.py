import json
import geojson
import geopandas

from data_base_driver.geometry.geometry_transformations import get_polygon_from_lines
from data_base_driver.relations.get_rel import get_related_objects
from data_base_driver.sys_key.get_key_dump import get_key_by_id
from data_base_driver.sys_key.get_list import get_item_list_value
from document_driver.exel_driver import get_xlsx_document_from_template
from data_base_driver.record.get_record import get_object_record_by_id_http
from data_base_driver.record.get_record import get_object_param_by_key
from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple, io_get_rel, io_get_obj
from data_base_driver.record.search import search
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry, get_geometries
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon, get_line_buffer_polygon, get_distance_between_point_math
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, get_document_date_format
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString, MultiPoint



def script_134(request, group_id):
	try:
		region = request.get('region',{}).get('value',[])
		date_start = request.get('date_start',{}).get('value',[])
		date_end = request.get('date_end',{}).get('value',[])
		date_time_start = date_start + ' 00:00:00'
		date_time_end = date_end + ' 00:00:00'
		time_interval = {'second_start': str_to_sec(date_time_start), 'second_end': str_to_sec(date_time_end)}
		
		start_region_feature = region['features'][0]
		start_region_feature['properties']['color'] = 'rgba(0, 0, 255, 0.3)'
		
		points = relations_to_geometry_id(group_id, 25, 0, 0, [], time_interval)
		geometries = relations_to_geometry_id(group_id, 30, 0, 0, [], time_interval)
		
		fc_points = feature_collection_by_geometry(group_id, 25, points, [50163], {})
		fc_polygons = feature_collection_by_geometry(group_id, 30, geometries, [30303], {})
		features = []
		polygon = Polygon(region['features'][0]['geometry']['coordinates'][0])
		for feature in fc_points['features']:
		    if polygon.contains(Point(feature['geometry']['coordinates'])):
		        features.append(feature)
		for feature in fc_polygons['features']:
		    geometry = feature['geometry']['geometries'][0]
		    if geometry['type'] == 'Polygon':
		        if polygon.intersects(Polygon(geometry['coordinates'][0])):
		            features.append(feature)
		    elif geometry['type'] == 'LineString':
		        if polygon.intersects(LineString(geometry['coordinates'])):
		            features.append(feature)
		fc_polygons['features'] = features
		fc_polygons['features'] += [start_region_feature]
		return fc_polygons
	except Exception as e:
		raise e