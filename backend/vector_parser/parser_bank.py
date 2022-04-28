import copy
from pathlib import Path
from typing import List, Dict, Tuple

from data_bank import Bank, Param, Database, Dictionary, Relation


class ParserBank:
    base_path: Path
    _bank_path: Path
    _dictionary_path: Path
    _bank_folder_path: Path
    _dictionary_folder_path: Path
    _encoding: str = 'UTF-8' #windows-1251
    databases: List[Database] = []
    dictionaries: List[Dictionary] = []
    relations: Dict[str, Relation] = {}

    LIST_BASE_SEPARATOR = 'Список баз:'
    BASE_PARAMS_SEPARATOR = 'База  :'
    DATABASE_FOLDER = 'DB'
    DICTIONARIES_FOLDER = 'LDB'
    DOCUMENTS_PATH = 'documents'

    def __init__(self, path: str):
        self.base_path = Path(path)
        files = {x.name: x for x in self.base_path.iterdir()}
        if all(map(lambda item: item in files, ['DB struct.txt', 'LDB struct.txt', 'DB', 'LDB'])):
            self._bank_path = files['DB struct.txt']
            self._bank_folder_path = files['DB']
            self._dictionary_path = files['LDB struct.txt']
            self._dictionary_folder_path = files['LDB']
            self._parse_database()
            self._parse_dictionaries()
        else:
            raise Exception
        self.parse_dictionaries_data()
        self.parse_database_data()

    def get_documents_path(self) -> str:
        return f"{self.base_path}/{self.DOCUMENTS_PATH}"

    @staticmethod
    def _parse_bank_list(lines: List[str], databases: List[Bank], datatype=Bank):
        for line in lines:
            params = line.split('|')
            if params[0].isdigit():
                databases.append(datatype(id=int(params[0]), name=params[1], short_name=params[2]))

    def get_database_by_short_name(self, short_name: str) -> Database:
        for database in self.databases:
            if database.short_name == short_name:
                return database

    def get_database_by_id(self, bank_id: int) -> Database:
        for database in self.databases:
            if database.id == bank_id:
                return database

    def get_dictionary_by_name(self, name: str) -> Dictionary:
        for dictionary in self.dictionaries:
            if dictionary.name == name:
                return dictionary

    @staticmethod
    def _parse_params(lines: List[str]) -> List[Param]:
        result = []
        for line in lines:
            params = line.split('|')
            if params[0].isdigit():
                link_str = params[6].replace('\n', '')
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
        with open(path, encoding=self._encoding) as file:
            lines = file.readlines()
            list_base_start = next(i for i, v in enumerate(lines) if v.startswith(self.LIST_BASE_SEPARATOR))
            list_base_stop = lines.index('\n', list_base_start)
            ParserBank._parse_bank_list(lines[list_base_start:list_base_stop], databases, datatype)
            for database in databases:
                param_base_start = next(i for i, v in enumerate(lines)
                                        if v == (self.BASE_PARAMS_SEPARATOR + database.name + '\n'))
                param_base_stop = lines.index('\n', param_base_start)
                database.params = ParserBank._parse_params(lines[param_base_start:param_base_stop])
                file_params = [item for item in database.params if item.param_type == 'Ф']
                if len(file_params):
                    database.file_param = file_params[0]

    def _parse_database(self):
        self._parse_banks(self._bank_path, self.databases, Database)

    def _parse_dictionaries(self):
        self._parse_banks(self._dictionary_path, self.dictionaries, Dictionary)

    def parse_dictionaries_data(self):
        for dictionary in self.dictionaries:
            dict_path = f"{self._dictionary_folder_path}/{dictionary.id}.txt"
            if 'МН' in dictionary.params[2].status:
                sub_file_id = dictionary.params[2].id
                dict_sub_path = f"{self._dictionary_folder_path}/{dictionary.id}_{sub_file_id}.txt"
                with open(dict_path, encoding=self._encoding) as main_file, open(dict_sub_path,
                                                                                 encoding=self._encoding) as sub_file:
                    for line, sub_line in zip(main_file, sub_file):
                        params = line.split('|')
                        sub_params = sub_line.split('|')
                        if params[0].isdigit():
                            dictionary.data[params[1].replace('\n', '')] = sub_params[1].replace('\n', '')
            else:
                with open(dict_path, encoding=self._encoding) as main_file:
                    for line in main_file:
                        params = line.split('|')
                        if params[0].isdigit():
                            dictionary.data[params[1].replace('\n', '')] = params[2].replace('\n', '')

    @staticmethod
    def _parse_data_params(params: List[str], bank_params: List[Param]) -> dict:
        result = {}
        for i, param in enumerate(params):
            bank_param = next(item for item in bank_params if item.name == param)
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
            bank_data[object_id] = {'date': None, 'time': None, 'values': []}
        for i, param in enumerate(params[1:]):
            if len(param) == 0:
                continue
            param_type = params_type[i + 1]
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
                    if param_type.id == 600:
                        bank_data[object_id]['date'] = param
                        continue
                    elif param_type.id == 601:
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
            temp = [param.replace('\n', '') for param in line.split('|')]
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
    def _get_older_datetime(date_1: str, time_1: str, date_2:str, time_2: str) -> Tuple[str, str]:
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
                    first_line_params = [param.replace('\n', '') for param in file.readline().split('|')]
                    if sub_data:
                        params_type = ParserBank._parse_sub_data_params(sub_data, database.params)
                    else:
                        params_type = ParserBank._parse_data_params(first_line_params, database.params)
                    self._parse_database_file(file, database.id, params_type, database.data)
            if database.file_param:
                for item in database.data:
                    path = Path(self.get_documents_path())
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








