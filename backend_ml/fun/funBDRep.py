# -*- coding: utf-8 -*-

from   fun.funConst import REP_TYPE
from   fun.funSys   import tsNow, cmpTiming, tsToMonth, tsToDays, tsToHours
from   fun.funBD    import bdSQL
from   fun.funText  import textStrip



###################################################################################
# ПОЛУЧИТЬ СПИСОК ДОСТУПНЫХ ТИПОВ ОТЧЕТОВ
###################################################################################
def getRepType(dbBD=-1, isOnce=False, worker=''):
    sql = \
        "SELECT "+ \
            REP_TYPE.ID        +", "+ \
            REP_TYPE.PARAM     +", "+ \
            REP_TYPE.ARGS      +", "+ \
            REP_TYPE.TIMING    +", "+ \
            REP_TYPE.START_ONCE+", "+ \
            REP_TYPE.DESCRIPT  +" "+ \
        "FROM "+REP_TYPE.TABLE+" " + \
        "WHERE " + \
            REP_TYPE.WORKER   +"='"+worker+"' AND "+ \
            REP_TYPE.ENABLED  +"=1 "+ \
            (("AND "+REP_TYPE.START_ONCE+"=1 ") if isOnce else "")+ \
        "ORDER BY "+REP_TYPE.SORT+" ASC"
    ret = []
    for rec in bdSQL(sql, True, True, dbBD):
        val = {}
        val[REP_TYPE.ID]         = str(rec[0])
        val[REP_TYPE.PARAM]      = rec[1].strip()
        val[REP_TYPE.ARGS]       = rec[2].strip()
        val[REP_TYPE.TIMING]     = rec[3].strip()
        val[REP_TYPE.START_ONCE] = str(rec[4])
        val[REP_TYPE.DESCRIPT]   = rec[5].strip()
        ret.append(val)
    return ret


###################################################################################
# УСТАНОВИТЬ/СБРОСИТЬ ПРИЗНАК REP_TYPE.START_ONCE
###################################################################################
def setRepTypeStartOnce(id, flag=False, dbBD=-1):
    val = 1 if flag else 0
    sql = \
        "UPDATE IGNORE "+REP_TYPE.TABLE+" "+ \
        "SET "   +REP_TYPE.START_ONCE+"="+str(val)+" "+ \
        "WHERE " +REP_TYPE.ID+"="+str(id)+" AND "+REP_TYPE.START_ONCE+"="+str(1-val)+" "+ \
        "LIMIT 1;"
    bdSQL(sql, True, False, dbBD)



###################################################################################
# АНАЛИЗ REP_TYPE.TIMING НА ЗАПУСК
###################################################################################
def isRepTypeTiming(now, fieldTiming=''):
    ret = False
    for itemTiming in fieldTiming.replace('\r','').split('\n'):                         # цикл по всем таймингам: itemTiming = '*/2 * *'
        if itemTiming.strip()=='': continue                                             # если пусто - пропустить
        lstTiming = textStrip(itemTiming).split(' ')                                    # удалить лишние пробелы, разбить в массив
        if len(lstTiming)<1: lstTiming.append(self.TIMING_ALL)                          # lstTiming = ['*/2', '*', '*']
        if len(lstTiming)<2: lstTiming.append(self.TIMING_ALL)
        if len(lstTiming)<3: lstTiming.append(self.TIMING_ALL)

        if not cmpTiming(lstTiming[0], tsToHours(now), 23): continue
        if not cmpTiming(lstTiming[1], tsToDays(now),  31): continue
        if not cmpTiming(lstTiming[2], tsToMonth(now), 12): continue
        ret = True
        break
    return ret
