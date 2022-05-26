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