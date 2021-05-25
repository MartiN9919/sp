# -*- coding: utf-8 -*-

# некоторые версии MySQLdb после выполнения db.close не полностью "убирают мусор"
# добавим вызов garbage collector
import MySQLdb, MySQLdb.cursors
import gc
import re
import time
import logging

from   django.conf                import settings
from   lib.db.const.const_connect import CONNECT

logger = logging.getLogger(settings.PROJECT_LOG_REQUESTS)

##################################################################################
# ВАЖНО
# connection.insert_id() не срабатывает если  INSERT ... SET id=...
##################################################################################


##################################################################################
#  ЧИТАЕТ РЕЗУЛЬТАТЫ ЗАПРОСА ПО СТРОКАМ (ГЕНЕРАТОР)
##################################################################################
# dataOnServer=True - данные хранить на сервере - при длительных ожиданиях cursor теряет связь
# database          - база данных
##################################################################################
class DB_read_lines(object):
    def __init__(self, sql, database=CONNECT.DATA, block_size=1000, dataOnServer=True):
        self.connection   = db_connect(database=database, dataOnServer=dataOnServer)
        self.sql          = sql
        self.database     = database
        self.block_size   = block_size
        self.dataOnServer = dataOnServer

    def __del__(self):
        db_disconnect(self.connection)

    def __iter__(self):
        icount = 3
        while icount>0:
            try:
                self.connection.commit()
                cursor = self.connection.cursor()
                cursor.execute(self.sql)
                break
            except Exception as e:
                self.connection = bd_reconnect(connection=self.connection, database=self.database, dataOnServer=self.dataOnServer)
                icount -= 1

        if icount==0: raise Exception('Wrong execute sql: '+self.sql)

        #for row in cursor: yield row
        while True:
            rows = cursor.fetchmany(self.block_size)
            if not rows: break
            for row in rows: yield row



    #def __len__(self):
    #    self.connection.commit()                                                       # синхрон в т.ч. при изменении БД другими средствами
    #    val = db_sql(sql='SELECT COUNT(*) as len FROM ('+self.sql+') as titer', wait=True, read=True, connection=self.connection)
    #    if len(val) == 0: return 0
    #    return val[0][0]



##################################################################################
# КЛАСС РАБОТЫ С DB
##################################################################################
class DB_sql():
    def __init__(self, database=CONNECT.DATA, dataOnServer=False):
        self.database   = database
        self.connection = db_connect(database=database, dataOnServer=dataOnServer)

    def __del__(self):
        db_disconnect(self.connection)

    def execute(self, sql, wait=False, read=True):
        return db_sql(sql, wait, read, database=self.database, connection=self.connection)



##################################################################################
# BD: УСТАНОВИТЬ / РАЗОРВАТЬ СОЕДИНЕНИЕ
##################################################################################
# dataOnServer - хранить результаты на сервере (для больших запросов)
# database     - база данных
##################################################################################
def db_connect(database=CONNECT.DATA, dataOnServer=False):
    return MySQLdb.connect(
        host        = database.HOST,
        port        = int(database.PORT),
        user        = database.USER,
        passwd      = database.PASSWORD,
        db          = database.NAME,
        charset     = database.CHARSET,
        cursorclass = MySQLdb.cursors.SSCursor if dataOnServer else MySQLdb.cursors.Cursor)

def db_disconnect(connection):
    try:
        connection.close()
        gc.collect()
    except Exception:
        pass


def bd_reconnect(connection, database=CONNECT.DATA, dataOnServer=False):
    db_disconnect(connection)
    iErr = 0
    while True:
        try:
            ret = db_connect(database=database, dataOnServer=dataOnServer)
            break
        except Exception as e:
            if (iErr < 10):
                iErr += 1                                                   # ошибка + 1
            else:
                logger.warning(str(e))                                      # вывести сообщение если 10 и более ошибок
                iErr = 0                                                    # обнулить счетчик ошибок
    return ret


#####################################################
# BD: выполнить SQL
#####################################################
# sql  - запрос, должен содержать 'commit;' при записи в БД
# wait - ожидать доступности БД
# read - True - получить данные
# connection  - для работы с открытой базой данных (не обязательно)
#####################################################
def db_sql(sql, wait=False, read=True, database=CONNECT.DATA, connection=-1):

    def run(connection, dbOpened, dbReconnect):
        if ((not dbOpened) or dbReconnect): connection = db_connect(database=database)
        if read:
            cursor = connection.cursor()
            cursor.execute(sql)
            ret = cursor.fetchall()
            cursor.close()
        else:
            connection.autocommit(True)
            connection.query(sql)
            #connection.commit()
            ret = []
        if not dbOpened: db_disconnect(connection)
        return ret

    #logger.info(sql)
    ret = []
    if sql == '': return []
    dbOpened    = (connection != -1)
    dbReconnect = False
    iErr        = 0
    while True:
        try:
            ret  = run(connection, dbOpened, dbReconnect)
            isOk = True
            #logger.debug("OK "+sql[:130])
        except Exception as e:
            ret  = []
            isOk = not wait
            if (iErr < 10) and wait:
                iErr += 1                                           # ошибка + 1
            else:
                logger.warning(str(e)+"\n"+sql[:200])               # вывести сообщение если 10 и более ошибок
                iErr = 0                                            # обнулить счетчик ошибок
        if isOk: break
        dbReconnect = True
        time.sleep(3.0)
    return ret


# # не работает при вставке одной записи, при вставке нескольких записей работает
# # exec_info(self.connection, 'Rows matched')
# def exec_info(connection, var):
#     #var = re.findall(r'([^:]+): (\d+)[\s]*', connection.info())    # 'Rows matched: 12  Changed: 0  Warnings: 0'
#     tmp = connection.info()
#     return int(re.findall(r'.*'+var+': (\d+)', tmp)[0]) if tmp else None




# #===============================================================================
# #   BD.NOD: ПРОЧИТАТЬ АКТИВНЫЕ VAL В СЛОВАРЬ
# #===============================================================================
# def nodArrGet():
#     sql = "SELECT "+NOD.NAM+", "+NOD.VAL+" "+ \
#           "FROM "  +NOD.TABLE+" " + \
#           "WHERE " +NOD.ENABLED+"=1;"
#     val = {}
#     for rec in db_sql(sql, True, True):
#         val[rec[0]] = rec[1]
#     return val



# #===============================================================================
# #   BD.NOD: ПРОЧИТАТЬ АКТИВНЫЕ VAL В СТРОКУ
# #===============================================================================
# def nodValGet():
#     sql = "SELECT "+NOD.VAL+" "+ \
#           "FROM "  +NOD.TABLE+" " + \
#           "WHERE " +NOD.ENABLED+"=1;"

#     val = ''
#     for rec in db_sql(sql, True, True):                              #val = '|'.join([str(elem[0]) for elem in data])
#         #if '@' in rec[0]: continue                                 # исключить записи
#         val+='|('+rec[0]+')'
#     return val[1:]


# #==================================================================================
# #   VAR
# #==================================================================================
# def varGet(owner, worker, name, valEmpty=None):
#         sql = "SELECT "+ VAR.VALUE + " "+ \
#               "FROM "  + VAR.TABLE + " "+ \
#               "WHERE " + \
#                   VAR.ENABLED + "=1 AND "+ \
#                   VAR.OWNER   + "='" + owner  +"' AND "+ \
#                   VAR.WORKER  + "='" + worker +"' AND "+ \
#                   VAR.NAME    + "='" + name +"';"
#         val = db_sql(sql, True, True)
#         if len(val) != 1: return valEmpty
#         else: return val[0][0]



# #==================================================================================
# #   VAR - случайная переменная среди нескольких одноименных
# #==================================================================================
# def varGetRandom(owner, worker, name, valEmpty=None):
#         sql = "SELECT "+ VAR.VALUE + " "+ \
#               "FROM "  + VAR.TABLE + " "+ \
#               "WHERE " + \
#                   VAR.ENABLED + "=1 AND "+ \
#                   VAR.OWNER   + "='" + owner  +"' AND "+ \
#                   VAR.WORKER  + "='" + worker +"' AND "+ \
#                   VAR.NAME    + "='" + name +"';"
#         ret = []
#         for rec in db_sql(sql, True, True): ret.append(rec[0])
#         if len(ret) == 0: return valEmpty

#         return random.choice(ret)
