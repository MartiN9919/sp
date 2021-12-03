from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec, get_document_date_format
from document_driver.word_driver import get_document_from_template



def script_80(request, group_id):
	try:
		search_test1 = request.get('search_test1',{}).get('value',[])
		search_test2 = request.get('search_test2',{}).get('value',[])
		search_test3 = request.get('search_test3',{}).get('value',[])
		search_test4 = request.get('search_test4',{}).get('value',[])
		search_test5 = request.get('search_test5',{}).get('value',[])
		search_test6 = request.get('search_test6',{}).get('value',[])
		search_test7 = request.get('search_test7',{}).get('value',[])
		search_test8 = request.get('search_test8',{}).get('value',[])
		search_test9 = request.get('search_test9',{}).get('value',[])
		search_test10 = request.get('search_test10',{}).get('value',[])
		search_test11 = request.get('search_test11',{}).get('value',[])
		
	except Exception as e:
		raise e