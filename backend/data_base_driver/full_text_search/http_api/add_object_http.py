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
    if TEST_MODE:
        return False
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    days = date_time.date().toordinal()
    seconds = date_time.time().second + date_time.time().minute * 60 + date_time.time().hour * 3600
    data = json.dumps({'index': index_title,
                       'id': int(id),
                       'doc':
                           {
                               'date': days,
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
    if TEST_MODE:
        return False
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    days = date_time.date().toordinal()
    seconds = date_time.time().second + date_time.time().minute * 60 + date_time.time().hour * 3600
    data = json.dumps({
        "index": "rel",
        "doc":
        {
            "date": str(days),
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
