# -*- coding: utf-8 -*-

import threading, time
from fun.funConst import UNIT
from fun.funSys   import Queue, logger, sqlDateTime, tsNow, getMD5
from fun.funBD    import bdConnect, bdDisconnect, bdSQL



#####################################################
# ФОНОВАЯ ЗАПИСЬ ОЧЕРЕДИ В UNIT И UNIT_DYNAMIC_REL
#####################################################
# maxRecQueue     - максимальное количество записей в Queue
# maxRecSQL       - максимальное количество записей в SQL
# isStaticUpdate  - обновлять записи в UNIT (только REL)
# isDynamicInsert - добавлять записи в UNIT_DYNAMIC_REL
#####################################################
class UnitRelWriter():
    def __init__(self, maxRecQueue=10000, maxRecSQL=1000, isStaticUpdate=True, isDynamicInsert=True):
        self.queue     = Queue(maxRecQueue)
        self.isStop    = False
        self.thread    = UnitWriterThread(self.queue, maxRecSQL, isStaticUpdate, isDynamicInsert)
        self.thread.start()

    def recIni(self):
        rec                        = {}
        rec[UNIT.HOST]             = ''
        rec[UNIT.ID]               = ''
        rec[UNIT.TO_ALL]           = '0'
        rec[UNIT.TO_RELATIV]       = '0'
        rec[UNIT.TO_ARC]           = '0'
        rec[UNIT.TO_GROUP]         = '0'
        rec[UNIT.TO_FRIEND]        = '0'
        rec[UNIT.TO_FOLLOW]        = '0'
        rec[UNIT.TO_FOLLOW_ALL]    = '0'
        rec[UNIT.TO_LIKE]          = '0'
        rec[UNIT.TO_REPOST]        = '0'
        rec[UNIT.TO_ADMIN]         = '0'
        rec[UNIT.FROM_ALL]         = '0'
        rec[UNIT.FROM_ARC]         = '0'
        rec[UNIT.FROM_GROUP]       = '0'
        rec[UNIT.FROM_FOLLOW]      = '0'
        rec[UNIT.FROM_LIKE]        = '0'
        rec[UNIT.FROM_REPOST]      = '0'
        rec[UNIT.FROM_ADMIN]       = '0'
        #rec[UNIT.REFRESH_REL]     = ''
        #rec[UNIT.CRC_DYNAMIC_REL] = ''
        return rec


    def recAdd(self, rec):
        # окончательная обработка
        rec[UNIT.REFRESH_REL]     = sqlDateTime(tsNow())
        rec[UNIT.CRC_DYNAMIC_REL] = getMD5(rec[UNIT.HOST]+rec[UNIT.ID]+rec[UNIT.TO_ALL]+rec[UNIT.FROM_ALL])

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

    def __init__(self, queue, maxRecSQL, isStaticUpdate, isDynamicInsert):
        threading.Thread.__init__(self)
        self.queue           = queue
        self.maxRecSQL       = maxRecSQL
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
                sqlStaticUpdate  = ''                             if self.isStaticUpdate  else ''
                sqlDynamicInsert = self.__sqlDynamicInsertTitle() if self.isDynamicInsert else ''

                # читаем из очереди не больше self.maxRecSQL записей
                sqlCount = 0
                while (not self.queue.isEmpty()) and (sqlCount < self.maxRecSQL):
                    sqlCount += 1

                    rec = self.queue.pop()
                    if self.isStaticUpdate:  sqlStaticUpdate  += self.__sqlStaticUpdate(rec)+' '
                    if self.isDynamicInsert: sqlDynamicInsert += self.__sqlDynamicInsertValue(rec)+', '

                if self.isDynamicInsert: sqlDynamicInsert = sqlDynamicInsert[0:-2]+';'

                sql = ((sqlStaticUpdate +' ') if self.isStaticUpdate  else '')+ \
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
    def __sqlStaticUpdate(self, rec):
        return \
            "UPDATE IGNORE " + \
                UNIT.TABLE + " " + \
            "SET " + \
                UNIT.TO_ALL        + "="  + rec[UNIT.TO_ALL]        + ", " + \
                UNIT.TO_RELATIV    + "="  + rec[UNIT.TO_RELATIV]    + ", " + \
                UNIT.TO_ARC        + "="  + rec[UNIT.TO_ARC]        + ", " + \
                UNIT.TO_GROUP      + "="  + rec[UNIT.TO_GROUP]      + ", " + \
                UNIT.TO_FRIEND     + "="  + rec[UNIT.TO_FRIEND]     + ", " + \
                UNIT.TO_FOLLOW     + "="  + rec[UNIT.TO_FOLLOW]     + ", " + \
                UNIT.TO_FOLLOW_ALL + "="  + rec[UNIT.TO_FOLLOW_ALL] + ", " + \
                UNIT.TO_LIKE       + "="  + rec[UNIT.TO_LIKE]       + ", " + \
                UNIT.TO_REPOST     + "="  + rec[UNIT.TO_REPOST]     + ", " + \
                UNIT.TO_ADMIN      + "="  + rec[UNIT.TO_ADMIN]      + ", " + \
                UNIT.FROM_ALL      + "="  + rec[UNIT.FROM_ALL]      + ", " + \
                UNIT.FROM_ARC      + "="  + rec[UNIT.FROM_ARC]      + ", " + \
                UNIT.FROM_GROUP    + "="  + rec[UNIT.FROM_GROUP]    + ", " + \
                UNIT.FROM_FOLLOW   + "="  + rec[UNIT.FROM_FOLLOW]   + ", " + \
                UNIT.FROM_LIKE     + "="  + rec[UNIT.FROM_LIKE]     + ", " + \
                UNIT.FROM_REPOST   + "="  + rec[UNIT.FROM_REPOST]   + ", " + \
                UNIT.FROM_ADMIN    + "="  + rec[UNIT.FROM_ADMIN]    + ", " + \
                UNIT.REFRESH_REL   + "='" + rec[UNIT.REFRESH_REL]   + "' " + \
            "WHERE " + \
                "("+UNIT.HOST + "='" + rec[UNIT.HOST]    + "') AND "+ \
                "("+UNIT.ID   + "='" + rec[UNIT.ID]      + "');"




    #===========================================================================================
    def __sqlDynamicInsertTitle(self):
        return \
            'INSERT IGNORE INTO ' + \
                UNIT.TABLE_DYNAMIC_REL + ' (' + \
                UNIT.CRC_DYNAMIC_REL   + ', ' + \
                UNIT.HOST              + ', ' + \
                UNIT.ID                + ', ' + \
                UNIT.REFRESH_REL       + ', ' + \
                UNIT.TO_ALL            + ', ' + \
                UNIT.TO_RELATIV        + ', ' + \
                UNIT.TO_ARC            + ', ' + \
                UNIT.TO_GROUP          + ', ' + \
                UNIT.TO_FRIEND         + ', ' + \
                UNIT.TO_FOLLOW         + ', ' + \
                UNIT.TO_FOLLOW_ALL     + ', ' + \
                UNIT.TO_LIKE           + ', ' + \
                UNIT.TO_REPOST         + ', ' + \
                UNIT.TO_ADMIN          + ', ' + \
                UNIT.FROM_ALL          + ', ' + \
                UNIT.FROM_ARC          + ', ' + \
                UNIT.FROM_GROUP        + ', ' + \
                UNIT.FROM_FOLLOW       + ', ' + \
                UNIT.FROM_LIKE         + ', ' + \
                UNIT.FROM_REPOST       + ', ' + \
                UNIT.FROM_ADMIN        + ') ' + \
            'VALUES '


    def __sqlDynamicInsertValue(self, rec):
        return \
            "("+ \
            "'"+rec[UNIT.CRC_DYNAMIC_REL] + "', "+ \
            "'"+rec[UNIT.HOST]            + "', "+ \
            "'"+rec[UNIT.ID]              + "', "+ \
            "'"+rec[UNIT.REFRESH_REL]     + "', "+ \
                rec[UNIT.TO_ALL]          + ", " + \
                rec[UNIT.TO_RELATIV]      + ", " + \
                rec[UNIT.TO_ARC]          + ", " + \
                rec[UNIT.TO_GROUP]        + ", " + \
                rec[UNIT.TO_FRIEND]       + ", " + \
                rec[UNIT.TO_FOLLOW]       + ", " + \
                rec[UNIT.TO_FOLLOW_ALL]   + ", " + \
                rec[UNIT.TO_LIKE]         + ", " + \
                rec[UNIT.TO_REPOST]       + ", " + \
                rec[UNIT.TO_ADMIN]        + ", " + \
                rec[UNIT.FROM_ALL]        + ", " + \
                rec[UNIT.FROM_ARC]        + ", " + \
                rec[UNIT.FROM_GROUP]      + ", " + \
                rec[UNIT.FROM_FOLLOW]     + ", " + \
                rec[UNIT.FROM_LIKE]       + ", " + \
                rec[UNIT.FROM_REPOST]     + ", " + \
                rec[UNIT.FROM_ADMIN]      + ")"
