import threading
import time

from data_base_driver.connect.base_conection import SingletonMeta, BaseConnection
from data_base_driver.constants.connect_db import OSM
import psycopg2


class PgSqlConnection(BaseConnection):
    def set_connection(self, database):
        self.connection = psycopg2.connect(
            host=database['HOST'],
            database=database['NAME'],
            user=database['USER'],
            password=database['PASSWORD'],
        )
        self.busy = False


class SingletonPgsql(metaclass=SingletonMeta):
    def __init__(self, n, database=OSM):
        self.connections_list = [PgSqlConnection(database) for i in range(n)]
        self._lock = threading.Lock()

    def get_connection(self):
        with self._lock:
            try:
                free_connection = [connection for connection in self.connections_list if
                                   not (connection.get_connection_status())]
                free_connection[0].set_busy()
                if free_connection[0].get_connection().closed != 0:
                    free_connection[0] = PgSqlConnection(OSM)
                return free_connection[0]
            except:
                print('not free connection')
                return False

    def reconnect(self, database):
        for connection in self.connections_list:
            connection.set_connection(database)


def connect_to_data_base(database=OSM):
    while True:
        connection = SingletonPgsql(n=5, database=database).get_connection()
        if connection:
            return connection
        else:
            time.sleep(0.1)


def db_connect(database=OSM, dataOnServer=False):
    return connect_to_data_base(database)


def db_pg_sql(sql, wait=False, read=True, database=OSM, connection=-1):
    def run(connection_pg_sql, dbOpened, dbReconnect):
        if ((not dbOpened) or dbReconnect):
            connection_pg_sql = db_connect(database=database)
        connection = connection_pg_sql.get_connection()
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

    if sql == '':
        return []
    dbOpened = not (connection == -1)
    dbReconnect = False
    iErr = 0
    while True:
        try:
            ret = run(connection, dbOpened, dbReconnect)
            isOk = True
            # logger.debug("OK "+sql[:130])
        except Exception as e:
            ret = []
            isOk = not wait
            if (iErr < 10) and wait:
                iErr += 1
            else:
                return ['error']
        if isOk: break
        dbReconnect = True
        time.sleep(3.0)
    return ret




