import json
import geojson
import geopandas

from objects.geometry.geometry_transformations import get_polygon_from_lines
from objects.relations.get_rel import get_related_objects
from data_base_driver.sys_key.get_key_dump import get_key_by_id
from data_base_driver.sys_key.get_list import get_item_list_value
from document_driver.exel_driver import get_xlsx_document_from_template
from objects.record.get_record import get_object_record_by_id_http, get_record_title
from objects.record.get_record import get_object_param_by_key
from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple, io_get_rel, io_get_obj
from objects.record.search import search
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
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



def script_92(request, group_id):
	try:
		result = []
		fc_geometries = feature_collection_by_geometry(group_id, 30, [39, 40], [30303], {})
		for geometry in fc_geometries['features'][0]['geometry']['geometries']:
		    if geometry['type'] == 'LineString':
		        result += get_line_buffer_polygon(LineString(geometry['coordinates']))['features']
		for geometry in fc_geometries['features'][1]['geometry']['geometries']:
		    if geometry['type'] == 'LineString':
		        result += get_line_buffer_polygon(LineString(geometry['coordinates']))['features']
		fc_geometries['features'] = result
		polygon1 = Polygon(result[0]['geometry']['coordinates'][0])
		polygon2 = Polygon(result[1]['geometry']['coordinates'][0])
		if polygon1.overlaps(polygon2):
		    res = geopandas.GeoSeries([polygon1.intersection(polygon2)]).__geo_interface__
		    return res
		return fc_geometries
	except Exception as e:
		raise e