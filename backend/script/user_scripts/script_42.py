from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec



def script_42(request, group_id):
	try:
		geometry = request.get('geometry',{}).get('value',[])
		datatime_start = request.get('datatime_start',{}).get('value',[])
		datatime_end = request.get('datatime_end',{}).get('value',[])
		time_interval = {'second_start': str_to_sec(datatime_start + ':00'),'second_end': str_to_sec(datatime_end + ':00')}
		ids = relations_to_geometry_id(group_id, 25, 45, 0, [50141], time_interval)
		polygons = feature_collection_to_manticore_polygon(geometry)
		temp_result = []
		for polygon in polygons['in_polygon']:
		    temp_result += get_points_inside_polygon(polygon, ids, group_id)
		fc_new = feature_collection_by_geometry(group_id, 25, temp_result, [], {})
		return fc_new
	except BaseException:
		return 'error'