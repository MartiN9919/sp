from data_base_driver.constants.const_dat import DAT_SYS_NOTIFY, DAT_OWNER_USERS
from data_base_driver.connect.connect_mysql import db_sql


def get_status_by_alert(alert, file):
    """
    Вспомогательная функция для получения числового статуса в соответствии со строковым типом
    @param alert: строковый тип
    @param file: файл закрепленный за оповещением, если нет то None
    @return: числовой статус оповещения
    """
    if alert == 'information':
        return 501
    elif alert == 'warning':
        return 502
    elif alert == 'error':
        return 503


def get_alert_json(alert):
    return {'id_alert': alert[0], 'from': alert[1], 'content': alert[2], 'date_time': alert[3].isoformat(sep=' '),
            'status': get_status_by_alert(alert[4], alert[5]), 'file': alert[5], 'geometry': alert[6]}


def get_notifications_by_user(id, previous_list):
    """
    Функция для получения списка оповещений пользователя
    @param id: идентификационный номер пользователя получающего список
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
          + DAT_SYS_NOTIFY.TO_ID + ' = ' + str(id)

    user_alert = db_sql(sql)
    sql = 'SELECT ' + DAT_SYS_NOTIFY.ID + ' FROM '\
        + DAT_SYS_NOTIFY.TABLE_SHORT + ';'
    alerts = db_sql(sql)
    to_remove_set = set(previous_list) - set([alert[0] for alert in alerts])
    user_alert_dict = [get_alert_json(alert) for alert in user_alert if
                       not (int(alert[0]) in previous_list)]
    user_alert_dict = {'notifications': user_alert_dict, 'to_remove': list(to_remove_set)}
    return user_alert_dict

