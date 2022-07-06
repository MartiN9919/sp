import datetime
import json
import requests
from data_base_driver.constants.const_fulltextsearch import FullTextSearch
from data_base_driver.sys_key.get_key_info import get_key_by_id


def add_row_record_http(index_title, rec_id, date_time, key_id, val):
    """
    Функция для добавления записи в manticore
    @param index_title: название индекса (таблицы)
    @param rec_id: идентификатор добавляемой записи
    @param date_time: строка содержащая дату и время добавления
    @param key_id: идентификатор ключа классификатора
    @param val: вносимое значение
    @return: True в случае успешного добавления, False в случае ошибки
    """
    if get_key_by_id(key_id)['type'] == 'checkbox':
        val = 1 if val == 'True' else 0
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    days = date_time.date().toordinal() + 365
    seconds = date_time.time().second + date_time.time().minute * 60 + date_time.time().hour * 3600 + days * 86400
    data = json.dumps({'index': index_title,
                       'id': 0,
                       'doc': {
                           'rec_id': int(rec_id),
                           'sec': seconds,
                           'key_id': str(key_id),
                           'val': str(val)
                       }})
    response = requests.post(FullTextSearch.INSERT_URL, data=data)
    if response.status_code != 201:
        return False
    else:
        return True


def add_col_record_http(index_title, rec_id, params):
    """
    Функция для добавления записи в col index мантикоры
    @param index_title: название таблицы
    @param rec_id: идентификатор записи
    @param params: параметры для записи
    @return: если добавление прошло успешно True, если нет False
    """
    doc = {}
    for param in params:
        param_list = param.split('=')
        key = param_list[0]
        if key == 'location' or key == 'point':
            value = param_list[1][20:-2]
        elif key == 'dat':
            key = 'sec'
            date_time = datetime.datetime.strptime(param_list[1][1:-1], "%Y-%m-%d %H:%M:%S")
            days = date_time.date().toordinal() + 365
            value = date_time.time().second + date_time.time().minute * 60 + date_time.time().hour * 3600 + days * 86400
        else:
            value = param_list[1].replace('\'', '')
        doc[key] = value
    doc['rec_id'] = rec_id
    data = json.dumps({'index': index_title,
                       'id': 0,
                       'doc': doc
                       })
    response = requests.post(FullTextSearch.INSERT_URL, data=data)
    if response.status_code != 201:
        return False
    else:
        return True


def update_col_record_http(index_title, rec_id, params):
    """
    Функция для изменения записи в col index мантикоры
    @param index_title: название таблицы
    @param rec_id: идентификатор записи
    @param params: параметры для записи
    @return: если добавление прошло успешно True, если нет False
    """
    doc = {}
    for param in params:
        param_list = param.split('=')
        key = param_list[0]
        if key == 'location' or key == 'point':
            value = param_list[1][20:-2]
        elif key == 'rec_id':
            value = int(param_list[1])
        else:
            value = param_list[1]
        doc[key] = value
    rec_id = int(rec_id)
    data = json.dumps({'index': index_title,
                       'doc': doc,
                       'equals': {'rec_id': rec_id}
                       })
    response = requests.post(FullTextSearch.UPDATE_URL, data=data)
    if response.status_code != 201 or response.status_code != 200:
        return False
    else:
        return True


def add_relation_http(rec_id, date_time, key_id, obj_id_1, rec_id_1, obj_id_2, rec_id_2, val, document_id):
    """
    Функция для добавления связи
    @param rec_id: идентификатор записи о связи
    @param date_time: строка содержащая дату и время добавления
    @param key_id: идентификатор ключа классификатора
    @param obj_id_1: идентификатор типа первого объекта
    @param rec_id_1: идентификатор записи первого объекта
    @param obj_id_2: идентификатор типа второго объекта
    @param rec_id_2: идентификатор записи второго объекта
    @param val: значение связи, если нет то пустая строка
    @param document_id: идентификатор документа основания связи
    @return: True в случае успешного добавления, False в случае ошибки
    """
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    days = date_time.date().toordinal() + 365
    seconds = date_time.time().second + date_time.time().minute * 60 + date_time.time().hour * 3600 + days * 86400
    data = json.dumps({
        "index": "rel",
        "id": rec_id,
        "doc":
            {
                "sec": str(seconds),
                "key_id": str(key_id),
                "obj_id_1": str(obj_id_1),
                "rec_id_1": str(rec_id_1),
                "obj_id_2": str(obj_id_2),
                "rec_id_2": str(rec_id_2),
                "val": str(val),
                "document_id": str(document_id)
            }})
    response = requests.post(FullTextSearch.INSERT_URL, data=data)
    if response.status_code not in [200, 201]:
        return False
    else:
        return True
