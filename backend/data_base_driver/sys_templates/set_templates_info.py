import json

from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_TEMPLATES, DAT_OWNER


def add_template(group_id, title, active_scripts, passive_scripts):
    """
    Функция для добавления шаблона в базу данных
    @param group_id: идентификационный номер группы пользователей
    @param title: название шаблона
    @param active_scripts: json с активными скриптами
    @param passive_scripts: json с пассивными скриптами
    """
    active_scripts = json.dumps(active_scripts, ensure_ascii=False)
    passive_scripts = json.dumps(passive_scripts, ensure_ascii=False)
    active_scripts = active_scripts.replace('\\', '\\\\').replace('\'', '\\\'')
    passive_scripts = passive_scripts.replace('\\', '\\\\').replace('\'', '\\\'')
    sql = 'INSERT INTO ' + DAT_SYS_TEMPLATES.TABLE_SHORT + ' (' \
          + DAT_SYS_TEMPLATES.GROUP_ID + ', ' \
          + DAT_SYS_TEMPLATES.TITLE + ', ' \
          + DAT_SYS_TEMPLATES.ACTIVE_SCRIPTS + ', ' \
          + DAT_SYS_TEMPLATES.PASSIVE_SCRIPTS + ') VALUES (' \
          + str(group_id) + ', \'' \
          + title + '\', \'' \
          + active_scripts + '\',\''\
          + passive_scripts + '\');'
    return db_sql(sql, read=False)[0]


def update_template(template_id, user_id, title, active_scripts, passive_scripts):
    """
    Функция для изменения шаблона в базе данных
    @param template_id: идентификационный номер шаблона в базе данных
    @param user_id: идентификационный номер пользователя
    @param title: новое название шаблона
    @param active_scripts: новый json с активными скриптами
    @param passive_scripts: новый json с пассивными скриптами
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=user_id)
    active_scripts = json.dumps(active_scripts, ensure_ascii=False)
    passive_scripts = json.dumps(passive_scripts, ensure_ascii=False)
    active_scripts = active_scripts.replace('\\', '\\\\').replace('\'', '\\\'')
    passive_scripts = passive_scripts.replace('\\', '\\\\').replace('\'', '\\\'')
    sql = 'SELECT ' + DAT_SYS_TEMPLATES.GROUP_ID + ' FROM ' \
          + DAT_SYS_TEMPLATES.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_TEMPLATES.ID + ' = ' + str(template_id)
    template = db_sql(sql)
    if len(template) != 1:
        raise ('шаблон не найден')
    elif template[0][0] != int(group_id):
        raise ('нет доступа к изменению')
    sql = 'UPDATE ' + DAT_SYS_TEMPLATES.TABLE_SHORT + ' SET ' \
          + DAT_SYS_TEMPLATES.ACTIVE_SCRIPTS + ' = \'' + active_scripts + '\', ' \
          + DAT_SYS_TEMPLATES.PASSIVE_SCRIPTS + ' = \'' + passive_scripts + '\', ' \
          + DAT_SYS_TEMPLATES.TITLE + ' = \'' + title + '\' WHERE ' \
          + DAT_SYS_TEMPLATES.ID + ' = ' + str(template_id)
    db_sql(sql, read=False)


def remove_template(user_id, template_id):
    """
    Функция для удаления шаблона из базы данных
    @param user_id: идентификационный номер пользователя, для проверки уровня доступа
    @param template_id: идентификационный номер шаблона
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=user_id)
    sql = 'SELECT ' + DAT_SYS_TEMPLATES.GROUP_ID + ' FROM ' \
          + DAT_SYS_TEMPLATES.TABLE_SHORT + ' WHERE ' \
          + DAT_SYS_TEMPLATES.ID + ' = ' + str(template_id)
    template = db_sql(sql)
    if len(template) != 1:
        raise ('No such template')
    elif template[0][0] != group_id:
        raise ('access dinied')
    sql = 'DELETE FROM ' + DAT_SYS_TEMPLATES.TABLE_SHORT \
          + ' WHERE ' + DAT_SYS_TEMPLATES.ID \
          + ' = ' + str(template_id)
    db_sql(sql, read=False)




