from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_FILES
from datetime import datetime


def add_file(path, user_id, params, date_auto_remove=datetime.now(), status='in_progress'):
    """
    Функция для добавления информации о файле в базу данных
    @param path: путь к файлу, из него так же будет получено имя
    @param user_id: идентификатор пользователя
    @param date_auto_remove: время до авто удаления
    @param params: параметры запуска скрипта получения отчета
    @param status: статус готовности отчета
    """
    params = params.replace('\'', '\\\'')
    sql = 'INSERT INTO ' + DAT_SYS_FILES.TABLE_SHORT + ' (' \
          + DAT_SYS_FILES.PATH + ', ' \
          + DAT_SYS_FILES.NAME + ', ' \
          + DAT_SYS_FILES.USER_ID + ', ' \
          + DAT_SYS_FILES.DATE_AUTO_REMOVE + ', ' \
          + DAT_SYS_FILES.STATUS + ', ' \
          + DAT_SYS_FILES.PARAMS + ') VALUES (\'' \
          + path + '\', \'' \
          + path.split('/')[-1] + '\', ' \
          + str(user_id) + ', \'' \
          + date_auto_remove.isoformat(' ') + '\', \'' \
          + status + '\', \'' \
          + params + '\');'
    return db_sql(sql, read=False)[0]


def set_file_status(file_id, status):
    """
    Функция для установки статуса файла в базе данных
    @param file_id: идентификационный номер файла в базе данных
    @param status: статус который должен быть установлен
    """
    sql = 'UPDATE ' + DAT_SYS_FILES.TABLE_SHORT + ' SET ' \
          + DAT_SYS_FILES.STATUS + ' = \'' \
          + status + '\' WHERE ' \
          + DAT_SYS_FILES.ID + ' = ' \
          + str(file_id)
    db_sql(sql, read=False)


def set_file_path(file_id, path):
    """
    Функция для установки пути к файлу в базе данных
    @param file_id: идентификационный номер файла в базе данных
    @param path: путь к файлу который должен быть установлен
    """
    sql = 'UPDATE ' + DAT_SYS_FILES.TABLE_SHORT + ' SET ' \
          + DAT_SYS_FILES.PATH + ' = \'' \
          + path + '\' WHERE ' \
          + DAT_SYS_FILES.ID + ' = ' \
          + str(file_id)
    db_sql(sql, read=False)

