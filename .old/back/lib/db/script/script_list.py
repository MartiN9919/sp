# -*- coding: utf-8 -*-

from   pprint                       import pprint

from   lib.db.const.const_connect   import CONNECT
from   lib.db.const.const_dat       import DAT_SYS_SCRIPT, DAT_OWNER
from   lib.db.connect.connect_mysql import DB_sql as MYSQL
from   lib.sys                      import tuple_to_dict_many


DEBUG = False


###########################################
# СПИСОК ДОСТУПНЫХ СКРИПТОВ
###########################################
def script_list(group_id, parent_id=-1):
    db  = MYSQL(database=CONNECT.DATA)
    sql = ""+\
        "SELECT "+\
            DAT_SYS_SCRIPT.ID       +", "+\
            DAT_SYS_SCRIPT.PARENT_ID+", "+\
            DAT_SYS_SCRIPT.NAME     +", "+\
            DAT_SYS_SCRIPT.TITLE    +", "+\
            DAT_SYS_SCRIPT.ICON     +", "+\
            DAT_SYS_SCRIPT.HINT     +", "+\
            DAT_SYS_SCRIPT.OWNER_LINE+" "+\
        "FROM "  + DAT_SYS_SCRIPT.TABLE_SHORT+" "+\
        "WHERE " + \
            DAT_SYS_SCRIPT.ENABLED+"=1"
    if parent_id>-1:
        sql += \
            " AND "+ \
            DAT_SYS_SCRIPT.PARENT_ID+"="+str(parent_id)
    rec = db.execute(sql=sql, wait=not DEBUG, read=True)
    if DEBUG:
        print('\nscript_list rec origin')
        pprint(rec)
        print('\n')

    # проверка на доступ
    rec = list(filter(lambda x: DAT_OWNER.DUMP.valid_line_group(group_id=group_id, line_id=x[-1]), rec))    # !!!!! x[-1]
    rec = tuple_to_dict_many(rec, [
        DAT_SYS_SCRIPT.ID,
        DAT_SYS_SCRIPT.PARENT_ID,
        DAT_SYS_SCRIPT.NAME,
        DAT_SYS_SCRIPT.TITLE,
        DAT_SYS_SCRIPT.ICON,
        DAT_SYS_SCRIPT.HINT,
        DAT_SYS_SCRIPT.OWNER_LINE,
    ])
    if DEBUG:
        print('\nscript_list rec return')
        pprint(rec)
        print('\n')

    return rec
