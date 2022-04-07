# -*- coding: utf-8 -*-

from fun.funConst import LOADER_LIST
from fun.funSys   import sqlDateTime, tsNow
from fun.funBD    import bdSQL


# добавить записи (lst - список словарей-записей)
def loaderListRecAddList(owner, worker, lst, db=-1):
    sql = \
        "INSERT IGNORE INTO "+ \
            LOADER_LIST.TABLE +" ("+ \
            LOADER_LIST.OWNER +", "+ \
            LOADER_LIST.WORKER+", "+ \
            LOADER_LIST.VAL1  +", "+ \
            LOADER_LIST.VAL2  +", "+ \
            LOADER_LIST.VAL3  +", "+ \
            LOADER_LIST.VAL4  +", "+ \
            LOADER_LIST.DAT   +") "+ \
        "VALUES "
    for item in lst:
        sql += "("+ \
            "'"+owner                         +"', "+ \
            "'"+worker                        +"', "+ \
            "'"+item.get(LOADER_LIST.VAL1, '')+"', "+ \
            "'"+item.get(LOADER_LIST.VAL2, '')+"', "+ \
            "'"+item.get(LOADER_LIST.VAL3, '')+"', "+ \
            "'"+item.get(LOADER_LIST.VAL4, '')+"', "+ \
            (("'"+sqlDateTime(item[LOADER_LIST.DAT])+"'),") if item.get(LOADER_LIST.DAT, None) else "")
    if sql[-1]==',': sql=sql[:-1]
    bdSQL(sql=sql, wait=True, read=False, db=db)


# работает но не используется
# добавить запись
# def loaderListRecAdd(owner, worker, val1='', val2='', val3='', val4='', dat_ts=0, db=-1):
#     sql = \
#         "INSERT IGNORE INTO "+LOADER_LIST.TABLE+" SET "+ \
#         LOADER_LIST.OWNER +"='"+owner +"'" + \
#         ((", "+LOADER_LIST.WORKER+"='"+worker             +"'") if worker!="" else "")+ \
#         ((", "+LOADER_LIST.VAL1  +"='"+val1               +"'") if val1  !="" else "")+ \
#         ((", "+LOADER_LIST.VAL2  +"='"+val2               +"'") if val2  !="" else "")+ \
#         ((", "+LOADER_LIST.VAL3  +"='"+val3               +"'") if val3  !="" else "")+ \
#         ((", "+LOADER_LIST.VAL4  +"='"+val4               +"'") if val4  !="" else "")+ \
#         ((", "+LOADER_LIST.DAT   +"='"+sqlDateTime(dat_ts)+"'") if dat_ts!=0  else "")
#     bdSQL(sql=sql, wait=True, read=False, db=db)


# обновить поля val3, val4, dat_ts записи, идентифицируемой по ключу (owner, worker, val1, val2)
def loaderListRecUpdate(owner, worker, val1='', val2='', val3='', val4='', dat_ts=0, db=-1):
    sql = \
        "UPDATE IGNORE "+LOADER_LIST.TABLE+" SET "+ \
            ((LOADER_LIST.VAL3  +"='"+val3               +"',") if val3  !="" else "")+ \
            ((LOADER_LIST.VAL4  +"='"+val4               +"',") if val4  !="" else "")+ \
            ((LOADER_LIST.DAT   +"='"+sqlDateTime(dat_ts)+"',") if dat_ts!=0  else "")
    if sql[-1]==',': sql=sql[:-1]
    sql += \
        " WHERE " + \
            LOADER_LIST.OWNER +"='"+owner +"'" + \
            ((" AND "+LOADER_LIST.WORKER+"='"+worker     +"'") if worker!="" else "")+ \
            ((" AND "+LOADER_LIST.VAL1  +"='"+val1       +"'") if val1  !="" else "")+ \
            ((" AND "+LOADER_LIST.VAL2  +"='"+val2       +"'") if val2  !="" else "")
    bdSQL(sql=sql, wait=True, read=False, db=db)


# прочитать запись
def loaderListRecGet(owner, worker, dat_min_ts=0, db=-1):
    sql = \
        "SELECT "+LOADER_LIST.VAL1+", "+LOADER_LIST.VAL2+", "+LOADER_LIST.VAL3+", "+LOADER_LIST.VAL4+", "+LOADER_LIST.DAT+" "+ \
        "FROM "+LOADER_LIST.TABLE+" "+ \
        "WHERE ("+LOADER_LIST.OWNER+"='"+owner+"') AND ("+LOADER_LIST.WORKER+"='"+worker+"')"+ ((" AND ("+LOADER_LIST.DAT+">='"+sqlDateTime(dat_min_ts)+"')") if dat_min_ts>0 else "")
    for item in bdSQL(sql=sql, wait=True, read=True, db=db):
        yield {
            LOADER_LIST.VAL1: item[0],
            LOADER_LIST.VAL2: item[1],
            LOADER_LIST.VAL3: item[2],
            LOADER_LIST.VAL4: item[3],
            LOADER_LIST.DAT:  item[4],
        }


# удалить записи старше period_days дней
def loaderListRecDel(owner, worker, period_days, db=-1):
    sql = \
        "DELETE  FROM "+LOADER_LIST.TABLE+" "+ \
        "WHERE ("+LOADER_LIST.OWNER+"='"+owner+"') AND ("+LOADER_LIST.WORKER+"='"+worker+"') AND ("+LOADER_LIST.DAT+"<'"+sqlDateTime(tsNow()-period_days*24*60*60)+"')"
    bdSQL(sql=sql, wait=True, read=False, db=db)
