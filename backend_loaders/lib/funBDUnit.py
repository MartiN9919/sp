# -*- coding: utf-8 -*-

import threading, time
from lib.funConst import UNIT
from lib.funSys   import Queue, logger, sqlDateTime, tsNow, getMD5
from lib.funBD    import bdConnect, bdDisconnect, bdSQL



#####################################################
# ФОНОВАЯ ЗАПИСЬ ОЧЕРЕДИ В UNIT И UNIT_DYNAMIC_MAIN
#####################################################
# maxRecQueue     - максимальное количество записей в Queue
# maxRecSQL       - максимальное количество записей в SQL
# isStaticInsert  - добавлять записи в UNIT
# isStaticUpdate  - обновлять записи в UNIT
# isDynamicInsert - добавлять записи в UNIT_DYNAMIC_MAIN
#####################################################
class UnitWriter():
    def __init__(self, maxRecQueue=10000, maxRecSQL=1000, isStaticInsert=True, isStaticUpdate=True, isDynamicInsert=True):
        self.queue     = Queue(maxRecQueue)
        self.isStop    = False
        self.thread    = UnitWriterThread(self.queue, maxRecSQL, isStaticInsert, isStaticUpdate, isDynamicInsert)
        self.thread.start()

    #def recIni(self):
    #    rec                         = {}
    #    rec[UNIT.HOST]              = ''
    #    rec[UNIT.ID]                = ''
    #    rec[UNIT.SOURCE]            = ''
    #    rec[UNIT.NAME]              = ''
    #    rec[UNIT.BDATE]             = ''
    #    rec[UNIT.RDATE]             = ''
    #    rec[UNIT.COUNTRY]           = ''
    #    rec[UNIT.CITY]              = ''
    #    rec[UNIT.INFO]              = ''
    #    rec[UNIT.DESCRIPT]          = ''
    #    rec[UNIT.VISIT_DATE]        = ''
    #    rec[UNIT.VISIT_DEVICE]      = '0'
    #    #rec[UNIT.REFRESH]          = ''
    #    #rec[UNIT.CRC_DYNAMIC_MAIN] = ''
    #    return rec

    def recAdd(self, rec):
        # окончательная обработка
        rec[UNIT.REFRESH]          = sqlDateTime(tsNow())
        rec[UNIT.CRC_DYNAMIC_MAIN] = getMD5(rec[UNIT.HOST]+rec[UNIT.ID]+rec[UNIT.NAME]+rec[UNIT.VISIT_DATE]+rec[UNIT.VISIT_DEVICE])

        # ждем место в очереди
        isFull = self.queue.isFull()
        if isFull: t = time.time()
        while self.queue.isFull(): time.sleep(1)
        if isFull: logger.warning("Waited for a place in overflow queue: "+str(int(time.time() - t))+' s.')

        # помещаем в очередь
        self.queue.push(rec)

    def isEmpty(self):
        return self.queue.isEmpty() and (not self.thread.isSQLExec)

    def waitEmpty(self):
        if not self.isEmpty(): logger.info("Wait from write queue ("+str(self.queue.size())+") ...")
        while not self.isEmpty(): time.sleep(.2)

    def stop(self, isWait):
        if isWait: self.waitEmpty()
        self.thread.stop()
        self.thread.join()


class UnitWriterThread(threading.Thread):

    def __init__(self, queue, maxRecSQL, isStaticInsert, isStaticUpdate, isDynamicInsert):
        threading.Thread.__init__(self)
        self.queue           = queue
        self.maxRecSQL       = maxRecSQL
        self.isStaticInsert  = isStaticInsert
        self.isStaticUpdate  = isStaticUpdate
        self.isDynamicInsert = isDynamicInsert
        self.isStop          = False
        self.isSQLExec       = False


    def run(self):
        bd = bdConnect()
        while True:
            if self.isStop: break
            try:
                # ждем записи
                time.sleep(5)
                if self.queue.isEmpty(): continue
                self.isSQLExec = True
                t = time.time()

                # инициализация запросов
                sql = ''
                sqlStaticInsert  = self.__sqlStaticInsertTitle()  if self.isStaticInsert  else ''
                sqlStaticUpdate  = ''                             if self.isStaticUpdate  else ''
                sqlDynamicInsert = self.__sqlDynamicInsertTitle() if self.isDynamicInsert else ''

                # читаем из очереди не больше self.maxRecSQL записей
                sqlCount = 0
                while (not self.queue.isEmpty()) and (sqlCount < self.maxRecSQL):
                    sqlCount += 1

                    rec = self.queue.pop()
                    if self.isStaticInsert:  sqlStaticInsert  += self.__sqlStaticInsertValue(rec)+', '
                    if self.isStaticUpdate:  sqlStaticUpdate  += self.__sqlStaticUpdate(rec)+' '
                    if self.isDynamicInsert: sqlDynamicInsert += self.__sqlDynamicInsertValue(rec)+', '

                if self.isStaticInsert:  sqlStaticInsert  = sqlStaticInsert [0:-2]+';'
                if self.isDynamicInsert: sqlDynamicInsert = sqlDynamicInsert[0:-2]+';'

                sql = ((sqlStaticUpdate +' ') if self.isStaticUpdate  else '')+ \
                      ((sqlStaticInsert +' ') if self.isStaticInsert  else '')+ \
                      ((sqlDynamicInsert+' ') if self.isDynamicInsert else '')
                bdSQL(sql, True, False, bd)
                logger.debug(str(sqlCount)+' record from '+str(round(time.time() - t, 3))+' s.')
            except Exception as e:
                logger.error(str(e))
            finally:
                self.isSQLExec = False
        bdDisconnect(bd)

    def stop(self):
        self.isStop = True


    #===========================================================================================
    # REPLACE нельзя, так как удалится DESCRIPT
    #===========================================================================================
    def __sqlStaticInsertTitle(self):
        return \
            'INSERT IGNORE INTO ' + \
                UNIT.TABLE       + ' (' + \
                UNIT.HOST        + ', ' + \
                UNIT.ID          + ', ' + \
                UNIT.SOURCE      + ', ' + \
                UNIT.NAME        + ', ' + \
                UNIT.BDATE       + ', ' + \
                UNIT.RDATE       + ', ' + \
                UNIT.COUNTRY     + ', ' + \
                UNIT.CITY        + ', ' + \
                UNIT.INFO        + ', ' + \
                UNIT.DESCRIPT    + ', ' + \
                UNIT.REFRESH     + ') ' + \
            'VALUES '

    def __sqlStaticInsertValue(self, rec):
        return \
            "("+ \
            "'"+rec[UNIT.HOST]     + "', "+ \
            "'"+rec[UNIT.ID]       + "', "+ \
            "'"+rec[UNIT.SOURCE]   + "', "+ \
            "'"+rec[UNIT.NAME]     + "', "+ \
            "'"+rec[UNIT.BDATE]    + "', "+ \
            "'"+rec[UNIT.RDATE]    + "', "+ \
            "'"+rec[UNIT.COUNTRY]  + "', "+ \
            "'"+rec[UNIT.CITY]     + "', "+ \
            "'"+rec[UNIT.INFO]     + "', "+ \
            "'"+rec[UNIT.DESCRIPT] + "', "+ \
            "'"+rec[UNIT.REFRESH]  + "')"


    #===========================================================================================
    def __sqlStaticUpdate(self, rec):
        return \
            "UPDATE IGNORE " + \
                UNIT.TABLE + " " + \
            "SET " + \
                UNIT.SOURCE   + "='" + rec[UNIT.SOURCE]  + "', " + \
                UNIT.NAME     + "='" + rec[UNIT.NAME]    + "', " + \
                UNIT.COUNTRY  + "='" + rec[UNIT.COUNTRY] + "', " + \
                UNIT.CITY     + "='" + rec[UNIT.CITY]    + "', " + \
                UNIT.INFO     + "='" + rec[UNIT.INFO]    + "', " + \
                UNIT.REFRESH  + "='" + rec[UNIT.REFRESH] + "' "  + \
            "WHERE " + \
                "("+UNIT.HOST + "='" + rec[UNIT.HOST]    + "') AND "+ \
                "("+UNIT.ID   + "='" + rec[UNIT.ID]      + "');"


    #===========================================================================================
    def __sqlDynamicInsertTitle(self):
        return \
            'INSERT IGNORE INTO ' + \
                UNIT.TABLE_DYNAMIC_MAIN + ' (' + \
                UNIT.CRC_DYNAMIC_MAIN   + ', ' + \
                UNIT.HOST               + ', ' + \
                UNIT.ID                 + ', ' + \
                UNIT.REFRESH            + ', ' + \
                UNIT.NAME               + ', ' + \
                UNIT.VISIT_DATE         + ', ' + \
                UNIT.VISIT_DEVICE       + ') ' + \
            'VALUES '


    def __sqlDynamicInsertValue(self, rec):
        return \
            "("+ \
            "'"+rec[UNIT.CRC_DYNAMIC_MAIN] + "', "+ \
            "'"+rec[UNIT.HOST]             + "', "+ \
            "'"+rec[UNIT.ID]               + "', "+ \
            "'"+rec[UNIT.REFRESH]          + "', "+ \
            "'"+rec[UNIT.NAME]             + "', "+ \
            "'"+rec[UNIT.VISIT_DATE]       + "', "+ \
                rec[UNIT.VISIT_DEVICE]     + ")"



#===========================================================================================
# ПРОЧИТАТЬ ПОЛЯ fieldList=[поле1, поле2, ...] ДЛЯ HOST И ID
#===========================================================================================
def getUnitField(host, id, fieldList, dbBD=-1):
    sql = \
        "SELECT "+', '.join(fieldList)+" "+ \
        "FROM " +UNIT.TABLE+" "+ \
        "WHERE "+UNIT.HOST+"='"+host+"' AND "+UNIT.ID+"='"+str(id)+"' "+ \
        "LIMIT 1;"
    ret = []
    for rec in bdSQL(sql, True, True, dbBD):
        val = {}
        for ind, item in enumerate(rec): val[fieldList[ind]] = item
        ret.append(val)
    return ret
