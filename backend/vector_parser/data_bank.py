from typing import Literal, List, Optional, Dict

types = Literal['Ц', 'УД', 'T', 'С', 'ПО', 'В', 'Ф']
statuses = Literal['ИФ', 'МН']


class Param:
    id: int
    name: str
    param_type: types
    dictionary: Optional[str]
    length: Optional[int]
    status: Optional[List[statuses]]
    link: Optional[str]

    def __init__(self, id: int, name: str, param_type: types, dictionary: Optional[str], length: Optional[int],
                 status: Optional[List[statuses]], link: Optional[str]):
        self.id = id
        self.name = name
        self.param_type = param_type
        self.dictionary = dictionary
        self.length = length
        self.status = status
        self.link = link


class Bank:
    id: int
    name: str
    short_name: str
    params: List[Param]

    def __init__(self, id: int, name: str, short_name: str):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.params = []


class Dictionary(Bank):
    data: dict

    def __init__(self, *args, **kwargs):
        self.data = {}
        super().__init__(*args, **kwargs)


class Database(Bank):
    data: Dict[int, dict]
    file_param: Param = None

    def __init__(self, *args, **kwargs):
        self.data = {}
        super().__init__(*args, **kwargs)


class Relation:
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
        return '_'.join([str(item) for item in self.__dict__.values() if isinstance(item, int)])


