import geojson

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
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, get_document_date_format
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString



def script_49(request, group_id, file_id, user_id, title, lock):
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
		person_info = []
		for person in persons:
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
		                                                                'START': [get_document_date_format(date_start)],
		                                                                'END': [get_document_date_format(date_end)]})
		set_file_path(file_id, path)
		set_file_status(file_id, 'done')
		add_notification(user_id, 'information', 'ваш отчет: ' + title + ' - сгенерирован', from_id=1, file_id=file_id)
	except BaseException:
		set_file_status(file_id, 'error')
		add_notification(user_id, 'error', 'ошибка генерации вашего отчета: ' + title, from_id=1, file_id=file_id)
