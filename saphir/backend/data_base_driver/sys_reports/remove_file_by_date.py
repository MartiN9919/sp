import os
from datetime import datetime
from data_base_driver.constants.const_dat import DAT_SYS_FILES
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_file import BASE_SYSTEM_FILE_PATH


def get_delete_sql(id):
    """
    Функция для получения строки sql запроса на удаление файла
    @param id: идентификационный номер файла
    @return: строка sql запроса на удаление файла
    """
    return 'DELETE FROM ' + DAT_SYS_FILES.TABLE_SHORT + ' WHERE ' \
           + DAT_SYS_FILES.ID + ' = ' + str(id) + ';'


def remove_file_by_date():
    """
    Функция для удаления из базы данных файлов с истекшим временем хранения, удаляет запись о файле из базы данных и
    файл из файловой системы
    """
    date_time = datetime.now().isoformat(' ')
    sql = 'SELECT ' + DAT_SYS_FILES.ID + ', ' \
          + DAT_SYS_FILES.PATH + ' FROM ' \
          + DAT_SYS_FILES.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_FILES.DATE_AUTO_REMOVE + ' < \'' \
          + date_time + '\';'
    file_to_remove = db_sql(sql)
    for file in file_to_remove:
        try:
            os.remove(BASE_SYSTEM_FILE_PATH + file[1])
        except:
            pass
        db_sql(get_delete_sql(file[0]), read=False)
