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



def script_115(request, group_id):
	try:
		rels = io_get_rel(group_id, [50214], [25], [35], [], {}, True)
		persons = [{'rec_id': item['rec_id_2'], 'sec': item['sec']} for item in rels]
		points_id = []
		for person in persons:
		    points_id.append({'person_id': person['rec_id'],
		                        'point_id': relations_to_geometry_id(group_id, 25, 35, int(person['rec_id']), [50162],
		                                                            {})})
		fc_points = feature_collection_by_geometry(group_id, 25, [item['point_id'][0] for item in points_id], [], {})
		for feature in fc_points['features']:
		    person_id = [int(item['person_id']) for item in points_id if int(item['point_id'][0]) == feature['rec_id']][
		        0]
		    feature['properties']['hint'] = 'Место жительства ' + get_object_param_by_key(group_id, 35, person_id,
		                                                                                    35001)
		return fc_points
	except Exception as e:
		raise e