# -*- coding: utf-8 -*-

import random
from   fun.funConst import LOADER_TYPE, LOADER_NOD, LOADER_SYNC, LOADER_URL
from   fun.funBD    import bdSQL
from   fun.funSys   import logError, tsNow, sqlDateTime, sqlDateTimeNow



#####################################################
# LOADER_NOD: имя группы
#####################################################
def getLoaderName(host, id, db=-1):
    sql = \
        "SELECT "+LOADER_NOD.NAME+" "+ \
        "FROM "  +LOADER_NOD.TABLE+" "+ \
        "WHERE ("+LOADER_NOD.HOST+"='"+host+"') AND ("+LOADER_NOD.GROUP_ID+"='"+id+"') "+ \
        "LIMIT 1;"
    val = bdSQL(sql, True, True, db)
    val = val[0] if len(val) == 1 else ['']
    return val[0]



#####################################################
# LOADER_SYNC: данные синхронизации времени
#####################################################
class GetLoaderSync:
    VAR1 = 0
    VAR2 = 1
    VAL  = 2

def getLoaderSync(host):
    sql = "SELECT "+LOADER_SYNC.VAR1+", "+LOADER_SYNC.VAR2+", "+LOADER_SYNC.VAL+" "+ \
          "FROM "  +LOADER_SYNC.TABLE+" "+ \
          "WHERE ("+LOADER_SYNC.HOST+"='"+host+"');"
    return bdSQL(sql, True, True)




#####################################################
# LOADER_NOD: список rss-каналов
#####################################################
class GetNodRss:
    HOST       = 0
    URL        = 1
    COUNTRY    = 2
    TS_CORRECT = 3
def getNodRss(worker=''):
    sql = "SELECT "+LOADER_NOD.HOST+", "+LOADER_NOD.URL+", "+LOADER_NOD.COUNTRY+", "+LOADER_NOD.TS_CORRECT+" "+\
          "FROM "  +LOADER_NOD.TABLE +" "+\
          "WHERE ("+LOADER_NOD.LOADER_TYPE_ID+"="+LOADER_TYPE.ID_RSS+") AND "+\
                "("+LOADER_NOD.WORKER+"='"+worker+"') AND "+\
                "("+LOADER_NOD.ENABLED+"=1) "+\
          "ORDER BY "+LOADER_NOD.HOST+" ASC;"
    return bdSQL(sql, True, True)



#####################################################
# LOADER_NOD: данные выкачиваемого объекта
#####################################################
# return   - список id объектов
#####################################################
class GetNodObjects:
    GROUP_ID       = 0
    NAME           = 1
    URL            = 2
    VIP            = 3
def getNodObjects(host, worker):
    sql = "SELECT "+LOADER_NOD.GROUP_ID+", "+LOADER_NOD.NAME+", "+LOADER_NOD.URL+", "+LOADER_NOD.VIP+" "+ \
          "FROM "  +LOADER_NOD.TABLE+" "+ \
          "WHERE ("+LOADER_NOD.HOST+"='"+host+"') AND ("+LOADER_NOD.WORKER+"='"+worker+"') AND ("+LOADER_NOD.ENABLED+"=1);"
    return bdSQL(sql, True, True)



#####################################################
# LOADER_NOD: field = val
#####################################################
# fieldID_val - group_id - для сообществ со знаком "-" !!!
# fieldSET_val - может быть str, int, bool
#####################################################
def setNodField(host, worker, fieldID_nam, fieldID_val, fieldSET_nam, fieldSET_val):
    valNew = ("'"+fieldSET_val+"'") if isinstance(fieldSET_val, str) else str(fieldSET_val)
    sql = "UPDATE IGNORE "+LOADER_NOD.TABLE+" "+ \
          "SET "+fieldSET_nam+"="+valNew+" "+ \
          "WHERE ("+LOADER_NOD.HOST+"='"+host+"') AND ("+LOADER_NOD.WORKER+"='"+worker+"') AND ("+fieldID_nam+"='"+str(fieldID_val)+"');"
    bdSQL(sql, True, False)


def getNodFields(sqlFields, sqlWhere=''):
    sql = "SELECT "+sqlFields+" "+ \
          "FROM "  +LOADER_NOD.TABLE+" "+ \
          "WHERE ("+LOADER_NOD.ENABLED+"=1) "+(("AND ("+sqlWhere+") ") if sqlWhere!="" else "") + \
          ";"
    return bdSQL(sql, True, True)




#####################################################
# LOADER_NOD: список site-каналов
#####################################################
class GetNodSite:
    HOST       = 0
    URL        = 1
    PARAM      = 2
    COUNTRY    = 3
    TS_CORRECT = 4
def getNodSite(worker=''):
    sql = "SELECT "+LOADER_NOD.HOST+", "+LOADER_NOD.URL+", "+LOADER_NOD.PARAM+", "+LOADER_NOD.COUNTRY+", "+LOADER_NOD.TS_CORRECT+" "+\
          "FROM "  +LOADER_NOD.TABLE +" "+\
          "WHERE ("+LOADER_NOD.LOADER_TYPE_ID+"="+LOADER_TYPE.ID_SITE+") AND "+\
                "("+LOADER_NOD.WORKER+"='"+worker+"') AND "+\
                "("+LOADER_NOD.ENABLED+"=1) "+\
          "ORDER BY "+LOADER_NOD.HOST+" ASC;"
    return bdSQL(sql, True, True)








#####################################################
# LOADER_URL: добавить URL
#####################################################
def loaderUrlAdd(url):
    period = 3 * 60 * 60
    ts     = tsNow()+period
    delta  = round(period*0.3)
    sql    = \
        "INSERT IGNORE INTO " + \
            LOADER_URL.TABLE        + " (" + \
                LOADER_URL.URL      + ", " + \
                LOADER_URL.DATE_DEL + ") " + \
        "VALUES ("          + \
            "'"+url                                                   + "', " + \
            "'"+sqlDateTime(round(random.uniform(ts-delta, ts+delta)))+ "' "  + \
        ")"
    bdSQL(sql, True, False)


#####################################################
# LOADER_URL: проверить URL
#####################################################
def loaderUrlVerify(url):
    sql = \
        "SELECT 1 " + \
        "FROM " + LOADER_URL.TABLE +" " + \
        "WHERE "+ LOADER_URL.URL + "='"+url+"' "+ \
        "LIMIT 1"
    return len(bdSQL(sql, True, True)) > 0


#####################################################
# LOADER_URL: очистить старые URL
#####################################################
def loaderUrlClear():
    sql = \
        "DELETE " + \
        "FROM " + LOADER_URL.TABLE +" " + \
        "WHERE "+ LOADER_URL.DATE_DEL + "<'"+sqlDateTimeNow()+"'"
    bdSQL(sql, True, False)
