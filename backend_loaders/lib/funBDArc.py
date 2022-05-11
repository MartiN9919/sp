# -*- coding: utf-8 -*-

import threading, time
from lib.funConst import ARC, ARC_DYNAMIC, MSG
from lib.funSys   import Queue, logger, sqlDateTime, tsNow, getMD5
from lib.funBD    import bdConnect, bdDisconnect, bdSQL
#from lib.funEmo   import emo



#####################################################
# ФОНОВАЯ ЗАПИСЬ ОЧЕРЕДИ В ARC И ARC_DYNAMIC
#####################################################
# maxRecQueue     - максимальное количество записей в Queue
# maxRecSQL       - максимальное количество записей в SQL
# isStaticInsert  - добавлять записи в ARC
# isStaticUpdate  - обновлять записи в ARC
# isDynamicInsert - добавлять записи в ARC_DYNAMIC
#####################################################
class ArcWriter():
    def __init__(self, maxRecQueue=10000, maxRecSQL=1000, isStaticInsert=True, isStaticUpdate=True, isDynamicInsert=True):
        self.queue     = Queue(maxRecQueue)
        self.isStop    = False
        self.thread    = ArcWriterThread(self.queue, maxRecSQL, isStaticInsert, isStaticUpdate, isDynamicInsert)
        self.thread.start()

    def recIni(self):
        rec                      = {}
        rec[ARC.CRC_REL]         = ''
        rec[ARC.TYPE]            = ARC.TYPE_SOCIAL
        rec[ARC.DATE]            = ''
        rec[ARC.HOST]            = ''
        rec[ARC.SOURCE]          = ''
        rec[ARC.GROUP_ID]        = ''
        rec[ARC.TITLE_ID]        = ''
        rec[ARC.TITLE_NAME]      = ''
        rec[ARC.CONTENT]         = ''
        rec[ARC.AUTHOR_ID]       = ''
        rec[ARC.AUTHOR_NAME]     = ''
        rec[ARC.COUNTRY]         = ''
        rec[ARC.EMOTION]         = '0'
        rec[ARC_DYNAMIC.VIEW_NOW]= '0'
        rec[ARC.VIEW_ALL]        = '0'
        rec[ARC.LIKE_YES]        = '0'
        rec[ARC.LIKE_NO]         = '0'
        rec[ARC.REPOST]          = '0'
        #rec[ARC.DEL]            = '0'
        #rec[ARC.REFRESH]        = ''
        #rec[ARC.CRC]            = ''
        #rec[ARC_DYNAMIC.TABLE+'.'+ARC_DYNAMIC.CRC] = ''
        return rec

    def recAdd(self, rec):
        # окончательная обработка
        if not rec[ARC_DYNAMIC.VIEW_NOW].isdigit(): rec[ARC_DYNAMIC.VIEW_NOW] = '0'
        if not rec[ARC.VIEW_ALL        ].isdigit(): rec[ARC.VIEW_ALL        ] = '0'
        if not rec[ARC.LIKE_YES        ].isdigit(): rec[ARC.LIKE_YES        ] = '0'
        if not rec[ARC.LIKE_NO         ].isdigit(): rec[ARC.LIKE_NO         ] = '0'
        if not rec[ARC.REPOST          ].isdigit(): rec[ARC.REPOST          ] = '0'

        if rec[ARC.CONTENT]  == '': rec[ARC.CONTENT] = MSG.NO_TEXT
        #rec[ARC.EMOTION]     = str(emo(rec[ARC.TITLE_NAME]+' '+rec[ARC.CONTENT]))
        rec[ARC.DEL]         = '0'
        rec[ARC.REFRESH]     = sqlDateTime(tsNow())
        rec[ARC.CRC]         = getMD5(rec[ARC.HOST]+rec[ARC.GROUP_ID]+rec[ARC.TITLE_ID]+rec[ARC.AUTHOR_ID]+rec[ARC.CONTENT])
        # !!! (ARC.CRC == ARC_DYNAMIC.CRC) ==> ARC_DYNAMIC.TABLE+'.'+ARC_DYNAMIC.CRC
        rec[ARC_DYNAMIC.TABLE+'.'+ARC_DYNAMIC.CRC] = getMD5(rec[ARC.AUTHOR_NAME]+rec[ARC_DYNAMIC.VIEW_NOW]+rec[ARC.VIEW_ALL]+rec[ARC.LIKE_YES]+rec[ARC.LIKE_NO]+rec[ARC.REPOST])

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


class ArcWriterThread(threading.Thread):

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
                      ((sqlStaticInsert)      if self.isStaticInsert  else '')
                     #((sqlDynamicInsert+' ') if self.isDynamicInsert else '')
                bdSQL(sql, True, False, bd)
                if self.isDynamicInsert: bdSQL(sqlDynamicInsert, True, False, bd)
                logger.debug(str(sqlCount)+' record from '+str(round(time.time() - t, 3))+' s.')
            except Exception as e:
                logger.error(str(e))
            finally:
                self.isSQLExec = False
        bdDisconnect(bd)

    def stop(self):
        self.isStop = True


    #===========================================================================================
    # REPLACE ведет к сбросу признака indmain ==> ??? протестировать на предмет дубликатов
    #===========================================================================================
    def __sqlStaticInsertTitle(self):
        return \
            'INSERT IGNORE INTO ' + \
                ARC.TABLE       + ' (' + \
                ARC.CRC         + ', ' + \
                ARC.CRC_REL     + ', ' + \
                ARC.TYPE        + ', ' + \
                ARC.DATE        + ', ' + \
                ARC.HOST        + ', ' + \
                ARC.SOURCE      + ', ' + \
                ARC.GROUP_ID    + ', ' + \
                ARC.TITLE_ID    + ', ' + \
                ARC.TITLE_NAME  + ', ' + \
                ARC.CONTENT     + ', ' + \
                ARC.AUTHOR_ID   + ', ' + \
                ARC.AUTHOR_NAME + ', ' + \
                ARC.COUNTRY     + ', ' + \
                ARC.EMOTION     + ', ' + \
                ARC.VIEW_ALL    + ', ' + \
                ARC.LIKE_YES    + ', ' + \
                ARC.LIKE_NO     + ', ' + \
                ARC.REPOST      + ', ' + \
                ARC.DEL         + ', ' + \
                ARC.REFRESH     + ') ' + \
            'VALUES '

    def __sqlStaticInsertValue(self, rec):
        return \
            "("+ \
            "'"+rec[ARC.CRC]         + "', "+ \
            "'"+rec[ARC.CRC_REL]     + "', "+ \
                rec[ARC.TYPE]        + ", " + \
            "'"+rec[ARC.DATE]        + "', "+ \
            "'"+rec[ARC.HOST]        + "', "+ \
            "'"+rec[ARC.SOURCE]      + "', "+ \
            "'"+rec[ARC.GROUP_ID]    + "', "+ \
            "'"+rec[ARC.TITLE_ID]    + "', "+ \
            "'"+rec[ARC.TITLE_NAME]  + "', "+ \
            "'"+rec[ARC.CONTENT]     + "', "+ \
            "'"+rec[ARC.AUTHOR_ID]   + "', "+ \
            "'"+rec[ARC.AUTHOR_NAME] + "', "+ \
            "'"+rec[ARC.COUNTRY]     + "', "+ \
                rec[ARC.EMOTION]     + ", " + \
                rec[ARC.VIEW_ALL]    + ", " + \
                rec[ARC.LIKE_YES]    + ", " + \
                rec[ARC.LIKE_NO]     + ", " + \
                rec[ARC.REPOST]      + ", " + \
                rec[ARC.DEL]         + ", " + \
            "'"+rec[ARC.REFRESH]     + "')"


    #===========================================================================================
    def __sqlStaticUpdate(self, rec):
        return \
            "UPDATE IGNORE " + \
                ARC.TABLE + " " + \
            "SET " + \
                ((ARC.CRC_REL+ "='" + rec[ARC.CRC_REL]  + "', ") if rec[ARC.CRC_REL]!='' else '') + \
                ARC.VIEW_ALL + "="  + rec[ARC.VIEW_ALL] + ", " + \
                ARC.LIKE_YES + "="  + rec[ARC.LIKE_YES] + ", " + \
                ARC.LIKE_NO  + "="  + rec[ARC.LIKE_NO]  + ", " + \
                ARC.REPOST   + "="  + rec[ARC.REPOST]   + ", " + \
                ARC.REFRESH  + "='" + rec[ARC.REFRESH]  + "', "+ \
                ARC.DEL      + "="  + rec[ARC.DEL]      + ", " + \
                ARC.INDMAIN  + "=0 "+ \
            "WHERE " + \
                "("+ARC.DATE + "='" + rec[ARC.DATE]     + "') AND "+ \
                "("+ARC.CRC  + "='" + rec[ARC.CRC]      + "');"


    #===========================================================================================
    def __sqlDynamicInsertTitle(self):
        return \
            'INSERT IGNORE INTO ' + \
                ARC_DYNAMIC.TABLE       + ' (' + \
                ARC_DYNAMIC.CRC_ARC     + ', ' + \
                ARC_DYNAMIC.CRC         + ', ' + \
                ARC_DYNAMIC.REFRESH     + ', ' + \
                ARC_DYNAMIC.AUTHOR_NAME + ', ' + \
                ARC_DYNAMIC.VIEW_NOW    + ', ' + \
                ARC_DYNAMIC.VIEW_ALL    + ', ' + \
                ARC_DYNAMIC.LIKE_YES    + ', ' + \
                ARC_DYNAMIC.LIKE_NO     + ', ' + \
                ARC_DYNAMIC.REPOST      + ') ' + \
            'VALUES '


    def __sqlDynamicInsertValue(self, rec):
        return \
            "("+ \
            "'"+rec[ARC.CRC]     + "', "+ \
            "'"+rec[ARC_DYNAMIC.TABLE+'.'+ARC_DYNAMIC.CRC] + "', "+ \
            "'"+rec[ARC_DYNAMIC.REFRESH]                   + "', "+ \
            "'"+rec[ARC_DYNAMIC.AUTHOR_NAME] + "', "+ \
                rec[ARC_DYNAMIC.VIEW_NOW]    + ", " + \
                rec[ARC_DYNAMIC.VIEW_ALL]    + ", " + \
                rec[ARC_DYNAMIC.LIKE_YES]    + ", " + \
                rec[ARC_DYNAMIC.LIKE_NO]     + ", " + \
                rec[ARC_DYNAMIC.REPOST]      + ")"





#####################################################
# ОТМЕТИТЬ УДАЛЕННЫЕ В ИСТОЧНИКЕ ЗАПИСИ
#####################################################
# tsPeriodStart - ts начала периода
# tsScanStart   - ts начала сканирования
#####################################################
def arcMarkDel(host, tsPeriodStart, tsScanStart):
    logger.debug("Find deleted records ...")
    sql= "UPDATE "+ARC.TABLE+" "+ \
         "SET "+ARC.DEL+"=true "+ \
         "WHERE ("+ARC.HOST   +"='" +host+"') AND "+ \
               "("+ARC.DATE   +">='"+sqlDateTime(tsPeriodStart)+"') AND "+ \
               "("+ARC.REFRESH+"<'" +sqlDateTime(tsScanStart)  +"');"
    bdSQL(sql, True, False)
