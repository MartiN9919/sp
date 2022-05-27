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
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, date_server_to_client
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString, MultiPoint
from docx import Document
from docx.shared import RGBColor
from synonyms_manager.get_synonyms import get_synonyms
from document_driver.classifier_driver import get_exel_document
from core.projectSettings.constant import MEDIA_ROOT, DOCUMENT_ROOT



def script_96(request, group_id, file_id, user_id, title, lock):
	try:
		lock.acquire()
		lock.release()
		path = '/reports/' + title
		pogz = request.get('pogz',{}).get('value',[])
		date_start = request.get('date_start',{}).get('value',[])
		date_end = request.get('date_end',{}).get('value',[])
		time_interval = get_second_range(date_start, date_end)
		drags = {}
		towns = get_related_objects(group_id, pogz['objectId'], pogz['recId'], [50186], [], {})
		for town in towns:
		    town_title = get_object_param_by_key(group_id, town['object_id'], town['rec_id'], 50091)
		    border_guard = get_related_objects(group_id, town['object_id'], town['rec_id'], [50146], [], time_interval)
		    police = get_related_objects(group_id, town['object_id'], town['rec_id'], [50197], [], time_interval)
		    for temp in border_guard + police:
		        temp_type = 'police' if temp['key_id'] == 50197 else 'border_guard'
		        temp_drags = get_related_objects(group_id, temp['object_id'], temp['rec_id'], [50198], [], {})
		        for temp in temp_drags:
		            type = get_object_param_by_key(group_id, temp['object_id'], temp['rec_id'], 50195)
		            mass = get_object_param_by_key(group_id, temp['object_id'], temp['rec_id'], 50189)
		            if not drags.get(type):
		                drags[type] = {'police': {}, 'border_guard': {}}
		            if not drags[type][temp_type].get(town_title):
		                drags[type][temp_type][town_title] = {'count': 0, 'mass': 0}
		            drags[type][temp_type][town_title]['count'] += 1
		            drags[type][temp_type][town_title]['mass'] += int(mass)
		types, city_police, counts_police, mass_police, city_ops, counts_ops, mass_ops = [], [], [], [], [], [], []
		for drag in drags.keys():
		    types.append(drag)
		    temp_police = 0
		    temp_ops = 0
		    for key_police in drags[drag]['police']:
		        city_police.append(key_police)
		        counts_police.append(drags[drag]['police'][key_police]['count'])
		        mass_police.append(drags[drag]['police'][key_police]['mass'])
		        temp_police += 1
		    for key_ops in drags[drag]['border_guard']:
		        city_ops.append(key_ops)
		        counts_ops.append(drags[drag]['border_guard'][key_ops]['count'])
		        mass_ops.append(drags[drag]['border_guard'][key_ops]['mass'])
		        temp_ops += 1
		    if temp_ops > temp_police:
		        for i in range(temp_ops - temp_police):
		            city_police.append('-')
		            counts_police.append('-')
		            mass_police.append('-')
		    if temp_ops < temp_police:
		        for i in range(temp_police - temp_ops):
		            city_ops.append('-')
		            counts_ops.append('-')
		            mass_ops.append('-')
		    max = temp_ops if temp_ops > temp_police else temp_police
		    if max > 1:
		        for i in range(max-1):
		            types.append('')
		result = {'types': types, 'city_police': city_police, 'counts_police': counts_police, 'mass_police': mass_police,
		            'city_ops': city_ops, 'counts_ops': counts_ops, 'mass_ops': mass_ops}
		path = get_xlsx_document_from_template('template_drags.xlsx', title, result)
		set_file_path(file_id, path)
		set_file_status(file_id, 'done')
	except BaseException:
		set_file_status(file_id, 'error')
