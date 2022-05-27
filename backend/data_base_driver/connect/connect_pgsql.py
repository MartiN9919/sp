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


class PgSqlConnectionPool(metaclass=SingletonMeta):
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
            except IndexError as e:
                print('not free connection')
                return False
            except Exception as e:
                free_connection[0].free_connection()
                return False


def connect_to_data_base(database=OSM):
    while True:
        connection = PgSqlConnectionPool(n=5, database=database).get_connection()
        if connection:
            return connection
        else:
            time.sleep(0.1)


def db_pg_sql(sql, wait=False, read=True, database=OSM, connection=None):
    def run(connection_pg_sql, is_open, is_reconnect):
        if not is_open or is_reconnect:
            connection_pg_sql = connect_to_data_base(database=database)
        query_connection = connection_pg_sql.get_connection()
        if read:
            try:
                cursor = query_connection.cursor()
                cursor.execute(sql)
                query_result = cursor.fetchall()
                cursor.close()
            except Exception as e:
                connection_pg_sql.free_connection()
                raise e
        else:
            query_connection.autocommit(True)
            query_connection.query(sql)
            query_result = []
        if not is_open:
            connection_pg_sql.free_connection()
        return query_result

    if sql == '':
        return []
    database_open = not (connection is None)
    data_base_reconnect = False
    error_count = 0
    while True:
        try:
            result = run(connection, database_open, data_base_reconnect)
            is_ok = True
        except Exception as e:
            result = []
            is_ok = not wait
            if (error_count < 10) and wait:
                error_count += 1
            else:
                return ['error']
        if is_ok:
            break
        data_base_reconnect = True
        time.sleep(3.0)
    return result




