import json

from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_TEMPLATES, DAT_OWNER


def get_templates_list(user_id):
    """
    Функция для получения листа шаблонов доступных пользователю
    @param user_id: идентификационный номер пользователя, для получения группы
    @return: список словарей в формате [{'id':id1,'title':title1},{},...,{}]
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=user_id)
    sql = 'SELECT ' + DAT_SYS_TEMPLATES.ID + ', ' \
          + DAT_SYS_TEMPLATES.TITLE + ' FROM ' \
          + DAT_SYS_TEMPLATES.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_TEMPLATES.GROUP_ID + ' = ' \
          + str(group_id) + ';'
    return [{'id': template[0], 'title': template[1]} for template in db_sql(sql)]


def get_template(template_id, user_id):
    """
    Функция для получения шаблона по его идентификационному номеру
    @param template_id: идентификационный номер шаблона в базе данных
    @param user_id: идентификационный номер пользователя для проверки доступа
    @return: словарь в формате {'id':id,'title':title,'scripts':script}
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=user_id)
    sql = 'SELECT ' + DAT_SYS_TEMPLATES.GROUP_ID + ', ' \
          + DAT_SYS_TEMPLATES.TITLE + ', ' \
          + DAT_SYS_TEMPLATES.ACTIVE_SCRIPTS + ', ' \
          + DAT_SYS_TEMPLATES.PASSIVE_SCRIPTS + ' FROM ' \
          + DAT_SYS_TEMPLATES.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_TEMPLATES.ID + ' = ' \
          + str(template_id) + ';'
    template = db_sql(sql)
    if len(template) == 0:
        raise ('Template dont find')
    if template[0][0] != group_id:
        raise ('Access Denied')
    return {'id': template_id, 'title': template[0][1], 'activeAnalysts': json.loads(template[0][2]),
            'passiveAnalysts': json.loads(template[0][3])}
