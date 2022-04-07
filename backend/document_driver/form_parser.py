import json

from docx_utils.flatten import opc_to_flat_opc
from os import remove
import uuid


def get_entities_from_file(path):
    """
    Функция для получения объектов и их связей из бланка
    @param path: путь к файлу бланка
    @return: словарь содержащий obj и rel
    """
    temp_name_xml = str(uuid.uuid1()) + ".xml"
    opc_to_flat_opc(path, temp_name_xml)
    with open(temp_name_xml) as file:
        text = file.readlines()
        text = '/n'.join(text)
        text = text[text.find('docVars'):]
        text = text[text.find('"{') + 1:]
        text = text[:text.find('}"/>') + 1]
        text = text.replace('&quot;', '"')
    remove(temp_name_xml)
    return json.loads(text)
