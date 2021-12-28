import json
import geojson
import geopandas

from data_base_driver.geometry.geometry_transformations import get_polygon_from_lines
from data_base_driver.relations.get_rel import get_related_objects
from data_base_driver.sys_key.get_key_dump import get_key_by_id
from data_base_driver.sys_key.get_list import get_item_list_value
from document_driver.exel_driver import get_xlsx_document_from_template
from data_base_driver.record.get_record import get_object_record_by_id_http
from data_base_driver.record.get_record import get_object_param_by_key
from data_base_driver.input_output.input_output import io_set, io_get_obj_mysql_tuple, io_get_rel_mysql_tuple, io_get_rel, io_get_obj
from data_base_driver.record.search import search
from data_base_driver.sys_key.get_object_info import obj_list, rel_rec_to_el, el_to_rec_id
from data_base_driver.input_output.io_geo import rel_to_geo_fc, geo_id_to_fc, relations_to_geometry_id, feature_collection_by_geometry, get_geometries
from data_base_driver.sys_notifications.set_notifications_info import add_notification
from datetime import datetime
from data_base_driver.sys_reports.set_file_info import set_file_status, set_file_path
from data_base_driver.geometry.geometry_analytics import feature_collection_to_manticore_polygon, get_points_inside_polygon, get_line_buffer_polygon, get_distance_between_point_math
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, get_document_date_format
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString, MultiPoint
from docx import Document
from docx.shared import RGBColor
from synonyms_manager.get_synonyms import get_synonyms
from core.deploy_settings import MEDIA_ROOT, DOCUMENT_ROOT



def script_143(request, group_id, file_id, user_id, title, lock):
	try:
		lock.acquire()
		lock.release()
		path = '/reports/' + title
		document = request.get('document',{}).get('value',[])
		word = request.get('word',{}).get('value',[])
		file_name = get_object_param_by_key(group_id, document['objectId'], document['recId'], 50183)
		file = Document(MEDIA_ROOT + '/files/' + str(document['objectId']) + '/' + str(document['recId']) + '/' + file_name)
		synonyms = get_synonyms(word) + [word]
		for paragraph in file.paragraphs:
			for run in paragraph.runs:
				for item in synonyms:
					if run.text.find(item) != -1:
						run.font.color.rgb = RGBColor(255, 0, 0)
		file.save(DOCUMENT_ROOT + title + '.docx')
		path = DOCUMENT_ROOT + title + '.docx'
		set_file_path(file_id, path)
		set_file_status(file_id, 'done')
	except BaseException:
		set_file_status(file_id, 'error')
