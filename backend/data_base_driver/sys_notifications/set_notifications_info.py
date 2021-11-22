from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_NOTIFY
from datetime import datetime


def add_notification(to_id, type, content, date_time=datetime.now(), from_id='NULL', file_id='NULL', geometry='NULL',
                     test_mode=None):
    """
    Функция для добавления оповещения в базу данных
    @param from_id: идентификационный номер отправителя, по стандарту NULL
    @param to_id: идентификационный номер получателя
    @param type: тип оповещения
    @param content: текст оповещения
    @param file_id: идентификационный номер связанного файла, если имеется, если не то NULL
    @param date_time: дата и время оповещения, стандартное значение - время добавления
    @param geometry: геометрическая информация
    @param test_mode: флаг тестового режима
    """
    file_id = str(file_id) if file_id else 'NULL'
    content = content.replace('\'', '\\\'')
    geometry = geometry.replace('\'', '\\\'')
    sql = 'INSERT INTO ' + DAT_SYS_NOTIFY.TABLE_SHORT + ' (' \
          + DAT_SYS_NOTIFY.FROM_ID + ', ' \
          + DAT_SYS_NOTIFY.TO_ID + ', ' \
          + DAT_SYS_NOTIFY.DATE_TIME + ', ' \
          + DAT_SYS_NOTIFY.TYPE + ', ' \
          + DAT_SYS_NOTIFY.CONTENT + ', ' \
          + DAT_SYS_NOTIFY.FILE_ID + ', ' \
          + DAT_SYS_NOTIFY.GEOMETRY + ') VALUES (' \
          + str(from_id) + ', ' \
          + str(to_id) + ', \'' \
          + date_time.isoformat(sep=' ') + '\', \'' \
          + type + '\', \'' \
          + content + '\', ' \
          + str(file_id) + ', \'' \
          + geometry + '\');'
    id = db_sql(sql, read=False)[0]
    return id


def set_read(notification_id, user_id):
    """
    Функция для установки флага чтения уведомления
    @param notification_id: идентификатор прочитанного оповещения
    @param user_id: идентификатор пользователя
    """
    sql = 'UPDATE ' + DAT_SYS_NOTIFY.TABLE_SHORT \
        + 'SET ' + DAT_SYS_NOTIFY.IS_READ + ' = 1 '\
        + 'WHERE ' + DAT_SYS_NOTIFY.ID + ' = ' + str(notification_id) \
        + ' AND ' + DAT_SYS_NOTIFY.TO_USER + ' = ' + str(user_id) + ';'
    db_sql(sql, read=False)
