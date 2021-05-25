from datetime import time

from data_base_driver.constants.connect_db import OSM
import psycopg2

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class SingletonPgsql(metaclass=SingletonMeta):
    def __init__(self,database=OSM, dataOnServer=False):
        self.connection = psycopg2.connect(
            host=database['HOST'],
            database=database['NAME'],
            user=database['USER'],
            password=database['PASSWORD'],
            )
        print('connection to pgsql data base')

    def get_connection(self):
        return self.connection

def connect_to_data_base(database=OSM, dataOnServer=False):
    return SingletonPgsql(database=database,dataOnServer=dataOnServer).get_connection()

def db_connect(database=OSM, dataOnServer=False):
    return connect_to_data_base(database, dataOnServer)

def db_sql(sql, wait=False, read=True, database=OSM, connection=-1):

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
            ret = []
        return ret

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
                return ['error']                                          # обнулить счетчик ошибок
        if isOk: break
        dbReconnect = True
        time.sleep(3.0)
    return ret


