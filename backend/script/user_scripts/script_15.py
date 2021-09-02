from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec



def script_15(request, group_id):
	try:
		obj = request.get('obj',{}).get('value',[])
		keys_rel = request.get('keys_rel',{}).get('value',[])
		geometry = request.get('geometry',{}).get('value',[])
		checkbox = request.get('checkbox',{}).get('value',[])
		date = request.get('date',{}).get('value',[])
		datatime = request.get('datatime',{}).get('value',[])
		phone_number = request.get('phone_number',{}).get('value',[])
		list = request.get('list',{}).get('value',[])
		unknow = request.get('unknow',{}).get('value',[])
		keys_rel = [int(keys_rel)]
		
		
		return rel_to_geo_fc(obj,0,keys_rel=keys_rel,keys_obj=['parent_id'], where_dop=[])
	except BaseException:
		return 'error'