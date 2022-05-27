import threading

import MySQLdb, MySQLdb.cursors
import time
from data_base_driver.connect.base_conection import SingletonMeta, BaseConnection
from data_base_driver.constants.connect_db import VEC_DATA


class MySqlConnection(BaseConnection):
    """
    Класс для инкапсуляции соединения с базой данных mysql и его статуса
    """
    def set_connection(self, database):
        """
        Функция для установки соединения с базой данных
        @param database: словарь с информацией о соединении
        """
        self.connection = MySQLdb.connect(
            host=database['HOST'],
            port=int(database['PORT']),
            user=database['USER'],
            passwd=database['PASSWORD'],
            db=database['NAME'],
            charset=database['CHARSET'],
        )
        self.busy = False


class MySqlConnectionPool(metaclass=SingletonMeta):
    """
    Класс одиночка для инициализации пула соединений к базе данных
    """

    def __init__(self, n, database=VEC_DATA):
        """
        Конструктор для инициализации объекта класса
        @param n: количество соединений в пуле
        @param database: словарь с информацией о соединении
        """
        self.connections_list = [MySqlConnection(database) for i in range(n)]
        self._lock = threading.Lock()

    def get_connection(self):
        """
        Функция для получения свободного объекта класса MySqlConnection
        @return: свободный объект класса MySqlConnection
        """
        with self._lock:
            free_connection = [connection for connection in self.connections_list if
                               not (connection.get_connection_status())]
            try:
                free_connection[0].set_busy()
                free_connection[0].get_connection().ping(True)
                return free_connection[0]
            except IndexError as e:
                print('not free connection')
                return False
            except Exception as e:
                free_connection[0].free_connection()
                return False


def connect_to_data_base(database=VEC_DATA):
    """
    Функция для получения объекта соединения с базой данных, при отсутствии в
    пуле свободного соединения, будет производиться ожидание появления свободного
    @param database: словарь с информацией о соединении
    @return: свободный объект класса соединения
    """
    while True:
        connection = MySqlConnectionPool(n=5, database=database).get_connection()
        if connection:
            return connection
        else:
            time.sleep(0.1)


def db_sql(sql, wait=False, read=True, database=VEC_DATA, connection=None):
    """
    Функция для выполнения sql запроса в базе данных
    @param sql: текст sql запроса
    @param wait: ожидать доступности БД
    @param read: режим чтения/записи, если True чтение, если False - запись
    @param database: словарь с информацией о соединении
    @param connection: объект соединения, если нет то -1
    @return: результат запроса на чтение, либо список с идентификатором добавленного объекта, или список со
    строкой 'error' в случае ошибки
    """
    def run(connection_my_sql, is_open, is_reconnect):
        if not is_open or is_reconnect:
            connection_my_sql = connect_to_data_base(database=database)
        query_connection = connection_my_sql.get_connection()
        if read:
            query_connection.begin()
            cursor = query_connection.cursor()
            try:
                cursor.execute(sql)
                request_result = cursor.fetchall()
                cursor.close()
            except Exception as e:
                connection_my_sql.free_connection()
                raise e
        else:
            try:
                query_connection.query(sql)
                request_result = [query_connection.insert_id()]
                query_connection.commit()
            except Exception as e:
                connection_my_sql.free_connection()
                raise e
        if not is_open:
            connection_my_sql.free_connection()
        return request_result

    if sql == '':
        return []
    database_open = not (connection is None)
    database_reconnect = False
    error_count = 0
    while True:
        try:
            result = run(connection, database_open, database_reconnect)
            is_ok = True
        except Exception as e:
            print(e)
            result = []
            is_ok = not wait
            if (error_count < 10) and wait:
                error_count += 1  # ошибка + 1
            else:
                return ['error']  # обнулить счетчик ошибок
        if is_ok:
            break
        database_reconnect = True
        time.sleep(0.03)
    return result
