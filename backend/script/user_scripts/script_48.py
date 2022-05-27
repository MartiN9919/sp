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



def script_48(request, group_id, file_id, user_id, title, lock):
	try:
		lock.acquire()
		lock.release()
		path = '/reports/' + title
		date_start = request.get('date_start',{}).get('value',[])
		date_end = request.get('date_end',{}).get('value',[])
		list_id = request.get('list_id',{}).get('value',[])
		date_time_start = date_start + ' 00:00:00'
		date_time_end = date_end + ' 00:00:00'
		time_interval = {'second_start': str_to_sec(date_time_start), 'second_end': str_to_sec(date_time_end)}
		relations = io_get_rel(group_id, [50122], [20], [45], [list_id], {}, True)
		docs = []
		for relation in relations:
		    docs.append(int(relation['rec_id_1']))
		persons = []
		for doc in docs:
		    rels = io_get_rel(group_id, [50144], [35], [20, doc], [], {}, True)
		    if len(rels) > 0:
		        for rel in rels:
		            persons.append(int(rel['rec_id_2']))
		persons = list(set(persons))
		cars = []
		for doc in docs:
		    rels = io_get_rel(group_id, [50152], [50], [20, doc], [], {}, True)
		    if len(rels) > 0:
		        for rel in rels:
		            cars.append(int(rel['rec_id_2']))
		for car in cars:
		    rels = io_get_rel(group_id, [], [35], [50, car], [], {}, True)
		    if len(rels) > 0:
		        for rel in rels:
		            persons.append(int(rel['rec_id_1']))
		persons = list(set(persons))
		person_temp = []
		for person in persons:
		    rels = io_get_rel(group_id, [50146], [35, person], [30], [], time_interval, True)
		    if len(rels) > 0:
		        for rel in rels:
		            person_temp.append(int(rel['rec_id_2']))
		person_info = []
		for person in person_temp:
		    person_info.append(get_object_record_by_id_http(35, person, group_id, []))
		result = {}
		for temp in person_info:
		    country = [val for val in temp['params'] if val['id'] == 35004]
		    if len(country) == 0:
		        if not result.get('Не известно'):
		            result['Не известно'] = 0
		        result['Не известно'] += 1
		    else:
		        temp_country = country[0]['values'][0]['value']
		        if not result.get(temp_country):
		            result[temp_country] = 0
		        result[temp_country] += 1
		result_country, result_nums = [], []
		for key in sorted(result.keys()):
		    result_country.append(key)
		    result_nums.append(str(result[key]))
		path = get_xlsx_document_from_template('template.xlsx', title, {'COUNTRY': result_country, 'NUMS': result_nums,
		                                                                'START': [date_server_to_client(date_start)],
		                                                                'END': [date_server_to_client(date_end)]})
		set_file_path(file_id, path)
		set_file_status(file_id, 'done')
	except BaseException:
		set_file_status(file_id, 'error')
