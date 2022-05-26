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



def script_95(request, group_id):
	try:
		pogz = request.get('pogz',{}).get('value',[])
		towns = get_related_objects(group_id, pogz['objectId'], pogz['recId'], [50186], [], {})
		result = {'good': [], 'bad': []}
		features = []
		for town in towns:
		    peoples = get_related_objects(group_id, town['object_id'], town['rec_id'], [50147], [], {})
		    nums = len(peoples) if peoples and len(peoples) > 0 else 0
		    if nums == 0:
		        continue
		    workers = 0
		    for people in peoples:
		        if len(get_related_objects(group_id, people['object_id'], people['rec_id'], [50180, 1304], [], {})) > 0:
		            workers += 1
		    result['good'].append(town['rec_id']) if workers / nums > 0.5 else result['bad'].append(town['rec_id'])
		    temp_fc = feature_collection_by_geometry(group_id, 30, [town['rec_id']], [], {})
		    feature = temp_fc['features'][0]
		    feature['properties']['hint'] = str((1 - (workers / nums))*100) + '%'
		    feature['properties']['value'] = (1 - (workers / nums))*100
		    features.append(feature)
		fc_new = feature_collection_by_geometry(group_id, 30, result['bad'], [30303], {})
		fc_new['features'] = features
		fc_new['style'] = {'coloring': "green_max"}
		return fc_new
	except Exception as e:
		raise e