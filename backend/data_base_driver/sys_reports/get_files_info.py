import json

from data_base_driver.additional_functions import date_time_server_to_client
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_FILES, DAT_OWNER


def get_list_files(user_id, length, offset):
    sql = 'SELECT ' + DAT_SYS_FILES.ID + ', ' \
          + DAT_SYS_FILES.NAME + ', ' \
          + DAT_SYS_FILES.DATE_AUTO_REMOVE + ', ' \
          + DAT_SYS_FILES.STATUS + ', ' \
          + DAT_SYS_FILES.PARAMS + ' FROM ' \
          + DAT_SYS_FILES.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_FILES.USER_ID + ' = ' + str(user_id) + ' ORDER BY ' \
          + DAT_SYS_FILES.DATE_AUTO_REMOVE + ' DESC LIMIT ' \
          + str(length) + ' OFFSET ' + str((offset - 1) * length) + ';'
    return [
        {
            'id': file[0],
            'name': file[1],
            'date': date_time_server_to_client(file[2].replace(microsecond=0, tzinfo=None).isoformat(sep=' ')),
            'status': file[3], 'params': json.loads(file[4])
        } for file in db_sql(sql)
    ]


def get_total_reports(user_id):
    sql = 'SELECT COUNT(*) FROM ' + DAT_SYS_FILES.TABLE_SHORT \
          + ' WHERE ' + DAT_SYS_FILES.USER_ID \
          + ' = ' + str(user_id) + ';'
    return db_sql(sql)[0][0]


def get_in_progress_list(user_id):
    sql = 'SELECT ' + DAT_SYS_FILES.ID + ' ' \
          + DAT_SYS_FILES.PARAMS + ' FROM ' \
          + DAT_SYS_FILES.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_FILES.USER_ID + ' = ' + str(user_id) + ' AND ' \
          + DAT_SYS_FILES.STATUS + ' = \'' + DAT_SYS_FILES.IN_PROGRESS + '\';'
    return [item[0] for item in db_sql(sql)]


def get_reports(user_id, length, offset):
    reports_list = get_list_files(user_id, length, offset)
    total = get_total_reports(user_id)
    in_progress_list = get_in_progress_list(user_id)
    return {'list': reports_list, 'total': total, 'in_progress': in_progress_list}


def check_progress(user_id, in_progress_list, length, offset):
    in_progress_server_list = get_in_progress_list(user_id)
    done_list = list(set(in_progress_list).difference(set(in_progress_server_list)))
    if len(done_list) > 0:
        return {
            'list': get_list_files(user_id, length, offset),
            'total': get_total_reports(user_id),
            'in_progress': in_progress_server_list
        }
    else:
        return {'in_progress': in_progress_server_list}


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
