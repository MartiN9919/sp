from converter.base.base_parser import BaseParser
from converter.saphir.saphir_object import SaphirObject, SaphirParam, SaphirRelation
from data_base_driver.connect.connect_mysql import db_sql


class SaphirParser(BaseParser):
    database_setting: dict
    file_path: str
    keys: dict

    def __init__(self, parser_setting: dict):
        super().__init__()
        self.file_path = parser_setting['file_path']
        self.database_setting = parser_setting['database']
        self._parse_objects()
        self._parse_data()
        self._parse_relations()


    @property
    def documents_path(self) -> str:
        """
        Метод получения пути к файлам
        @return: строка содержащая путь к папке с файлами
        """
        return self.file_path

    def _parse_objects(self):
        sql = 'SELECT id, name FROM sys_obj WHERE id != 1'
        result = db_sql(sql, database=self.database_setting)
        for item in result:
            self.databases.append(SaphirObject(item[0], item[1]))
        sql = 'SELECT id, type, title FROM sys_key;'
        result = db_sql(sql, database=self.database_setting)
        self.keys = {item[0]: {'name': item[2], 'type': item[1]} for item in result}

    def _parse_data(self):
        for table in self.databases:
            sql = f"SELECT rec_id, key_id, val, dat FROM obj_{table.name}_row;"
            result = db_sql(sql, database=self.database_setting)
            for item in result:
                if table.data.get(item[0]) is None:
                    table.data[item[0]] = {'values': []}
                key = self.keys.get(item[1], {'name': 'Примечание', 'type': 'text'})
                param = SaphirParam(item[0], key['name'], key['type'])
                table.data[item[0]]['values'].append({'value': item[2], 'datetime': item[3].strftime("%d-%m-%Y %H:%M"), 'type': param})

    def _parse_relations(self):
        sql = 'SELECT key_id, obj_id_1, rec_id_1, obj_id_2, rec_id_2, val, document_id, dat FROM rel;'
        result = db_sql(sql, database=self.database_setting)
        for relation in result:
            key_id = int(relation[0])
            obj_id_1 = int(relation[1])
            rec_id_1 = int(relation[2])
            obj_id_2 = int(relation[3])
            rec_id_2 = int(relation[4])
            value = relation[5]
            document = relation[6]
            datetime = relation[7].strftime("%d-%m-%Y %H:%M")
            key = f"{obj_id_1}_{rec_id_1}_{obj_id_2}_{rec_id_1}"
            self.relations[key] = SaphirRelation(obj_id_1, rec_id_1, obj_id_2, rec_id_2, key_id, value, document, datetime)


setting = {
    'file_path': '',
    'database': {
        'HOST': '200.200.200.233',
        'PORT': '3306',
        'NAME': 'vec_3_data',
        'USER': 'dev',
        'PASSWORD': '1',
        'CHARSET': 'utf8',
    }
}

a = SaphirParser(setting)
b = 12