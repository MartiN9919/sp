import copy
import datetime
from pathlib import Path
from typing import List, Dict, Tuple

from data_bank import Bank, Param, Database, Dictionary, Relation


class ParserBank:
    base_path: Path
    _bank_path: Path # путь к файлу структуры БД
    _dictionary_path: Path # путь к файлу структуры словарей
    _bank_folder_path: Path # путь к папке хранящей объекты
    _dictionary_folder_path: Path # путь к папке хранящей данные
    _encoding: str = 'windows-1251' #кодировка файлов, хронос по стандарту вывгружает в windows-1251
    databases: List[Database] = [] # список баз данных (таблиц)
    dictionaries: List[Dictionary] = [] # список словарей (списков)
    relations: Dict[str, Relation] = {} # словарб связей в формате {id: Relation}
    # константы
    LIST_BASE_SEPARATOR = 'Список баз:'
    BASE_PARAMS_SEPARATOR = 'База  :'
    DATABASE_FOLDER = 'БД'
    DICTIONARIES_FOLDER = 'СБД'
    DOCUMENTS_PATH = 'файлы'
    SEPARATOR = '|'

    def __init__(self, path: str):
        """
        Метод инициализации
        @param path: путь к папке с банком данных
        """
        self.base_path = Path(path)
        files = {x.name: x for x in self.base_path.iterdir()}
        if all(map(lambda item: item in files, ['Стурктура БД опогк.txt', 'Структура СБД опогк.txt', 'БД', 'СБД'])):
            self._bank_path = files['Стурктура БД опогк.txt']
            self._bank_folder_path = files['БД']
            self._dictionary_path = files['Структура СБД опогк.txt']
            self._dictionary_folder_path = files['СБД']
            self._parse_database()
            self._parse_dictionaries()
        else:
            raise Exception
        self.parse_dictionaries_data() # запуск парсера словарей
        self.parse_database_data() # запуск парсера данных

    @property
    def documents_path(self) -> str:
        """
        Метод получения пути к файлам
        @return: строка содержащая путь к папке с файлами
        """
        return f"{self.base_path}/{self.DOCUMENTS_PATH}"

    @staticmethod
    def _parse_bank_list(lines: List[str], databases: List[Bank], datatype=Bank):
        """
        Метод для парсинга списка баз данных (таблиц)
        @param lines: список строк структурного файла
        @param databases: список накопитель баз данных (таблиц)
        @param datatype: тип базы (таблицы): словарь или обычная таблица
        """
        for line in lines:
            params = line.split(ParserBank.SEPARATOR)
            if params[0].isdigit():
                databases.append(datatype(id=int(params[0]), name=params[1], short_name=params[2]))

    def get_database_by_short_name(self, short_name: str) -> Database:
        """
        Метод для получения базы данных (таблицы) по ее краткому имени
        @param short_name: краткое имя в формате строки
        @return: найденная база данных (таблица)
        """
        for database in self.databases:
            if database.short_name == short_name:
                return database

    def get_database_by_id(self, bank_id: int) -> Database:
        """
        Метод для получения базы данных (таблицы) по ее идентификатору
        @param bank_id: идентификатор базы данных (таблицы)
        @return: найденная база данных (таблица)
        """
        for database in self.databases:
            if database.id == bank_id:
                return database

    def get_dictionary_by_name(self, name: str) -> Dictionary:
        """
        Метод для получения словаря (списка) по его имени
        @param name: имя в формате строки
        @return: найденный словарь (список)
        """
        for dictionary in self.dictionaries:
            if dictionary.name == name:
                return dictionary

    @staticmethod
    def _parse_params(lines: List[str]) -> List[Param]:
        """
        Метод для парсинга параметров базы данных (таблицы) из структурного файла
        @param lines: список строк хранящих параметры
        @return: список параметров
        """
        result = [] # пустой список для накопления результата
        for line in lines: # идем по строкам
            params = line.split(ParserBank.SEPARATOR) # получением список параметров, разбив строку по разделителю
            if params[0].isdigit(): # если первый параметр число начинаем обработку
                link_str = params[6].replace('\n', '') # убираем у последнего параметра \n
                result.append(Param(
                    id=int(params[0]),
                    name=params[1],
                    param_type=params[2],
                    length=int(params[3]) if len(params[3]) else None,
                    dictionary=params[4] if len(params[4]) else None,
                    status=params[5].split(';') if len(params[5]) else None,
                    link=link_str if len(link_str) else None)
                )
        return result

    def _parse_banks(self, path: Path, databases: List[Bank], datatype=Bank):
        """
        Метод для парсинга информации о банках из структурного файла
        @param path: путь к структурному файлу
        @param databases: список баз данных (таблиц)
        @param datatype: тип данных (обычная таблица или словарь)
        """
        with open(path, encoding=self._encoding) as file: # открываем файл
            lines = file.readlines() # считываем список строк
            list_base_start = next(i for i, v in enumerate(lines) if v.startswith(self.LIST_BASE_SEPARATOR)) # находим первую строку с информацией о базах (таблицах)
            list_base_stop = lines.index('\n', list_base_start) # находим последнюю строку (пустая пробельная строка)
            ParserBank._parse_bank_list(lines[list_base_start:list_base_stop], databases, datatype) # парсим список баз (таблиц) в databases
            for database in databases: # идем по базам (таблицам)
                param_base_start = next(i for i, v in enumerate(lines) # находим первую строку с параметрами базы (таблицы)
                                        if v == (self.BASE_PARAMS_SEPARATOR + database.name + '\n'))
                param_base_stop = lines.index('\n', param_base_start) # находим последнюю строку с параметрами базы (таблицы)
                database.params = ParserBank._parse_params(lines[param_base_start:param_base_stop]) # парсим параметры базы (таблицы)
                file_params = [item for item in database.params if item.param_type == 'Ф'] # проверяем является ли база (таблица) файловой (один из параметров имеет тип "Ф")
                if len(file_params):
                    database.file_param = file_params[0]

    def _parse_database(self):
        """
        Метод для вызова парсинга всех баз данных (таблиц)
        """
        self._parse_banks(self._bank_path, self.databases, Database)

    def _parse_dictionaries(self):
        """
        Метод для вызова парсинга всех словарей (списков)
        """
        self._parse_banks(self._dictionary_path, self.dictionaries, Dictionary)

    def parse_dictionaries_data(self):
        """
        Метод для считывания информации из всех словарей
        """
        for dictionary in self.dictionaries: # идем по списку словарей
            dict_path = f"{self._dictionary_folder_path}/{dictionary.id}.txt" # получаем путь к основному файлу словаря
            if 'МН' in dictionary.params[2].status: # если словарь имеет множественный тип хранения
                sub_file_id = dictionary.params[2].id # получаем идентификатор побочного файла
                dict_sub_path = f"{self._dictionary_folder_path}/{dictionary.id}_{sub_file_id}.txt" # получаем путь к побочному файлу
                with open(dict_path, encoding=self._encoding) as main_file, open(dict_sub_path,
                                                                                 encoding=self._encoding) as sub_file: # открываем основной и побочные файлы
                    for line, sub_line in zip(main_file, sub_file): # построчно считываем открытые файлы
                        params = line.split(ParserBank.SEPARATOR) # получаем параметры с основного файла
                        sub_params = sub_line.split(ParserBank.SEPARATOR) # получаем параметры с побочного файла
                        if params[0].isdigit(): # если первый параметр число (идентификатор) записываем
                            dictionary.data[params[1].replace('\n', '')] = sub_params[1].replace('\n', '')
            else: # если словарь имеет одиночный тип хранения
                with open(dict_path, encoding=self._encoding) as main_file:  # открываем основной файл
                    for line in main_file: # построчно считываем открытый файл
                        params = line.split(ParserBank.SEPARATOR) # получаем параметры с основного файла
                        if params[0].isdigit(): # если первый параметр число (идентификатор) записываем
                            dictionary.data[params[1].replace('\n', '')] = params[2].replace('\n', '')

    @staticmethod
    def _parse_data_params(params: List[str], database_params: List[Param]) -> dict:
        """
        Метод для получения соответствия порядка параметров с их типом
        @param params: параметры отдельного файла
        @param bank_params: параметры базы данных
        @return: словарь соответствия порядка параметра с их типом
        """
        result = {}
        for i, param in enumerate(params):
            bank_param = next(item for item in database_params if item.name == param)
            result[i] = bank_param
        return result

    @staticmethod
    def _parse_sub_data_params(sub_data: int, bank_params: List[Param]) -> dict:
        bank_param = next(item for item in bank_params if item.id == sub_data)
        return {
            0: 'object_id',
            1: bank_param
        }

    def _parse_database_data(self, params: List[str], params_type: dict, bank_id: int, bank_data: dict):
        object_id = int(params[0])
        if not bank_data.get(object_id, None):
            bank_data[object_id] = {'date': datetime.datetime.now().strftime("%d.%m.%Y"),
                                    'time': datetime.datetime.now().strftime("%H:%M"),
                                    'values': []}
        for i, param in enumerate(params[1:]):
            param_type = params_type[i + 1]
            if len(param) == 0:
                continue
            if param_type.link:
                other_object_id = int(param)
                other_bank = self.get_database_by_short_name(param_type.link[:2])
                other_bank_id = other_bank.id
                relation = Relation(bank_id, object_id, other_bank_id, other_object_id)
                if not self.relations.get(relation.id):
                    self.relations[relation.id] = relation
            else:
                if param_type.dictionary:
                    dictionary = self.get_dictionary_by_name(param_type.dictionary)
                    param = dictionary.data.get(param)
                    if not param:
                        continue
                if param_type.status and 'НК' in param_type.status:
                    if param_type.id == 603:
                        bank_data[object_id]['date'] = param
                        continue
                    elif param_type.id == 604:
                        bank_data[object_id]['time'] = param
                        continue
                    else:
                        continue
                bank_data[object_id]['values'].append({'value': param, 'type': param_type})

    def _parse_database_file(self, file, bank_id: int, params_type: dict, bank_data: dict):
        temp_params = []
        for line in file:
            if len(line.replace('\n', '')) == 0:
                continue
            temp = [param.replace('\n', '') for param in line.split(ParserBank.SEPARATOR)]
            if len(temp_params) == len(params_type) and temp[0].isdigit():
                params = copy.deepcopy(temp_params)
                self._parse_database_data(params, params_type, bank_id, bank_data)
                temp_params = temp
                continue
            elif len(temp_params) == len(params_type):
                temp_params[-1] += temp[0]
            elif len(temp_params) > 0 and len(temp) == 1:
                temp_params[-1] += temp[0]
            elif len(temp_params) == 0:
                temp_params += temp
            elif len(temp_params) < len(params_type):
                temp_params[-1] += temp[0]
                temp_params += temp[1:]
        else:
            if len(temp_params) > 0:
                params = copy.deepcopy(temp_params)
                self._parse_database_data(params, params_type, bank_id, bank_data)

    @staticmethod
    def _get_older_datetime(date_1: str, time_1: str, date_2: str, time_2: str) -> Tuple[str, str]:
        temp_date_1 = '.'.join(reversed(date_1.split('.')))
        temp_date_2 = '.'.join(reversed(date_2.split('.')))
        if temp_date_1 > temp_date_2 or (temp_date_1 == temp_date_2 and time_1 > time_2):
            return date_1, time_1
        else:
            return date_2, time_2

    def parse_database_data(self):
        for database in self.databases:
            files = [x for x in self._bank_folder_path.iterdir() if x.name.split('_')[0].split('.')[0] == str(database.id)]
            for file_path in files:
                path_params = file_path.name.split('_')
                sub_data = int(path_params[1].split('.')[0]) if len(path_params) > 1 else 0
                with open(file_path, encoding=self._encoding) as file:
                    first_line_params = [param.replace('\n', '') for param in file.readline().split(ParserBank.SEPARATOR)]
                    if sub_data:
                        params_type = ParserBank._parse_sub_data_params(sub_data, database.params)
                    else:
                        params_type = ParserBank._parse_data_params(first_line_params, database.params)
                    self._parse_database_file(file, database.id, params_type, database.data)
            path = Path(self.documents_path)
            if database.file_param and path.is_dir():
                for item in database.data:
                    files = [x.name for x in path.iterdir() if x.name.split('.')[0] == str(item)]
                    for file in files:
                        database.data[item]['values'].append({'value': file, 'type': database.file_param})
        for relation in self.relations.values():
            database_object = self.get_database_by_id(relation.object_id_1).data[relation.rec_id_1]
            date_1 = database_object['date']
            time_1 = database_object['time']
            database_object = self.get_database_by_id(relation.object_id_2).data[relation.rec_id_2]
            date_2 = database_object['date']
            time_2 = database_object['time']
            relation.date, relation.time = self._get_older_datetime(date_1, time_1, date_2, time_2)








