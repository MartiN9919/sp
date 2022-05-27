from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_FILES, DAT_OWNER


def check_file_permission(file_id, user_id):
    """
    Функция для проверки доступа пользователя к файлу
    @param file_id: идентификационный номер файла
    @param user_id: идентификатор пользователя
    @return: True если у данного пользователя есть доступ к файлу, False если такого доступа нет
    """
    sql = 'SELECT ' + DAT_SYS_FILES.USER_ID + ' FROM ' \
          + DAT_SYS_FILES.TABLE + ' WHERE ' \
          + DAT_SYS_FILES.ID + ' = ' + str(file_id)
    temp = db_sql(sql)
    return int(temp[0][0]) == user_id
