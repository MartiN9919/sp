from typing import List, Dict

from converter.base.base_object import BaseTable, BaseRelation


class BaseParser:
    databases: List[BaseTable]
    relations: Dict[str, BaseRelation]
    document_path: str

    def __init__(self):
        self.databases = []
        self.relations = {}

    @property
    def documents_path(self) -> str:
        """
        Метод получения пути к файлам
        @return: строка содержащая путь к папке с файлами
        """
        return self.document_path

