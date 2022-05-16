# -*- coding: utf-8 -*-

import threading, time
from lib.funConst import REL
from lib.funSys   import Queue, logger, logError, sqlDate, tsNow, getMD5
from lib.funBD    import bdConnect, bdDisconnect, bdSQL


#####################################################
# ФОНОВАЯ ЗАПИСЬ ОЧЕРЕДИ В REL
#####################################################
# maxRecQueue - максимальное количество записей в Queue
# maxRecSQL   - максимальное количество записей в SQL
#####################################################
class RelWriter():
    def __init__(self, maxRecQueue=25000, maxRecSQL=25000):
        self.queue     = Queue(maxRecQueue)
        self.isStop    = False
        self.thread    = RelWriterThread(self.queue, maxRecSQL)
        self.thread.start()

    def recAdd(self, rec):
        # окончательная обработка
        rec[REL.CRC]     = getMD5(rec[REL.TO_HOST]+rec[REL.TO_ID]+rec[REL.FROM_HOST]+rec[REL.FROM_ID]+rec[REL.TYPE]+rec[REL.HOST]+rec[REL.OBJECT])
        rec[REL.REFRESH] = sqlDate(tsNow())

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


class RelWriterThread(threading.Thread):

    def __init__(self, queue, maxRecSQL):
        threading.Thread.__init__(self)
        self.queue     = queue
        self.maxRecSQL = maxRecSQL
        self.isStop    = False
        self.isSQLExec = False


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

                # инициализация запроса
                sql = self.__sqlTitle()

                # читаем из очереди не больше self.maxRecSQL записей
                sqlCount = 0
                while (not self.queue.isEmpty()) and (sqlCount < self.maxRecSQL):
                    sqlCount += 1
                    rec =  self.queue.pop()
                    sql += self.__sqlValue(rec)+', '
                sql = sql[0:-2]+';'

                # пишем в базу
                bdSQL(sql, True, False, bd)
                logger.debug(str(sqlCount)+' record from '+str(round(time.time() - t, 3))+' s.')
            except Exception as e:
                logError(e, sql)
            finally:
                self.isSQLExec = False
        bdDisconnect(bd)

    def stop(self):
        self.isStop = True


    #===========================================================================================
    def __sqlTitle(self):
        return \
            'INSERT IGNORE INTO '    + \
                REL.TABLE     + ' (' + \
                REL.CRC       + ', ' + \
                REL.TO_HOST   + ', ' + \
                REL.TO_ID     + ', ' + \
                REL.FROM_HOST + ', ' + \
                REL.FROM_ID   + ', ' + \
                REL.TYPE      + ', ' + \
                REL.HOST      + ', ' + \
                REL.OBJECT    + ', ' + \
                REL.SOURCE    + ', ' + \
                REL.REFRESH   + ') ' + \
            'VALUES '

    def __sqlValue(self, rec):
        return \
            "("+ \
            "'"+rec[REL.CRC]      +"', "+ \
            "'"+rec[REL.TO_HOST]  +"', "+ \
            "'"+rec[REL.TO_ID]    +"', "+ \
            "'"+rec[REL.FROM_HOST]+"', "+ \
            "'"+rec[REL.FROM_ID]  +"', "+ \
            "'"+rec[REL.TYPE]     +"', "+ \
            "'"+rec[REL.HOST]     +"', "+ \
            "'"+rec[REL.OBJECT]   +"', "+ \
            "'"+rec[REL.SOURCE]   +"', "+ \
            "'"+rec[REL.REFRESH]  +"')"
