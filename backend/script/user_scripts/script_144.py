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
from data_base_driver.additional_functions import str_to_sec, get_second_range, get_date_time_from_sec, get_document_date_format
from document_driver.word_driver import get_document_from_template, get_dossier_for_object
from shapely.geometry import Polygon, Point, LineString, MultiPoint
from docx import Document
from docx.shared import RGBColor
from synonyms_manager.get_synonyms import get_synonyms
from document_driver.classifier_driver import get_exel_document
from core.projectSettings.constant import MEDIA_ROOT, DOCUMENT_ROOT



def script_144(request, group_id, file_id, user_id, title, lock):
	try:
		lock.acquire()
		lock.release()
		path = '/reports/' + title
		opg = request.get('opg',{}).get('value',[])
		def get_person_info(group_id, object_id, rec_id, relation_mode, old_rec_id=0):
		    info = {'params': {}, 'relations': []}
		    person = get_object_record_by_id_http(object_id, rec_id, group_id)
		    values = {}
		    for val in person['params']:
		        values[val['id']] = val['values'][0]['value']
		    info['params']['fio'] = values.get(35001, '')
		    info['params']['birthday'] = values.get(35002, '')
		    info['params']['citizenship'] = values.get(35004, '')
		    info['params']['nationality'] = values.get(35005, '')
		    info['params']['family_status'] = values.get(35014, '')
		    info['params']['own_number'] = values.get(50052, '')
		    info['params']['education'] = values.get(35015, '')
		    point_of_live = get_related_objects(group_id, object_id, rec_id, [50127], [], {}, 25)
		    if len(point_of_live) > 0:
		        point_name = get_record_title(point_of_live[0]['object_id'], point_of_live[0]['rec_id'], group_id,
		                                        length=8)
		        info['params']['place_of_live'] = point_name['title']
		    if relation_mode:
		        related_persons = get_related_objects(group_id, object_id, rec_id, [], [], {}, 35)
		        for person in related_persons:
		            if person['rec_id'] == old_rec_id:
		                continue
		            temp_related = get_related_objects(group_id, person['object_id'], person['rec_id'], [], [], {}, 40)
		            temp_opg = [item for item in temp_related if item['key_id'] == 50217]
		            if len(temp_opg) > 0:
		                opg_name = get_object_param_by_key(group_id, temp_opg[0]['object_id'], temp_opg[0]['rec_id'],
		                                                    50083)
		                info['params']['crime'] = get_key_by_id(person['key_id'])[
		                                                'title'] + ' c ' + get_item_list_value(
		                    temp_opg[0]['val']) + ' ' + opg_name
		    else:
		        related_persons = get_related_objects(group_id, object_id, rec_id, [], [], {}, 35)
		        for person in related_persons:
		            temp = get_person_info(group_id, person['object_id'], person['rec_id'], True, rec_id)
		            temp['params']['relation_type'] = get_key_by_id(person['key_id'])[
		                                                    'title'] + ' ' + get_item_list_value(person['val'])
		            info['relations'].append(temp)
		    return info
		opg_name = [get_object_param_by_key(group_id, opg['objectId'], opg['recId'], 50083)]
		persons = get_related_objects(group_id, opg['objectId'], opg['recId'], [50217], [], {}, 35)
		informations = []
		for person in persons:
		    temp = get_person_info(group_id, person['object_id'], person['rec_id'], False)
		    temp['params']['status'] = get_item_list_value(person['val'])
		    informations.append(temp)
		opg_status, fio, birthday, citizenship, number, place_of_live, education, family_status, family_fio, family_birthday, family_citizenship, family_number, family_place, family_education, family_crime = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
		for info in informations:
		    opg_status.append(info['params']['status'])
		    fio.append(info['params']['fio'])
		    birthday.append(info['params']['birthday'])
		    citizenship.append(info['params']['citizenship'])
		    number.append(info['params']['own_number'])
		    education.append(info['params']['education'])
		    place_of_live.append(info['params'].get('place_of_live', ''))
		    if len(info['relations']) > 0:
		        family_status.append(info['relations'][0]['params']['relation_type'])
		        family_fio.append(info['relations'][0]['params']['fio'])
		        family_birthday.append(info['relations'][0]['params']['birthday'])
		        family_citizenship.append(info['relations'][0]['params']['citizenship'])
		        family_number.append(info['relations'][0]['params']['own_number'])
		        family_place.append(info['relations'][0]['params'].get('place_of_live', ''))
		        family_education.append(info['relations'][0]['params']['education'])
		        family_crime.append(info['relations'][0]['params'].get('crime', ''))
		        for other_family in info['relations'][1:]:
		            opg_status.append('')
		            fio.append('')
		            birthday.append('')
		            citizenship.append('')
		            number.append('')
		            education.append('')
		            place_of_live.append('')
		            family_status.append(other_family['params']['relation_type'])
		            family_fio.append(other_family['params']['fio'])
		            family_birthday.append(other_family['params']['birthday'])
		            family_citizenship.append(other_family['params']['citizenship'])
		            family_number.append(other_family['params']['own_number'])
		            family_place.append(other_family['params'].get('place_of_live', ''))
		            family_education.append(other_family['params']['education'])
		            family_crime.append(other_family['params'].get('crime', ''))
		    else:
		        family_status.append('')
		        family_fio.append('')
		        family_birthday.append('')
		        family_citizenship.append('')
		        family_number.append('')
		        family_place.append('')
		        family_education.append('')
		        family_crime.append('')
		result = {
		    'opg_name': opg_name,
		    'opg_status': opg_status,
		    'fio': fio,
		    'birthday': birthday,
		    'citizenship': citizenship,
		    'number': number,
		    'education': education,
		    'place_of_live': place_of_live,
		    'family_status': family_status,
		    'family_fio': family_fio,
		    'family_birthday': family_birthday,
		    'family_citizenship': family_citizenship,
		    'family_number': family_number,
		    'family_place': family_place,
		    'family_education': family_education,
		    'family_crime': family_crime
		}
		path = get_xlsx_document_from_template('template_opg.xlsx', title, result)
		set_file_path(file_id, path)
		set_file_status(file_id, 'done')
	except BaseException:
		set_file_status(file_id, 'error')
