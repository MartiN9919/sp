from data_base_driver.constants.const_dat import DAT_SYS_NOTIFY, DAT_OWNER_USERS
from data_base_driver.connect.connect_mysql import db_sql


def get_alert_json(alert):
    return {'id_alert': alert[0], 'from': alert[1], 'content': alert[2], 'date_time': alert[3].isoformat(sep=' '),
            'status': alert[4], 'file': alert[5], 'geometry': alert[6]}


def get_notifications_by_user(user_id, previous_list):
    """
    Функция для получения списка оповещений пользователя
    @param user_id: идентификационный номер пользователя получающего список
    @param previous_list: список оповещений которые не требуются пользователю
    @return: список словарей в формате [{id1,from_id1,content1,date_time1,type1,file1},{},...{}]
    """
    sql = 'SELECT a.' + DAT_SYS_NOTIFY.ID + ', u.username, a.' \
          + DAT_SYS_NOTIFY.CONTENT + ', a.' \
          + DAT_SYS_NOTIFY.DATE_TIME + ', a.' \
          + DAT_SYS_NOTIFY.TYPE + ', a.' \
          + DAT_SYS_NOTIFY.FILE_ID + ', ' \
          + DAT_SYS_NOTIFY.GEOMETRY + ' FROM ' \
          + DAT_SYS_NOTIFY.TABLE_SHORT + ' a LEFT JOIN ' \
          + DAT_OWNER_USERS.TABLE_SHORT + ' u ON u.id = a.' \
          + DAT_SYS_NOTIFY.FROM_ID + ' WHERE a.' \
          + DAT_SYS_NOTIFY.TO_ID + ' = ' + str(user_id) + ' AND '\
          + DAT_SYS_NOTIFY.IS_READ + ' = 0;'
    user_alerts = db_sql(sql)
    return [get_alert_json(alert) for alert in user_alerts if not (int(alert[0]) in previous_list)]


def get_notifications_list_by_offset(user_id, length, offset, date, notification_type, order='up'):
    """
    Функция для ранжироввнного получения оповещений
    @param user_id: идентификатор пользователя, которому предназначены оповещения
    @param length: количество оповещений на странице
    @param offset: номер страницы
    @param date: дата если имеется, если нет None
    @param notification_type: тип ововещения, если любой None
    @param order: тип сортировки, по умолчанию от новых к старым, для изменения down
    @return: объект содержащий список оповещений и их общее количество при заданных параметрах
    """
    if order == 'up':
        order = True
    else:
        order = False
    where_list = []
    if date:
        where_list.append(DAT_SYS_NOTIFY.DATE_TIME + ' BETWEEN \'' + str(date) + ' 00:00:00\' AND \'' + str(date) + ' 23:59:59\'')
    if notification_type:
        where_list.append('`' + DAT_SYS_NOTIFY.TYPE + '` = \'' + notification_type + '\'')
    where_list.append('a.' + DAT_SYS_NOTIFY.TO_ID + ' = ' + str(user_id))
    where = ' WHERE ' + ' AND '.join(where_list)
    sql = 'SELECT a.' + DAT_SYS_NOTIFY.ID + ', u.username, a.' \
          + DAT_SYS_NOTIFY.CONTENT + ', a.' \
          + DAT_SYS_NOTIFY.DATE_TIME + ', a.' \
          + DAT_SYS_NOTIFY.TYPE + ', a.' \
          + DAT_SYS_NOTIFY.FILE_ID + ', ' \
          + DAT_SYS_NOTIFY.GEOMETRY + ' FROM ' \
          + DAT_SYS_NOTIFY.TABLE_SHORT + ' a LEFT JOIN ' \
          + DAT_OWNER_USERS.TABLE_SHORT + ' u ON u.id = a.' \
          + DAT_SYS_NOTIFY.FROM_ID + where + ' ORDER BY ' \
          + DAT_SYS_NOTIFY.DATE_TIME + str(' DESC' if order else '') + ' LIMIT ' \
          + str(length) + ' OFFSET ' + str(length*(offset - 1)) + ';'
    user_alerts = db_sql(sql)
    where_list.pop()
    where_list.append(DAT_SYS_NOTIFY.TO_ID + ' = ' + str(user_id))
    where = ' WHERE ' + ' AND '.join(where_list)
    sql = 'SELECT COUNT(*) FROM ' + DAT_SYS_NOTIFY.TABLE_SHORT + where + ';'
    rows_nun = db_sql(sql)[0][0]
    return {'list': [get_alert_json(alert) for alert in user_alerts], 'total': rows_nun}