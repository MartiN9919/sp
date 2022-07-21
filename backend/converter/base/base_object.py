class BaseParam:
    id: int
    name: str
    param_type: str

    def __init__(self, id: int, name: str, param_type: str):
        self.id = id
        self.name = name
        self.param_type = param_type


class BaseTable:
    id: int
    name: str
    data: dict

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.data = {}


class BaseRelation:
    object_id_1: int
    rec_id_1: int
    object_id_2: int
    rec_id_2: int
    date: str
    time: str

    def __init__(self, object_id_1: int, rec_id_1: int, object_id_2: int, rec_id_2: int):
        if object_id_2 < object_id_1 or (object_id_1 == object_id_2 and rec_id_2 < rec_id_1):
            object_id_1, object_id_2, rec_id_1, rec_id_2 = object_id_2, object_id_1, rec_id_2, rec_id_1
        self.object_id_1 = object_id_1
        self.rec_id_1 = rec_id_1
        self.object_id_2 = object_id_2
        self.rec_id_2 = rec_id_2

    @property
    def id(self) -> str:
        return f"{self.object_id_1}_{self.rec_id_1}_{self.object_id_2}_{self.rec_id_2}"
