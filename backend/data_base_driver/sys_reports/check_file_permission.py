from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_FILES, DAT_OWNER


def check_file_permission(file_id, user_id):
    """
    Функция для проверки доступа пользователя к файлу
    @param file_id: идентификационный номер файла
    @param user_id: идентификационный номер пользователя
    @return: True если у данного пользователя есть доступ к файлу, False если такого доступа нет
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=user_id)
    sql = 'SELECT ' + DAT_SYS_FILES.OWNER_LINE + ', ' \
          + DAT_SYS_FILES.OWNER_REGION + ' FROM ' \
          + DAT_SYS_FILES.TABLE + ' WHERE ' \
          + DAT_SYS_FILES.ID + ' = ' + str(file_id)
    temp = db_sql(sql)
    return DAT_OWNER.DUMP.valid_line_region(group_id=group_id, owner_line=temp[0][0], owner_region=temp[0][1])
