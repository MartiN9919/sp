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



def script_133(request, group_id):
	try:
		region = request.get('region',{}).get('value',[])
		date_start = request.get('date_start',{}).get('value',[])
		date_end = request.get('date_end',{}).get('value',[])
		date_time_start = date_start + ' 00:00:00'
		date_time_end = date_end + ' 00:00:00'
		time_interval = {'second_start': str_to_sec(date_time_start), 'second_end': str_to_sec(date_time_end)}
		
		points = relations_to_geometry_id(group_id, 25, 35, 0, [50209], time_interval)
		geometries = relations_to_geometry_id(group_id, 30, 35, 0, [50146], time_interval)
		fc_points = feature_collection_by_geometry(group_id, 25, points, [50163], {})
		fc_polygons = feature_collection_by_geometry(group_id, 30, geometries, [30303], {})
		if region:
		    start_region_feature = region['features'][0]
		    start_region_feature['properties']['color'] = 'rgba(0, 0, 255, 0.3)'
		    features = []
		    polygon = Polygon(region['features'][0]['geometry']['coordinates'][0])
		    for feature in fc_points['features']:
		        if polygon.contains(Point(feature['geometry']['coordinates'])):
		            feature['properties']['class'] = 'icon-svg-point_detention_inside'
		            features.append(feature)
		    for feature in fc_polygons['features']:
		        if polygon.intersects(Polygon(feature['geometry']['geometries'][0]['coordinates'][0])):
		            features.append(feature)
		    fc_polygons['features'] = features
		    fc_polygons['features'] += [start_region_feature]
		    return fc_polygons
		else:
		    for feature in fc_points['features']:
		        feature['properties']['class'] = 'icon-svg-point_detention_inside'
		    fc_polygons['features'] += fc_points['features']
		    return fc_polygons
	except Exception as e:
		raise e