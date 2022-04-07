from document_driver.pdf_driver import get_pdf_document_text
from document_driver.word_driver import get_docx_document_text


def get_document_text(path):
    """
    Функция для получения текста документа
    @param path: путь к документу
    @return: текст документа
    """
    file_type = path.split('/')[-1].split('.')[1]
    if file_type == 'docx':
        return get_docx_document_text(path)
    elif file_type == 'pdf':
        return get_pdf_document_text(path)
    else:
        return None