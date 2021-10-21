import geojson

from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon
from data_base_driver.additional_functions import str_to_sec



def script_33(request, group_id):
	try:
		obj = request.get('obj',{}).get('value',[])
		rec_id = request.get('rec_id',{}).get('value',[])
		#ret = []
		#params = {}
		# 
		#geometry = {
		#    "type": "Point",
		#    "coordinates": [26.842182,54.313136],
		#}
		#feature = geojson.Feature(geometry=geometry, properties=params, keys=[])
		#feature['id'] = 1
		#feature['obj_id'] = 25
		#ret.append(feature)
		#
		#geometry = {
		#    "type": "Point",
		#    "coordinates": [26.842182,54.313136],
		#}
		#feature = geojson.Feature(geometry=geometry, properties=params)
		#feature['id'] = 1
		#feature['obj_id'] = 25
		#ret.append(feature)
		#return geojson.FeatureCollection(ret)
		
		ret =  geo_id_to_fc(obj='geometry', group_id=group_id, geo_ids=[rec_id,], keys=[])
		return ret
	except BaseException:
		return 'error'