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
from core.deploy_settings import MEDIA_ROOT, DOCUMENT_ROOT



def script_90(request, group_id):
	try:
		zastava = request.get('zastava',{}).get('value',[])
		rel_with_naryds = io_get_rel(group_id, [50164], [int(zastava['objectId']), int(zastava['recId'])], [40], [], {}, True)
		naryads_rec_ids = []
		for temp_rel in rel_with_naryds:
		    if int(temp_rel['rec_id_1']) == int(zastava['recId']):
		        naryads_rec_ids.append(int(temp_rel['rec_id_2']))
		    if int(temp_rel['rec_id_2']) == int(zastava['recId']):
		        naryads_rec_ids.append(int(temp_rel['rec_id_1']))
		point_rels = []
		for nar in naryads_rec_ids:
		    point_rel = io_get_rel(group_id, [50165], [40, nar], [25], [], {}, True)
		    point_rels += point_rel
		point_rels = [item for item in point_rels if int(item['rec_id_1']) > 14]
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