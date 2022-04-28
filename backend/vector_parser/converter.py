from copy import copy
from typing import Dict, List, Tuple

from openpyxl import load_workbook

from data_bank import Database, Relation
from objects.record.add_record_vector import add_data_vector
from objects.relations.add_rel import add_rel
from parser_bank import ParserBank


class ConverterRelations:
    database_id_1: int
    database_id_2: int
    object_id_1: int
    object_id_2: int
    relations_convert_table: Dict

    def __init__(self, database_id_1: int, database_id_2: int, objects_convert_table: dict,
                 relations_convert_table: dict):
        self.database_id_1 = database_id_1
        self.database_id_2 = database_id_2
        self.object_id_1 = objects_convert_table[database_id_1]
        self.object_id_2 = objects_convert_table[database_id_2]
        self.relations_convert_table = relations_convert_table

    def convert(self, relation: Relation, objects: Dict) -> dict:
        old_id_1 = relation.rec_id_1
        old_id_2 = relation.rec_id_2
        new_id_1 = objects[f"{self.database_id_1}_{old_id_1}"]['rec_id']
        new_id_2 = objects[f"{self.database_id_2}_{old_id_2}"]['rec_id']
        key_id = self.relations_convert_table.get(f"{self.database_id_1}_{self.database_id_1}", 0)
        date_time = relation.date + ' ' + relation.time
        # тут должна быть логика созлания связи с САПФИР

        add_rel(1, self.object_id_1, new_id_1, self.object_id_2, new_id_2, [{'id': key_id, 'val': '', 'date': date_time}])

        result: Dict = {
            'object_id_1': self.object_id_1,
            'rec_id_1': new_id_1,
            'object_id_2': self.object_id_2,
            'rec_id_2': new_id_2,
            'key_id': key_id,
            'date': date_time
        }
        return result

    @property
    def id(self):
        return f"{self.database_id_1}_{self.database_id_2}"


class ConverterParams:
    database_id: int
    object_id: int
    params_converter_table: Dict[int, Tuple[
        int, int]]  # таблица соответствия старого id и нового id  созможным порядком следования (например ФИО)

    def __init__(self, database_id: int, object_id: int, params_convert_dict: dict):
        self.database_id = database_id
        self.object_id = object_id
        self.params_converter_table = params_convert_dict

    def convert(self, database: Database, path: str) -> Dict:
        result: Dict[str, Dict] = {}
        for database_object_id in database.data:
            key = f"{self.database_id}_{database_object_id}"
            new_object = {key: {'rec_id': 0, 'object_id': self.object_id, 'params': []}}
            database_object_params = database.data[database_object_id]['values']
            database_object_datetime = database.data[database_object_id]['date'] + ' ' + \
                                       database.data[database_object_id]['time']
            temp_params = {}
            for param in database_object_params:
                new_param_info = self.params_converter_table.get(param['type'].id, (0, 0))
                if new_param_info[0] == 0 and param['type'].param_type == 'Ф':
                    new_param_info = (1, 0)
                elif new_param_info[0] == 0:
                    param['value'] = param['type'].name + ': ' + param['value']
                if new_param_info[1]:
                    if not temp_params.get(new_param_info[0]):
                        temp_params[new_param_info[0]] = [(param['value'], new_param_info[1])]
                    else:
                        temp_params[new_param_info[0]].append((param['value'], new_param_info[1]))
                else:
                    new_object[key]['params'].append(
                        {'id': new_param_info[0], 'value': param['value'], 'date': database_object_datetime})
            for temp_param in temp_params:
                value = ' '.join([item[0] for item in sorted(temp_params[temp_param], key=lambda x: x[1])])
                new_object[key]['params'].append(
                    {'id': temp_param, 'value': value, 'date': database_object_datetime})
            temp_result = add_data_vector(1, new_object[key], path)
            if temp_result.get('object'):
                new_object[key]['rec_id'] = temp_result['object']
            else:
                print('some error')
            result.update(new_object)
        return result


class ConverterBank:
    bank_parser: ParserBank
    converter_objects_table: Dict[int, int] = {}  # словарь соответствия объектов
    converter_relations_table: Dict[str, int] = {}  # словарь соответствия связей ('о1_о2') -> (key_id)
    converters_params: Dict[int, ConverterParams] = {}  # словарь соответсия параметров объекта (o.id) -> ConverterParams
    converters_relations: Dict[str, ConverterRelations] = {}
    object_to_create: Dict = {}
    relation_to_create: List = []

    def __init__(self, path: str, bank_path: str, init_type: str = 'exel'):
        if init_type == 'exel':
            self._parse_exel(path)
        else:
            raise TypeError
        self.bank_parser = ParserBank(bank_path)

    def _parse_exel(self, path: str):
        work_book = load_workbook(path)
        objects = work_book['objects']
        params_convert_dict, row0, row1 = {}, 0, 0
        for row in objects.iter_rows():
            if isinstance(row[0].value, int):
                if len(params_convert_dict) > 0:
                    self.converters_params[row0] = ConverterParams(row0, row1, copy(params_convert_dict))
                    params_convert_dict = {}
                self.converter_objects_table[row[0].value] = row[1].value
                row0, row1 = row[0].value, row[1].value
            if isinstance(row[2].value, int):
                params_convert_dict[row[2].value] = (row[3].value, row[4].value)
        else:
            self.converters_params[row0] = ConverterParams(row0, row1, copy(params_convert_dict))

    def convert(self):
        for database in self.bank_parser.databases:
            converter_params = self.converters_params[database.id]
            self.object_to_create.update(converter_params.convert(database, self.bank_parser.get_documents_path()))

        for relation in self.bank_parser.relations.values():
            converter_relation = self.converters_relations.get(f"{relation.object_id_1}_{relation.object_id_2}")
            if not converter_relation:
                converter_relation = ConverterRelations(relation.object_id_1, relation.object_id_2,
                                                        self.converter_objects_table, self.converter_relations_table)
                self.converters_relations[f"{relation.object_id_1}_{relation.object_id_2}"] = converter_relation
            self.relation_to_create.append(converter_relation.convert(relation, self.object_to_create))


converter = ConverterBank('/home/pushkin/convert_table.xlsx', '/home/pushkin/testDB 05.04.2022')
converter.convert()

