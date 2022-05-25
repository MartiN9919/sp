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


def get_unique_objects(object_tree: List[dict]) -> dict:
    """
    Функция для фильтрации дерева объектов с занесением всех уникальных объектов в objects
    @param object_tree: дерево объектов построенное при поиске связей
    """
    objects = {}
    for item in object_tree:
        objects[f"{item['object_id']}_{item['rec_id']}"] = {'object_id': item['object_id'], 'rec_id': item['rec_id']}
        if len(item.get('relations', [])) != 0:
            objects.update(get_unique_objects(item['relations']))
    return objects


def get_path_to_object(object_tree: List[dict], path: List[dict] = None) -> dict:
    """
    Функция для получения самых коротких путей от корня к ветке
    @param object_tree: дерево объектов
    @param path: путь к корню текущей итерации
    @return: словарь в формате {'object_id_rec_id': path}
    """
    objects = {}
    if path is None:
        path = []
    for item in object_tree:
        objects[f"{item['object_id']}_{item['rec_id']}"] = \
            [[*path, {'object_id': item['object_id'], 'rec_id': item['rec_id']}]]
        if len(item.get('relations', [])) != 0:
            temp_objects = get_path_to_object(
                item['relations'], [*path, {'object_id': item['object_id'], 'rec_id': item['rec_id']}])
            for temp_object in temp_objects:
                if not objects.get(temp_object):
                    objects[temp_object] = temp_objects[temp_object]
                else:
                    for elem in temp_objects[temp_object]:
                        if len(elem) < len(objects[temp_object][0]):
                            objects[temp_object] = [elem]
                        elif len(elem) == len(objects[temp_object][0]):
                            objects[temp_object].append(elem)
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
