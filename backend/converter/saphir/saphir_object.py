from converter.base.base_object import BaseParam, BaseTable, BaseRelation


class SaphirParam(BaseParam):

    def __init__(self, id: int, name: str, param_type: str):
        param_type = 'Ф' if param_type in ['file_any', 'file_photo'] else param_type
        super().__init__(id, name, param_type)


class SaphirObject(BaseTable):
    pass


class SaphirRelation(BaseRelation):
    key_id: int
    value: int
    document: int

    def __init__(self, object_id_1: int, rec_id_1: int, object_id_2: int, rec_id_2: int, key_id: int, value: int,
                 document: int, datetime: str):
        super().__init__(object_id_1, rec_id_1, object_id_2, rec_id_2)
        self.key_id = key_id
        self.value = value
        self.document = document
        self.date = datetime.split(' ')[0]
        self.time = datetime.split(' ')[1]
