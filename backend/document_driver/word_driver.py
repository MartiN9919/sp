import re

from docx import Document
from docxtpl import DocxTemplate, InlineImage

from core.settings import DOCUMENT_ROOT, TEMPLATE_ROOT, MEDIA_ROOT
from data_base_driver.record.get_record import get_object_record_by_id_http
from data_base_driver.sys_key.get_key_dump import get_key_by_id


def get_document_from_template(template_name, title, data):
    """
    Функция для формирования документа microsoft word из шаблона
    @param template_name: название шаблона
    @param title: название документа
    @param data: словарь содержащий информаию для занесение в документ, формат:
    {Position:[data1,...,dataN],...,PositionN:p[]} , где Position позиция в шаблоне, data -  данные для занесения
    @return: путь к конечному документу
    """
    document = Document(TEMPLATE_ROOT + template_name)
    for paragraph in document.paragraphs:
        for word in paragraph.text.replace('\t', ' ').split(' '):
            if data.get(re.sub("{[^<]+}", "", word)):
                size = paragraph.runs[0].font.size
                font_name = paragraph.style.font.name
                try:
                    paragraph.text = paragraph.text.replace(word, str(data[word][0]) if word.find('{') == -1 else
                        str(data[re.sub("{[^<]+}", "", word)][int(word[word.find('{') + 1:word.find('}')]) - 1]))
                except IndexError as e:
                    raise Exception(1, 'Выход за пределы массива')
                paragraph.style.font.name = font_name
                for run in paragraph.runs:
                    run.font.size = size
    document.save(DOCUMENT_ROOT + title + '.docx')
    return DOCUMENT_ROOT + title + '.docx'


def get_dossier_for_object(group_id, object_id, rec_id, title):
    """
    Функция для формирования досье о любом объекте базы данных
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param title: название конечного досье
    @return: путь к конечному файлу
    """
    template = DocxTemplate(TEMPLATE_ROOT + 'template_tables.docx')
    object_records = get_object_record_by_id_http(object_id, rec_id, group_id)
    table_content = []
    for param in object_records['params']:
        if get_key_by_id(param['id'])['type'] == 'file_photo':
            value = InlineImage(template, MEDIA_ROOT + '/files/' + str(object_id) + '/' + str(rec_id) + '/' + param['values'][0]['value'])
        elif get_key_by_id(param['id'])['type'] == 'file_any':
            continue
        else:
            value = param['values'][0]['value']
        table_content.append({'id': param['id'], 'key': get_key_by_id(param['id'])['title'], 'value': value})
    table_content.sort(key=lambda x: get_key_by_id(x['id'])['type'] != 'file_photo')
    content = {
        'title': 'Досье на ' + object_records['title'],
        'table_contents': table_content
    }
    template.render(content)
    template.save(DOCUMENT_ROOT + title + '.docx')
    return DOCUMENT_ROOT + title + '.docx'

# data = {'POSITION': ['Начальнику отдела'],
#         'RANK': ['Подполковнику'],
#         'NAME': ['Иванову И.И.'],
#         'START': ["01.01.2020"],
#         'END': ["01.02.2020"],
#         'N': ["1200"],
#         'n': ["13"],
#         'OWNER_POSITION': ["Старший офицер"],
#         'OWNER_RANK': ["Майор"],
#         'OWNER_NAME': ["Петров П.П."],
#         'DATE': ["01.02.2020"]
#         }


# document = Document(TEMPLATE_ROOT + 'template_person_test.docx')
# for paragraph in document.paragraphs:
#     for run in paragraph.runs:
#         print(run.text)

# get_document_from_template('template.docx', 'отчет.docx', data)

# position;Должность руководителя;Должность руководителя;text
# rank;Звание руководителя;Звание руководителя;text
# name;ФИО руководителя;ФИО руководителя;text
# start;Начало отчета;Начало отчета;date
# end;Конец отчета;Конец  отчета;date
# num;Номер ТОПС;Номер ТОПС;number
# owner_position;Должность;Должность;text
# owner_rank;Звание;Звание;text
# owner_name;ФИО;ФИО;text
# owner_date;дата;дата;text
