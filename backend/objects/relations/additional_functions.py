import datetime
from typing import List

from data_base_driver.additional_functions import date_time_to_sec


def get_seconds_from_request_data_time(date_time_start, date_time_end):
    """
    Функция для преобразования строк содержащих дату время в кортеж содержащий интервал в секундах
    @param date_time_start: строка содержащая дату/время начала интервала
    @param date_time_end: строка содержащая дату/время конца интервала
    @return: кортеж содержащий 2 значения интервала в секундах
    """
    if not date_time_start:
        date_time_1_str = '0001-01-01 00:00:00'
    else:
        date_time_1_str = date_time_start + ':00'
    if not date_time_end:
        date_time_2_str = datetime.datetime.now().isoformat(sep=' ')[:19]
    else:
        date_time_2_str = date_time_end + ':00'
    date_time_1 = datetime.datetime.strptime(date_time_1_str, "%Y-%m-%d %H:%M:%S")
    seconds_1 = date_time_to_sec(date_time_1)
    date_time_2 = datetime.datetime.strptime(date_time_2_str, "%Y-%m-%d %H:%M:%S")
    seconds_2 = date_time_to_sec(date_time_2)
    return seconds_1, seconds_2


def get_unique_objects(object_tree: List[dict], path: List[dict] = None) -> dict:
    """
    Функция для фильтрации дерева объектов с занесением всех уникальных объектов в objects
    @param object_tree: дерево объектов построенное при поиске связей
    @param path: путь к объекту
    """
    objects = {}
    if path is None:
        path = []
    for item in object_tree:
        objects[f"{item['object_id']}_{item['rec_id']}"] = {'object_id': item['object_id'],
                                                            'rec_id': item['rec_id'], 'path': path}
        if len(item.get('relations', [])) != 0:
            objects.update(get_unique_objects(item['relations'],
                                              [*path, {'object_id': item['object_id'], 'rec_id': item['rec_id']}]))
    return objects


def check_in_list(elem: dict, keys: list, items: List[dict]) -> bool:
    """
    Функция для проверки наличия словаря в списке словарей по совпадению заданных ключей
    @param elem: проверяемый словарь
    @param keys: заданные ключи
    @param items: список словарей
    @return: True если есть в списке, False если нет
    """
    for item in items:
        for key in keys:
            if item.get(key, 0) != elem.get(key, 1):
                break
        else:
            return True
    return False

