import datetime
import json
import requests
from data_base_driver.constants.fulltextsearch import FullTextSearch

TEST_MODE = False


def on_test_mode_manticore():
    global TEST_MODE
    TEST_MODE = True


def off_test_mode_manticore():
    global TEST_MODE
    TEST_MODE = False


def add_record_http(index_title, id, date_time, key_id, val):
    """
    Функция для добавления записи в manticore
    @param index_title: название индекса (таблицы)
    @param id: идентификатор добавляемой записи
    @param date_time: строка содержащая дату и время добавления
    @param key_id: идентификатор ключа классификатора
    @param val: вносимое значение
    @return: True в случае успешного добавления, False в случае ошибки
    """
    if TEST_MODE:
        return False
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    days = date_time.date().toordinal() + 365
    seconds = date_time.time().second + date_time.time().minute * 60 + date_time.time().hour * 3600 + days*86400
    data = json.dumps({'index': index_title,
                       'id': 0,
                       'doc':
                           {
                               'rec_id': int(id),
                               'sec': seconds,
                               'key_id': str(key_id),
                               'val': str(val)
                           }
                       })
    response = requests.post(FullTextSearch.INSERT_URL, data=data)
    if response.status_code != 201:
        return False
    else:
        return True


def add_relation_http(date_time, key_id, obj_id_1, rec_id_1, obj_id_2, rec_id_2, val):
    """
    Функция для добавления связи
    @param date_time: строка содержащая дату и время добавления
    @param key_id: идентификатор ключа классификатора
    @param obj_id_1: идентификатор типа первого объекта
    @param rec_id_1: идентификатор записи первого объекта
    @param obj_id_2: идентификатор типа второго объекта
    @param rec_id_2: идентификатор записи второго объекта
    @param val: значение связи, если нет то пустая строка
    @return: True в случае успешного добавления, False в случае ошибки
    """
    if TEST_MODE:
        return False
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    days = date_time.date().toordinal()
    seconds = date_time.time().second + date_time.time().minute * 60 + date_time.time().hour * 3600 + days*86400
    data = json.dumps({
        "index": "rel",
        "doc":
        {
            "sec": str(seconds),
            "key_id": str(key_id),
            "obj_id_1": str(obj_id_1),
            "rec_id_1": str(rec_id_1),
            "obj_id_2": str(obj_id_2),
            "rec_id_2": str(rec_id_2),
            "val": str(val)
        }})
    response = requests.post(FullTextSearch.INSERT_URL, data=data)
    if response.status_code != 201:
        return False
    else:
        return True
