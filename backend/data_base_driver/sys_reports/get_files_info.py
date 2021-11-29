import json

from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_FILES, DAT_OWNER


def get_list_files_by_user(user_id, length, offset):
    """
    Функция для получения списка файлов пользователя
    @param user_id: идентификационный номер пользователя
    @param length: сколько файлов на странице
    @param offset: номер страницы
    @return: список словарей в формате [{id1,name1},{},...{}]
    """
    sql = 'SELECT ' + DAT_SYS_FILES.ID + ', ' \
          + DAT_SYS_FILES.NAME + ', ' \
          + DAT_SYS_FILES.DATE_AUTO_REMOVE + ', ' \
          + DAT_SYS_FILES.STATUS + ', ' \
          + DAT_SYS_FILES.PARAMS + ' FROM ' \
          + DAT_SYS_FILES.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_FILES.USER_ID + ' = ' + str(user_id) + ' ORDER BY '\
          + DAT_SYS_FILES.DATE_AUTO_REMOVE + ' LIMIT '\
          + str(length) + ' OFFSET ' + str((offset-1)*length) + ';'
    temp = db_sql(sql)
    sql = 'SELECT COUNT(*) FROM ' + DAT_SYS_FILES.TABLE_SHORT \
          + ' WHERE ' + DAT_SYS_FILES.USER_ID \
          + ' = ' + str(user_id) + ';'
    total = db_sql(sql)[0][0]
    reports_list = [
        {
            'id': file[0],
            'name': file[1],
            'date': file[2].replace(microsecond=0, tzinfo=None).isoformat(sep=' '),
            'status': file[3], 'params': json.loads(file[4])
         } for file in temp
    ]
    return {'list': reports_list, 'total': total}



def get_file_path(file_id):
    """
    Функция для получения пути к файлу
    @param file_id: идентификационный номер файла
    @return: путь к файлу в текстовом формате
    """
    sql = 'SELECT ' + DAT_SYS_FILES.PATH + ' FROM ' \
          + DAT_SYS_FILES.TABLE + ' WHERE ' \
          + DAT_SYS_FILES.ID + ' = ' + str(file_id)
    file_path = db_sql(sql)
    if len(file_path) == 0:
        raise ('Error, file dont found')
    return str(file_path[0][0])
