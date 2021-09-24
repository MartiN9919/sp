import re

from openpyxl import Workbook, load_workbook

from core.settings import DOCUMENT_ROOT, TEMPLATE_ROOT


def get_document(title, data):
    work_book = Workbook()
    works_sheet = work_book.active
    works_sheet.title = title
    for key_index, key in enumerate(data):
        works_sheet.cell(column=key_index+1, row=1, value=key)
        for index, value in enumerate(data[key]):
            works_sheet.cell(column=key_index+1, row=index+2, value=value)
    work_book.save(DOCUMENT_ROOT + title + '.xlsx')


def insert_list(works_sheet, mode, start_cell, data):
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


def get_document_from_template(template_path, name, data):
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
    work_book.save(DOCUMENT_ROOT + name + 'xlsx')
    return DOCUMENT_ROOT + name + 'xlsx'


get_document_from_template('template.xlsx', 'отчет2.xlsx', {'tops': [10,20,30], 'nums': [100,200,300,], 'test': ['a', 'b', 'c']})




