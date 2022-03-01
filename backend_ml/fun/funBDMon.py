# -*- coding: utf-8 -*-
import copy, datetime

from fun.funConst import ARC, IARC, MON_TYPE, MON
from fun.funSys   import tsNow, sqlDateTime
from fun.funText  import textCutDots, textWithoutObj

import fun.funBD, fun.funSphinx


################################################################################
#   РАБОТА С ATLAS.MON_TYPE
################################################################################

#===========================================================================================
# MON_TYPE CONTROL: добавить запись-контроль
#===========================================================================================
monTypeControlNamTitle   = lambda nam: 'Темы: КОНТРОЛЬ ['      +nam[:255]+'], (24ч)'
monTypeControlNamContent = lambda nam: 'Публикации: КОНТРОЛЬ ['+nam[:255]+'], (24ч)'
def monTypeControlAdd(nam, val, descript=''):
    monTypeControlValTitle   = lambda val: '"nod_text": "@title_name '+val+'"'
    monTypeControlValContent = lambda val: '"nod_text": "@content '   +val+'"'

    setSQL = lambda dat: \
        "INSERT IGNORE INTO " + \
            MON_TYPE.TABLE           + " (" + \
                MON_TYPE.WORKER      + ", " + \
                MON_TYPE.SORT        + ", " + \
                MON_TYPE.TITLE       + ", " + \
                MON_TYPE.HANDLER     + ", " + \
                MON_TYPE.PARAM_1     + ", " + \
                MON_TYPE.PARAM_2     + ", " + \
                MON_TYPE.PARAM_3     + ", " + \
                MON_TYPE.NOD         + ", " + \
                MON_TYPE.STEP        + ", " + \
                MON_TYPE.ROW_COUNT   + ", " + \
                MON_TYPE.WIDTH       + ", " + \
                MON_TYPE.COLOR       + ", " + \
                MON_TYPE.ENABLED     + ", " + \
                MON_TYPE.DESCRIPT    + ", " + \
                MON_TYPE.REFRESH     + ") " + \
        "VALUES ("          + \
            "'"+dat[MON_TYPE.WORKER]    + "', " + \
                dat[MON_TYPE.SORT]      + ", "  + \
            "'"+dat[MON_TYPE.TITLE]     + "', " + \
            "'"+dat[MON_TYPE.HANDLER]   + "', " + \
            "'"+dat[MON_TYPE.PARAM_1]   + "', " + \
            "'"+dat[MON_TYPE.PARAM_2]   + "', " + \
            "'"+dat[MON_TYPE.PARAM_3]   + "', " + \
                dat[MON_TYPE.NOD]       + ", "  + \
                dat[MON_TYPE.STEP]      + ", "  + \
                dat[MON_TYPE.ROW_COUNT] + ", "  + \
                dat[MON_TYPE.WIDTH]     + ", "  + \
            "'"+dat[MON_TYPE.COLOR]     + "', " + \
                dat[MON_TYPE.ENABLED]   + ", "  + \
            "'"+dat[MON_TYPE.DESCRIPT]  + "', " + \
            "'"+dat[MON_TYPE.REFRESH]   + "' "  + \
        ")"

    # добавить MON_TYPE title_name
    dat = {
        MON_TYPE.WORKER:    MON_TYPE.WORKER_STANDART,
        MON_TYPE.SORT:      MON_TYPE.SORT_AUTO,
        MON_TYPE.TITLE:     monTypeControlNamTitle(nam),
        MON_TYPE.HANDLER:   MON_TYPE.HANDLER_GROUP,
        MON_TYPE.PARAM_1:   ARC.TITLE_NAME,
        MON_TYPE.PARAM_2:   MON_TYPE.PARAM_2_ALL,
        MON_TYPE.PARAM_3:   monTypeControlValTitle(val),
        MON_TYPE.NOD:       '0',
        MON_TYPE.STEP:      '1440',                      # за сутки
        MON_TYPE.ROW_COUNT: '50',
        MON_TYPE.WIDTH:     '600',
        MON_TYPE.COLOR:     MON_TYPE.COLOR_NAVY,
        MON_TYPE.ENABLED:   '1',
        MON_TYPE.DESCRIPT:  descript,
        MON_TYPE.REFRESH:   sqlDateTime(tsNow()),
    }
    idTitle = monTypeControlGetID(dat[MON_TYPE.TITLE])
    if idTitle == '-1':
        fun.funBD.bdSQL(setSQL(dat), True, False)
        idTitle = monTypeControlGetID(dat[MON_TYPE.TITLE])

    # добавить MON_TYPE content
    dat[MON_TYPE.TITLE]   = monTypeControlNamContent(nam)
    dat[MON_TYPE.PARAM_1] = ARC.CONTENT
    dat[MON_TYPE.PARAM_3] = monTypeControlValContent(val)
    dat[MON_TYPE.COLOR]   = MON_TYPE.COLOR_BLUE
    idContent = monTypeControlGetID(dat[MON_TYPE.TITLE])
    if idContent == '-1':
        fun.funBD.bdSQL(setSQL(dat), True, False)
        idContent = monTypeControlGetID(dat[MON_TYPE.TITLE])

    return idTitle, idContent



#===========================================================================================
# MON_TYPE CONTROL: удалить запись-контроль
#===========================================================================================
def monTypeControlDel(nam):
    setSQL = lambda id: \
        "DELETE " + \
        "FROM "   + MON_TYPE.TABLE + " " + \
        "WHERE "  + MON_TYPE.ID    + "=" + id

    idTitle   = monTypeControlGetID(monTypeControlNamTitle  (nam))
    idContent = monTypeControlGetID(monTypeControlNamContent(nam))

    fun.funBD.bdSQL(setSQL(idTitle  ), True, False)
    fun.funBD.bdSQL(setSQL(idContent), True, False)



#===========================================================================================
# MON_TYPE CONTROL: получить id записи-контроля
#===========================================================================================
def monTypeControlGetID(title_name):
    sql = \
        "SELECT " + MON_TYPE.ID    + " " + \
        "FROM "   + MON_TYPE.TABLE + " " + \
        "WHERE "  + \
            MON_TYPE.TITLE   + "='"  + title_name + "' AND " + \
            MON_TYPE.ENABLED + "=1 " + \
        "LIMIT 1"
    rec = fun.funBD.bdSQL(sql, True, True)
    return str(rec[0][0] if len(rec) > 0 else -1)



#===========================================================================================
# MON_TYPE CONTROL: существует ли запись
#===========================================================================================
def monTypeControlVerify(nam):
    return \
        (monTypeControlGetID(monTypeControlNamTitle(nam))   != '-1') or \
        (monTypeControlGetID(monTypeControlNamContent(nam)) != '-1')





# установить готовность мониторинга id
def monReadySet(id, status, dbBD=-1):
    if status == "1": dop = ", "+MON_TYPE.DATE+"="+str(tsNow())+" "
    else:             dop = ""
    sql = "UPDATE IGNORE "+MON_TYPE.TABLE + " " + \
          "SET " +MON_TYPE.READY+"="+status+dop+ " " + \
          "WHERE "+MON_TYPE.ID   +"="+id
    fun.funBD.bdSQL(sql, True, False, dbBD)


# прочитать готовность мониторинга id
# без ожидания при ошибке
def monReadyGet(id, dbBD=-1):
    ret = False
    sql = "SELECT "+MON_TYPE.READY+" "+ \
          "FROM "  +MON_TYPE.TABLE+" "+ \
          "WHERE " +MON_TYPE.ID+"="+id
    v = fun.funBD.bdSQL(sql, False, True, dbBD)
    if len(v) == 1: ret = (v[0][0] == 1)
    return ret


# прочитать данные о мониторинге id
# без ожидания при ошибке
# id - str
# id='-1' - читать все
def monTypeRead(id, dbBD=-1):
    sql = \
        "SELECT "+ \
            MON_TYPE.ID+", "   + \
            MON_TYPE.HANDLER   +", "+ \
            MON_TYPE.PARAM_1   +", "+ \
            MON_TYPE.PARAM_2   +", "+ \
            MON_TYPE.TITLE     +", "+ \
            MON_TYPE.STEP      +", "+ \
            MON_TYPE.ROW_COUNT +", "+ \
            MON_TYPE.WIDTH     +", "+ \
            MON_TYPE.COLOR     +", "+ \
            MON_TYPE.DATE      +", "+ \
            MON_TYPE.DESCRIPT  +" "+ \
        "FROM "+MON_TYPE.TABLE +" "+ \
        "WHERE "+ \
            MON_TYPE.ENABLED+"=1 "+ \
            (("AND "+MON_TYPE.ID+"="+id+" ") if id != '-1' else "")+ \
        "ORDER BY "+ \
            MON_TYPE.SORT+" ASC, "+ \
            MON_TYPE.TITLE+" ASC, "+ \
            MON_TYPE.STEP+" ASC"

    ret = []
    for rec in fun.funBD.bdSQL(sql, False, True, dbBD):
        ret.append({
            MON_TYPE.ID:        rec[0],
            MON_TYPE.HANDLER:   rec[1],
            MON_TYPE.PARAM_1:   rec[2],
            MON_TYPE.PARAM_2:   rec[3],
            MON_TYPE.TITLE:     rec[4],
            MON_TYPE.STEP:      rec[5],
            MON_TYPE.ROW_COUNT: rec[6],
            MON_TYPE.WIDTH:     rec[7],
            MON_TYPE.COLOR:     rec[8],
            MON_TYPE.DATE:      rec[9],
            MON_TYPE.DESCRIPT:  rec[10],
        })
    return ret




################################################################################
#   РАБОТА С ATLAS.MON
################################################################################
def monAdd(type_id, dat, host, nam, val='', url='', born='0', dbBD=-1):
    sql = "INSERT IGNORE INTO " + \
            MON.TABLE   + " ("  + \
                MON.MON_TYPE_ID + ", " + \
                MON.DATE        + ", " + \
                MON.HOST        + ", " + \
                MON.NAM         + ", " + \
                MON.VAL         + ", " + \
                MON.URL         + ", " + \
                MON.BORN        + ") " + \
          "VALUES ("+ \
                type_id + ", "  + \
                dat     + ", "  + \
                "'"+ host + "', " + \
                "'"+ nam  + "', " + \
                "'"+ val  + "', " + \
                "'"+ url  + "', " + \
                born+ ")"
    fun.funBD.bdSQL(sql, True, False, dbBD)


# удаление ВСЕХ записей мониторинга
def monDel(type_id, dbBD=-1):
    sql = "DELETE "+ \
          "FROM "  +MON.TABLE+" "+ \
          "WHERE " +MON.MON_TYPE_ID +"="+type_id
    fun.funBD.bdSQL(sql, True, False, dbBD)


# удаление старых записей до количества MON_TYPE.ROW_COUNT
def monClear(type_id, dbBD=-1):
    ID = str(type_id)
    sql = \
        'SELECT '+MON_TYPE.ROW_COUNT+' INTO @REC_MAX FROM '+MON_TYPE.TABLE+' WHERE '+MON_TYPE.ID+'='+ID+'; '+ \
        'SELECT COUNT(*) INTO @REC_ALL FROM '+MON.TABLE+' WHERE '+MON.MON_TYPE_ID+'='+ID+'; '+ \
        'set @REC_DEL = @REC_ALL - @REC_MAX; '+ \
        'set @REC_DEL = IF(@REC_DEL>0, @REC_DEL, 0); '+ \
        'PREPARE q FROM "DELETE FROM '+MON.TABLE+' WHERE '+MON.MON_TYPE_ID+'='+ID+' ORDER BY '+MON.DATE+' ASC LIMIT ?;"; '+ \
        'EXECUTE q USING @REC_DEL; '+ \
        'DEALLOCATE PREPARE q;'
    fun.funBD.bdSQL(sql, True, False, dbBD)


# без ожидания при ошибке
# return [{'host': 'local', 'dat': 1531322290, 'val': [1], 'nam': 'Анализ ...', 'url': '...', 'born': 0}, ...]
def monRead(type_id, dbBD=-1):
    sql = "SELECT "+ \
            MON.DATE+", "+ \
            MON.HOST+", "+ \
            MON.NAM+", "+ \
            MON.VAL+", "+ \
            MON.URL+", "+ \
            MON.BORN+" "+ \
          "FROM " +MON.TABLE+" "+ \
          "WHERE "+MON.MON_TYPE_ID+"="+type_id
    ret = []
    for rec in fun.funBD.bdSQL(sql, False, True, dbBD):
        ret.append({
            MON.DATE:   rec[0],
            MON.HOST:   rec[1],
            MON.NAM:    rec[2],
            MON.VAL:    list(map(int, rec[3].split(", "))) if rec[3] not in ['', None] else [],
            MON.URL:    rec[4],
            MON.BORN:   rec[5],
        })
    return ret


################################################################################
#   CОДЕРЖИТ ЛИ text хоть один объект интереса
################################################################################
def monNamNod(text, db=-1):
    return (text != fun.funSphinx.sphinxSnippetsNod(text, db))

#print('!', monNamNod('Сегодня Лебяжий сказал о выборах'))


################################################################################
#   Сформировать содержимое для MON.NAM
################################################################################
def monNamNormal(text):
    return textCutDots(textWithoutObj(text), 150)



################################################################################
#   СОРТИРОВКА РЕЗУЛЬТАТОВ МОНИТОРИНГА (методом пузырька)
################################################################################
#   встроенные функции нельзя использовать, т.к. разные направления сортировки разных полей
################################################################################
def monSort(data, cmp):
    ret = copy.deepcopy(data)
    if len(data) > 0:
        for i in range(len(ret), 0, -1):
            for j in range(1, i):
                if cmp(ret[j-1], ret[j]): ret[j-1], ret[j] = ret[j], ret[j-1]
    return ret

def monSortStatAbsolute(a, b):
    ret = (a[MON.VAL][0] < b[MON.VAL][0])                                   # по значению
    if (a[MON.VAL][0] == b[MON.VAL][0]): ret = (a[MON.NAM] > b[MON.NAM])    # по имени
    return ret

def monSortDynAbsolute(a, b):
    if (len(a[MON.VAL]) <= 1) | (len(b[MON.VAL]) <= 1):
        ret = False
        return
    aa = a[MON.VAL][0]-a[MON.VAL][1]
    bb = b[MON.VAL][0]-b[MON.VAL][1]
    ret = (aa < bb)                                                         # по значению
    if (aa == bb): ret = (a[MON.NAM] > b[MON.NAM])                          # по имени
    return ret

def monSortDynPercent(a, b):
    if (len(a[MON.VAL]) <= 1) | (len(b[MON.VAL]) <= 1):
        ret = False
        return
    aa = 100-(a[MON.VAL][1]*100/a[MON.VAL][0]) if (a[MON.VAL][0]!=0) else (999999999+a[MON.VAL][1])
    bb = 100-(b[MON.VAL][1]*100/b[MON.VAL][0]) if (b[MON.VAL][0]!=0) else (999999999+b[MON.VAL][1])
    ret = (aa < bb)                                                         # по значению
    if (aa == bb): ret = (a[MON.NAM] > b[MON.NAM])                          # по имени
    return ret





################################################################################
#   РАБОТА С ДАННЫМИ МОНИТОРИНГОВ
################################################################################
# только новые записи
def monDataFresh(data, hours):
    ret = []
    for rec in data:
        if (tsNow()-rec[MON.BORN]) <= (hours*60*60): ret.append(rec)
    return ret

# только рост (в k раз)
def monDataRise(data, k=1):
    ret = []
    for rec in data:
        if len(rec[MON.VAL]) <= 1: continue
        if rec[MON.VAL][0] > (rec[MON.VAL][1] * k): ret.append(rec)
    return ret

# только с абсолютным последним значением не ниже minVal
def monDataMin(data, minVal=1):
    ret = []
    for rec in data:
        if rec[MON.VAL][0] >= minVal: ret.append(rec)
    return ret

# обрезает число записей до top
def monDataTop(data, top):
    return data[0:top]

# добавляет points баллов каждой записи
# nam = [rating, [MON.DATE, MON.NAM, ... ]]
def monDataRating(rating, data, points=1):
    for i in range(len(data)):
        nam = data[i][MON.NAM]
        val = rating.get(nam, [0, []])
        ratingNew = val[0] + points
        ratingDat = val[1] if val[1] != [] else [   # должно совпадать с monRead
                data[i][MON.DATE],
                data[i][MON.NAM],
                data[i][MON.VAL],
                data[i][MON.URL],
                data[i][MON.BORN]
            ]
        rating[nam] = [ ratingNew, ratingDat ]
    return rating
