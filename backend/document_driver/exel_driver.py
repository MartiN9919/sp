import re

from openpyxl import load_workbook

from core.settings import DOCUMENT_ROOT, TEMPLATE_ROOT


def insert_list(works_sheet, mode, start_cell, data):
    """
    Функция для вставки списка в exel документ
    @param works_sheet: рабочее окно для вставки
    @param mode: режим вставки (ud, down, left, right)
    @param start_cell: стартовая ячейка
    @param data: список для вставки
    """
    col = start_cell.col_idx
    row = start_cell.row
    if mode == 'down' or mode == 'up':
        for index, value in enumerate(data):
            index = index if mode == 'down' else -index
            works_sheet.cell(row + index, col).value = value
    if mode == 'left' or mode == 'right':
        for index, value in enumerate(data):
            index = index if mode == 'right' else -index
            works_sheet.cell(row, col + index - 1).value = value


def get_xlsx_document_from_template(template_path, name, data):
    """
    Функция для формирования exel документа из шаблона
    @param template_path: название шаблона
    @param name: название конечного документа
    @param data: словарь содержащий информаию для занесение в документ, формат:
    {Position:[data1,...,dataN],...,PositionN:p[]} , где Position позиция в шаблоне, data -  данные для занесения
    @return: путь к конечному документу
    """
    work_book = load_workbook(TEMPLATE_ROOT + template_path)
    works_sheet = work_book.active
    for col in works_sheet.iter_cols():
        for row in col:
            if row.value and re.sub("<[^<]+>", "", str(row.value)) in data.keys():
                mode = row.value[row.value.find('<') + 1:row.value.find('>')] if row.value.find('<') != -1 else None
                if not mode:
                    row.value = data[row.value][0]
                else:
                    insert_list(works_sheet, mode, row, data[re.sub("<[^<]+>", "", row.value)])
    work_book.save(DOCUMENT_ROOT + name + '.xlsx')
    return DOCUMENT_ROOT + name + '.xlsx'


# get_document_from_template('template.xlsx', 'отчет2.xlsx', {'tops': [10,20,30], 'nums': [100,200,300,], 'test': ['a', 'b', 'c']})




