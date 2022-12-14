import datetime
import json

import requests

from data_base_driver.additional_functions import date_time_to_sec, push_dict
from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_OWNER
from data_base_driver.constants.const_fulltextsearch import FullTextSearch
from data_base_driver.constants.const_key import SYS_KEY_CONSTANT


def check_object_permission(group_id, object_type, rec_id, write=False):
    """
    Проверка доступа группы к объекту
    @param group_id: идентификатор группы пользователя запросившего объект
    @param object_type: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param write: флаг запись/чтение
    @return: True - доступ разрешен
    """
    if object_type not in DAT_SYS_KEY.DUMP.owners.keys():
        return True
    keys_validation_tuple = DAT_SYS_KEY.DUMP.owners[object_type]
    index = 'obj_' + FullTextSearch.TABLES[object_type] + '_row'
    data = json.dumps({
        'index': index,
        'query': {
            'bool': {
                'must': [{
                    'in': {
                        'key_id': [str(key) for key in keys_validation_tuple]
                    }
                }, {
                    'equals': {
                        'rec_id': rec_id
                    }
                }
                ]
            }
        }
    })
    response = requests.post(FullTextSearch.SEARCH_URL, data=data)
    permission_keys = [key['_source'] for key in json.loads(response.text)['hits']['hits']]
    permit_groups = {}
    for key in permission_keys:
        if int(key['key_id']) == keys_validation_tuple[4]:
            push_dict(permit_groups, int(key['key_id']), {'val': int(key['val']), 'sec': key['sec']})
        elif int(key['key_id']) == keys_validation_tuple[2]:
            if key['sec'] < date_time_to_sec(datetime.datetime.now()):
                push_dict(permit_groups, int(key['key_id']), (int(key['val'])))
        else:
            push_dict(permit_groups, int(key['key_id']), (int(key['val'])))
    if permit_groups.get(keys_validation_tuple[4]):
        permit_groups[keys_validation_tuple[4]].sort(key=lambda x: x['sec'], reverse=True)
        permit_groups[keys_validation_tuple[4]] = [item['val'] for item in permit_groups[keys_validation_tuple[4]]]
    return valid_group_object(group_id, permit_groups, keys_validation_tuple, write)


def valid_group_object(group_id, permit_group, keys_validation_tuple, write=False):
    """
    Функция для проверки доступа группы пользователя к данному объекту
    @param group_id: идентификатор группы доступа
    @param permit_group: словарь содержащий информацию о группах, для которых доступ к объекту разрешен, формат:
    {key_id_owner_add_rw:[id1,id2,...,id_n], ...}
    @param keys_validation_tuple: кортеж содержащий 4 идентификатора ключа по режимам доступа для данного типа объекта
    @param write: флаг запись/чтение
    @return: True если для группы пользователя доступ разрешен, в противном случае False
    """
    keys_validation_dict = {'owner_add_rw': keys_validation_tuple[0],
                            'owner_add_ro': keys_validation_tuple[1],
                            'owner_add_ro_limit': keys_validation_tuple[2],
                            'owner_del': keys_validation_tuple[3],
                            'owner_visible': keys_validation_tuple[4]}
    if group_id in permit_group.get(keys_validation_dict['owner_del'], []):
        return False
    if write:
        if not permit_group.get(keys_validation_dict['owner_add_rw'], None):
            return True
        return DAT_OWNER.DUMP.valid_group_rw(
            group_id=group_id,
            valids_id=permit_group.get(keys_validation_dict['owner_add_rw'], [])
        )
    else:
        if not permit_group.get(keys_validation_dict['owner_add_ro_limit'], None) and \
                not permit_group.get(keys_validation_dict['owner_add_ro'], None) and \
                not permit_group.get(keys_validation_dict['owner_add_rw'], None):
            return True
        read_groups = permit_group.get(keys_validation_dict['owner_add_ro'], []) + permit_group.get(
            keys_validation_dict['owner_add_ro_limit'], []) + permit_group.get(keys_validation_dict['owner_add_rw'], [])
        return DAT_OWNER.DUMP.valid_group_ro(
            group_id=group_id,
            valids_id=read_groups
        )


def get_enabled_records(object_type, records, group_id, write=False):
    """
    Функция для фильтрации записей на основе доступа по группе пользователя
    @param object_type: идентификатор типа объекта
    @param records: список словарей записей
    @param group_id: идентификатор группы пользователя
    @param write: флаг запись/чтение
    @return: отфильтрованный список словарей записей
    """
    if object_type not in DAT_SYS_KEY.DUMP.owners.keys() or group_id == 1:
        return records
    objects = set([record['rec_id'] for record in records])
    remove_objects = []
    for object in objects:
        if not check_object_permission(group_id, object_type, object, write):
            remove_objects.append(object)
    return [record for record in records if record['rec_id'] not in remove_objects]


def check_relation_permission(relation, group_id):
    """
    Функция для проверки доступа пользователя к связи
    @param relation: проверяемая связь в формате {_id, _source:{key_id, obj_id_1, ..., val}}
    @param group_id: идентификатор группы пользователя
    @return: True если доступ есть, в противном случае False
    """
    if int(relation['_source']['obj_id_1']) in DAT_SYS_KEY.DUMP.owners.keys():
        if not check_object_permission(group_id, relation['_source']['obj_id_1'], relation['_source']['rec_id_1'],
                                        False):
            return False
    if int(relation['_source']['obj_id_2']) in DAT_SYS_KEY.DUMP.owners.keys():
        if not check_object_permission(group_id, relation['_source']['obj_id_2'], relation['_source']['rec_id_2'],
                                       False):
            return False
    if len(relation['_source']['document_id']) > 0:
        if not check_object_permission(group_id, SYS_KEY_CONSTANT.DOC_ID,
                                       int(relation['_source']['document_id']), False):
            return False
    return True


