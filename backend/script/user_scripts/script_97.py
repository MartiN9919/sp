import geojson

from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple
from data_base_driver.record.search import search
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec
from document_driver.word_driver import get_document_from_template, get_dossier_for_object



def script_97(request, group_id, file_id, user_id, title, lock):
	try:
		lock.acquire()
		lock.release()
		path = '/reports/' + title
		object = request.get('object',{}).get('value',[])
		path = get_dossier_for_object(group_id, object['objectId'], object['recId'], title)
		set_file_path(file_id, path)
		set_file_status(file_id, 'done')
		add_notification(user_id, 'information', 'ваш отчет: ' + title + ' - сгенерирован', from_id=1, file_id=file_id)
	except BaseException:
		set_file_status(file_id, 'error')
		add_notification(user_id, 'error', 'ошибка генерации вашего отчета: ' + title, from_id=1, file_id=file_id)
