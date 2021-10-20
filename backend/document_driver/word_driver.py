import re

from docx import Document

from core.settings import DOCUMENT_ROOT, TEMPLATE_ROOT


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
