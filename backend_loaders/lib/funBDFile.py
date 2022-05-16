# -*- coding: utf-8 -*-

import threading, os, time
from lib.funConst import FILE, HOST
from lib.funSys   import Queue, logger, logError, sqlDateTime, tsNow
from lib.funFile  import filePrefAdd
from lib.funBD    import bdConnect, bdDisconnect, bdSQL


#####################################################
# ФОНОВАЯ ЗАПИСЬ ОЧЕРЕДИ В FILE
#####################################################
# maxRecQueue - максимальное количество записей в Queue
# maxRecSQL   - максимальное количество записей в SQL
#####################################################
class FileWriter():
    def __init__(self, maxRecQueue=25000, maxRecSQL=25000):
        self.queue     = Queue(maxRecQueue)
        self.isStop    = False
        self.thread    = FileWriterThread(self.queue, maxRecSQL)
        self.thread.start()

    # !!! если указан source - загрузить, иначе просто зарегистрировать !!!
    def recAdd(self, path, source='', host=HOST.LOCAL, arc_crc='', unit_id=''):
        # окончательная обработка
        if unit_id=='':
            val = os.path.split(path)
            if len(val)>=2:
                val = val[0]                            # выделить путь
                val = val.split('/')
                if len(val)>=2: unit_id = val[1]        # выделить unit_id из пути
        rec = {}
        rec[FILE.PATH]    = filePrefAdd(path)
        rec[FILE.SOURCE]  = source
        rec[FILE.HOST]    = host
        rec[FILE.ARC_CRC] = arc_crc
        rec[FILE.UNIT_ID] = unit_id
        rec[FILE.ACTION]  = str(FILE.ACTION_LOAD) if source != '' else str(FILE.ACTION_NONE)
        rec[FILE.REFRESH] = sqlDateTime(tsNow())

        # ждем место в очереди
        isFull = self.queue.isFull()
        if isFull: t = time.time()
        while self.queue.isFull(): time.sleep(1)
        if isFull: logger.warning("Waited for a place in overflow queue: "+str(int(time.time() - t))+' s.')

        # помещаем в очередь
        self.queue.push(rec)

        rec = None

    def isEmpty(self):
        return self.queue.isEmpty() and (not self.thread.isSQLExec)

    def waitEmpty(self):
        if not self.isEmpty(): logger.info("Wait from write queue ("+str(self.queue.size())+") ...")
        while not self.isEmpty(): time.sleep(.2)

    def stop(self, isWait):
        if isWait: self.waitEmpty()
        self.thread.stop()
        self.thread.join()


class FileWriterThread(threading.Thread):

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
    # FILE.DESCRIPT - по умолчанию
    #===========================================================================================
    def __sqlTitle(self):
        return \
            'INSERT IGNORE INTO '     + \
                FILE.TABLE     + ' (' + \
                FILE.PATH      + ', ' + \
                FILE.SOURCE    + ', ' + \
                FILE.HOST      + ', ' + \
                FILE.ARC_CRC   + ', ' + \
                FILE.UNIT_ID   + ', ' + \
                FILE.ACTION    + ', ' + \
                FILE.REFRESH   + ') ' + \
            'VALUES '

    def __sqlValue(self, rec):
        try:
            ret = \
            "("+ \
            "'"+rec[FILE.PATH]   +"', "+ \
            "'"+rec[FILE.SOURCE] +"', "+ \
            "'"+rec[FILE.HOST]   +"', "+ \
            "'"+rec[FILE.ARC_CRC]+"', "+ \
            "'"+rec[FILE.UNIT_ID]+"', "+ \
            "'"+rec[FILE.ACTION] +"', "+ \
            "'"+rec[FILE.REFRESH]+"')"
            return ret
        except Exception as e:
            logger.error(rec)
            raise



#####################################################
# ПОЛУЧИТЬ СПИСОК ЗАПИСЕЙ С ACTION
#####################################################
class FileRecGetList:
    PATH   = 0
    SOURCE = 1

    def fun(action):
        sql = "SELECT "+FILE.PATH+", "+FILE.SOURCE+" "+ \
              "FROM "  +FILE.TABLE+" "+ \
              "WHERE ("+FILE.ACTION+"="+str(action)+");"
        return bdSQL(sql, True, True)


#####################################################
# УСТАНОВИТЬ ПРИЗНАК ACTION
#####################################################
def fileRecSetAction(path, action):
    sql = "UPDATE IGNORE "+FILE.TABLE+" "+ \
          "SET "  +FILE.ACTION+"=" +str(action)+" "+ \
          "WHERE "+FILE.PATH  +"='"+path+"';"
    bdSQL(sql, True, False)


#####################################################
# ДОБАВИТЬ ЗАПИСЬ С НЕМЕДЛЕННЫМ ПОМЕЩЕНИЕМ В БД
#####################################################
# файл должен существовать в структууре проекта
# для выкачки из Интернета использовать FileWriter
#####################################################
def fileRecAdd(path, source='', host=HOST.LOCAL, arc_crc='', unit_id='', action=str(FILE.ACTION_NONE), descript=''):
    sql = \
        'INSERT IGNORE INTO '     + \
            FILE.TABLE     + ' (' + \
            FILE.PATH      + ', ' + \
            FILE.SOURCE    + ', ' + \
            FILE.HOST      + ', ' + \
            FILE.ARC_CRC   + ', ' + \
            FILE.UNIT_ID   + ', ' + \
            FILE.ACTION    + ', ' + \
            FILE.DESCRIPT  + ', ' + \
            FILE.REFRESH   + ') ' + \
        'VALUES (' + \
            "'"+path                  +"', "+ \
            "'"+source                +"', "+ \
            "'"+host                  +"', "+ \
            "'"+arc_crc               +"', "+ \
            "'"+unit_id               +"', "+ \
            "'"+action                +"', "+ \
            "'"+descript              +"', "+ \
            "'"+sqlDateTime(tsNow())  +"')"
    bdSQL(sql, True, False)


#####################################################
# УДАЛИТЬ ЗАПИСЬ
#####################################################
def fileRecDel(path):
    sql = "DELETE FROM "+FILE.TABLE+" "+ \
          "WHERE "+FILE.PATH  +"='"+path+"';"
    bdSQL(sql, True, False)
