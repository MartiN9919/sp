from typing import Literal, List, Optional, Dict

from converter.base.base_object import BaseParam, BaseTable, BaseRelation

types = Literal['Ц', 'УД', 'T', 'С', 'ПО', 'В', 'Ф']
statuses = Literal['ИФ', 'МН']


class Param(BaseParam):
    dictionary: Optional[str]
    length: Optional[int]
    status: Optional[List[statuses]]
    link: Optional[str]

    def __init__(self, id: int, name: str, param_type: types, dictionary: Optional[str], length: Optional[int],
                 status: Optional[List[statuses]], link: Optional[str]):
        super().__init__(id, name, param_type)
        self.dictionary = dictionary
        self.length = length
        self.status = status
        self.link = link


class Bank(BaseTable):
    short_name: str
    params: List[Param]

    def __init__(self, id: int, name: str, short_name: str):
        super().__init__(id, name)
        self.short_name = short_name
        self.params = []


class Dictionary(Bank):
    pass


class Database(Bank):
    file_param: Optional[Param]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_param = None


class Relation(BaseRelation):
    pass


