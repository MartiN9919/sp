import geojson
import geopandas

from data_base_driver.sys_key.get_key_dump import get_key_by_id
from data_base_driver.sys_key.get_list import get_item_list_value
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
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon, get_line_buffer_polygon
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, get_document_date_format
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString, MultiPoint



def script_43(request, group_id, file_id, user_id, title, lock):
	try:
		lock.acquire()
		lock.release()
		path = '/reports/' + title
		position = request.get('position',{}).get('value',[])
		rank = request.get('rank',{}).get('value',[])
		name = request.get('name',{}).get('value',[])
		start = request.get('start',{}).get('value',[])
		end = request.get('end',{}).get('value',[])
		country = request.get('country',{}).get('value',[])
		country_title = request.get('country_title',{}).get('value',[])
		owner_position = request.get('owner_position',{}).get('value',[])
		owner_rank = request.get('owner_rank',{}).get('value',[])
		owner_name = request.get('owner_name',{}).get('value',[])
		owner_date = request.get('owner_date',{}).get('value',[])
		n = 10
		data = {
			'POSITION': [position],
			'RANK': [rank],
			'NAME': [name],
			'START': [get_document_date_format(start)],
			'END': [get_document_date_format(end)],
			'N': ['10'],
			'n': ['10'],
			'OWNER_POSITION': [owner_position],
			'OWNER_RANK': [owner_rank],
			'OWNER_NAME': [owner_name],
			'DATE': [get_document_date_format(owner_date)]
		}
		path=get_document_from_template('template.docx',title,data)
		set_file_path(file_id, path)
		set_file_status(file_id, 'done')
		add_notification(user_id, 'information', 'ваш отчет: ' + title + ' - сгенерирован', from_id=1, file_id=file_id)
	except BaseException:
		set_file_status(file_id, 'error')
		add_notification(user_id, 'error', 'ошибка генерации вашего отчета: ' + title, from_id=1, file_id=file_id)