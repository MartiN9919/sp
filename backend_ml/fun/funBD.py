# -*- coding: utf-8 -*-

# некоторые версии MySQLdb после выполнения db.close не полностью "убирают мусор"
# добавим вызов garbage collector
import MySQLdb, MySQLdb.cursors, gc
import time, random

import fun.funSys
from   fun.funConst import BD, NOD, VAR


###################################################################################
#  ЧИТАЕТ РЕЗУЛЬТАТЫ ЗАПРОСА ПО СТРОКАМ (ГЕНЕРАТОР)
###################################################################################
# dataOnServer=True - данные хранить на сервере - при длительных ожиданиях cursor теряет связь
###################################################################################
class BDReadLines(object):
    def __init__(self, sql, block_size=1000, dataOnServer=True):
        self.db           = bdConnect(dataOnServer=dataOnServer)
        self.sql          = sql
        self.block_size   = block_size
        self.dataOnServer = dataOnServer

    def __del__(self):
        bdDisconnect(self.db)

    def __iter__(self):
        icount = 3
        while icount>0:
            try:
                self.db.commit()
                cursor = self.db.cursor()
                cursor.execute(self.sql)
                break
            except Exception as e:
                self.db = bdReconnect(db=self.db, dataOnServer=self.dataOnServer)
                icount -= 1

        if icount==0: raise Exception('Wrong execute sql: '+self.sql)

        #for row in cursor: yield row
        while True:
            rows = cursor.fetchmany(self.block_size)
            if not rows: break
            for row in rows: yield row



    #def __len__(self):
    #    self.db.commit()                                                       # синхрон в т.ч. при изменении БД другими средствами
    #    val = bdSQL(sql='SELECT COUNT(*) as len FROM ('+self.sql+') as titer', wait=True, read=True, db=self.db)
    #    if len(val) == 0: return 0
    #    return val[0][0]



#####################################################
# КЛАСС РАБОТЫ С BD
#####################################################
class SQL_bd():
    def __init__(self, dataOnServer=False):
        self.db = bdConnect(dataOnServer=dataOnServer)

    def __del__(self):
        bdDisconnect(self.db)

    def execute(self, sql, wait=False, read=True):
        return bdSQL(sql, wait, read, self.db)


#===============================================================================
#=====   BD: УСТАНОВИТЬ / РАЗОРВАТЬ СОЕДИНЕНИЕ   ===============================
#===============================================================================
# dataOnServer - хранить результаты на сервере (для больших запросов)
#===============================================================================
def bdConnect(dataOnServer=False):
    return MySQLdb.connect(host=BD.HOST,       port=BD.PORT, user=BD.USER,
                           passwd=BD.PASSWORD, db=BD.DB,     charset=BD.CHARSET,
                           cursorclass=MySQLdb.cursors.SSCursor if dataOnServer else MySQLdb.cursors.Cursor)

def bdDisconnect(db):
    try:
        db.close()
        gc.collect()
    except Exception:
        pass


def bdReconnect(db, dataOnServer=False):
    bdDisconnect(db)
    iErr = 0
    while True:
        try:
            ret = bdConnect(dataOnServer=dataOnServer)
            break
        except Exception as e:
            if (iErr < 10):
                iErr += 1                                                   # ошибка + 1
            else:
                fun.funSys.logger.warning(str(e))                           # вывести сообщение если 10 и более ошибок
                iErr = 0                                                    # обнулить счетчик ошибок
    return ret


#####################################################
# BD: выполнить SQL
#####################################################
# sql  - запрос, должен содержать 'commit;' при записи в БД
# wait - ожидать доступности БД
# read - True - получить данные
# db   - для работы с открытой базой данных (не обязательно)
#####################################################
def bdSQL(sql, wait=False, read=True, db=-1):

    def run(db, dbOpened, dbReconnect):
        if ((not dbOpened) or dbReconnect): db = bdConnect()
        if read:
            cursor = db.cursor()
            cursor.execute(sql)
            ret = cursor.fetchall()
            cursor.close()
        else:
            db.autocommit(True)
            db.query(sql)
            #db.commit()
            ret = []
        if not dbOpened: bdDisconnect(db)
        return ret

    #logger.info(sql)
    ret = []
    #fun.funSys.logger.info(sql)
    if sql == '': return []
    dbOpened    = (db != -1)
    dbReconnect = False
    iErr        = 0
    while True:
        try:
            ret  = run(db, dbOpened, dbReconnect)
            isOk = True
            #fun.funSys.logger.debug("OK "+sql[:130])
        except Exception as e:
            ret  = []
            isOk = not wait
            if (iErr < 10) and wait:
                iErr += 1                                           # ошибка + 1
            else:
                fun.funSys.logger.warning(str(e)+"\n"+sql[:200])    # вывести сообщение если 10 и более ошибок
                iErr = 0                                            # обнулить счетчик ошибок
        if isOk: break
        dbReconnect = True
        time.sleep(3.0)
    return ret



#===============================================================================
#   BD.NOD: ПРОЧИТАТЬ АКТИВНЫЕ VAL В СЛОВАРЬ
#===============================================================================
def nodArrGet():
    sql = "SELECT "+NOD.NAM+", "+NOD.VAL+" "+ \
          "FROM "  +NOD.TABLE+" " + \
          "WHERE " +NOD.ENABLED+"=1;"
    val = {}
    for rec in bdSQL(sql, True, True):
        val[rec[0]] = rec[1]
    return val



#===============================================================================
#   BD.NOD: ПРОЧИТАТЬ АКТИВНЫЕ VAL В СТРОКУ
#===============================================================================
def nodValGet():
    sql = "SELECT "+NOD.VAL+" "+ \
          "FROM "  +NOD.TABLE+" " + \
          "WHERE " +NOD.ENABLED+"=1;"

    val = ''
    for rec in bdSQL(sql, True, True):                              #val = '|'.join([str(elem[0]) for elem in data])
        #if '@' in rec[0]: continue                                 # исключить записи
        val+='|('+rec[0]+')'
    return val[1:]


#==================================================================================
#   VAR
#==================================================================================
def varGet(owner, worker, name, valEmpty=None):
        sql = "SELECT "+ VAR.VALUE + " "+ \
              "FROM "  + VAR.TABLE + " "+ \
              "WHERE " + \
                  VAR.ENABLED + "=1 AND "+ \
                  VAR.OWNER   + "='" + owner  +"' AND "+ \
                  VAR.WORKER  + "='" + worker +"' AND "+ \
                  VAR.NAME    + "='" + name +"';"
        val = bdSQL(sql, True, True)
        if len(val) != 1: return valEmpty
        else: return val[0][0]



#==================================================================================
#   VAR - случайная переменная среди нескольких одноименных
#==================================================================================
def varGetRandom(owner, worker, name, valEmpty=None):
        sql = "SELECT "+ VAR.VALUE + " "+ \
              "FROM "  + VAR.TABLE + " "+ \
              "WHERE " + \
                  VAR.ENABLED + "=1 AND "+ \
                  VAR.OWNER   + "='" + owner  +"' AND "+ \
                  VAR.WORKER  + "='" + worker +"' AND "+ \
                  VAR.NAME    + "='" + name +"';"
        ret = []
        for rec in bdSQL(sql, True, True): ret.append(rec[0])
        if len(ret) == 0: return valEmpty

        return random.choice(ret)
