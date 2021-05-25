# -*- coding: utf-8 -*-

# pip3 install psycopg2-binary
# добавим вызов garbage collector

#import MySQLdb, MySQLdb.cursors
import psycopg2
import gc
import time
import logging

from   django.conf                import settings
from   lib.db.const.const_connect import CONNECT

logger = logging.getLogger(settings.PROJECT_LOG_REQUESTS)



##################################################################################
#  ЧИТАЕТ РЕЗУЛЬТАТЫ ЗАПРОСА ПО СТРОКАМ (ГЕНЕРАТОР)
##################################################################################
class DB_read_lines(object):
    def __init__(self, sql, database=CONNECT.OSM, block_size=1000):
        self.connection   = db_connect(database=database)
        self.sql          = sql
        self.database     = database
        self.block_size   = block_size

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
                self.connection = bd_reconnect(connection=self.connection, database=self.database)
                icount -= 1

        if icount==0: raise Exception('Wrong execute sql: '+self.sql)

        #for row in cursor: yield row
        while True:
            rows = cursor.fetchmany(self.block_size)
            if not rows: break
            for row in rows: yield row



##################################################################################
# КЛАСС РАБОТЫ С DB
##################################################################################
class DB_sql():
    def __init__(self, database=CONNECT.OSM):
        self.database   = database
        self.connection = db_connect(database=database)

    def __del__(self):
        db_disconnect(self.connection)

    def execute(self, sql, wait=False, read=True):
        return db_sql(sql, wait, read, database=self.database, connection=self.connection)



##################################################################################
# BD: УСТАНОВИТЬ / РАЗОРВАТЬ СОЕДИНЕНИЕ
##################################################################################
def db_connect(database=CONNECT.OSM):
    conn = psycopg2.connect(
        host        = database.HOST,
        port        = int(database.PORT),
        user        = database.USER,
        password    = database.PASSWORD,
        database    = database.NAME)
    if conn.encoding != database.CHARSET: conn.set_client_encoding(database.CHARSET)
    return conn

def db_disconnect(connection):
    try:
        connection.close()
        gc.collect()
    except Exception:
        pass


def bd_reconnect(connection, database=CONNECT.OSM):
    db_disconnect(connection)
    iErr = 0
    while True:
        try:
            ret = db_connect(database=database)
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
def db_sql(sql, wait=False, read=True, database=CONNECT.OSM, connection=-1):

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
    #logger.info(sql)
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
            #print(e)
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
