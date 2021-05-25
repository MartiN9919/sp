import json

from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_FILES, DAT_OWNER


def get_list_files_by_user(id):
    """
    Функция для получения списка файлов пользователя
    @param id: идентификационный номер пользователя
    @return: список словарей в формате [{id1,name1},{},...{}]
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=id)
    sql = 'SELECT ' + DAT_SYS_FILES.ID + ', ' \
          + DAT_SYS_FILES.NAME + ', ' \
          + DAT_SYS_FILES.OWNER_LINE_ID + ', ' \
          + DAT_SYS_FILES.OWNER_REGION_ID + ', ' \
          + DAT_SYS_FILES.DATE_AUTO_REMOVE + ', ' \
          + DAT_SYS_FILES.STATUS + ', ' \
          + DAT_SYS_FILES.PARAMS + ' FROM ' \
          + DAT_SYS_FILES.TABLE_SHORT + ';'
    temp = db_sql(sql)
    files_tuple = list(
        filter(lambda x: DAT_OWNER.DUMP.valid_line_region(group_id=group_id, owner_line=x[2], owner_region=x[3]),
               temp))
    return [{'id': file[0], 'name': file[1], 'date': file[4].replace(microsecond=0, tzinfo=None).isoformat(sep=' '),
             'status': file[5], 'params': json.loads(file[6])}
            for file in files_tuple]


def get_file_path(id):
    """
    Функция для получения пути к файлу
    @param id: идентификационный номер файла
    @return: путь к файлу в текстовом формате
    """
    sql = 'SELECT ' + DAT_SYS_FILES.PATH + ' FROM ' \
          + DAT_SYS_FILES.TABLE + ' WHERE ' \
          + DAT_SYS_FILES.ID + ' = ' + str(id)
    file_path = db_sql(sql)
    if len(file_path) == 0:
        raise ('Error, file dont found')
    return str(file_path[0][0])
