import threading
import time

import MySQLdb

from data_base_driver.connect.connect_mysql import SingletonMeta, BaseConnection
from data_base_driver.constants.connect_db import MANTICORE

AUTOCOMMIT = True


class ManticoreConnection(BaseConnection):
    """
    класс для инкапсуляции соединения с сервисом manticore и его статуса
    """

    def set_connection(self, database):
        """
        Функция для установки соединения с manticore
        @param database: словарь с информацией о соединении
        """
        self.connection = MySQLdb.connect(
            host=database['HOST'],
            port=int(database['PORT']),
            db=database['NAME'],
        )
        self.busy = False


class SingletonManticore(metaclass=SingletonMeta):
    """
    класс одиночка для инициализации пула соединений к manticore
    """

    def __init__(self, n, database=MANTICORE):
        """
        Конструктор для инициализации объекта класса
        @param n: количество соединений в пуле
        @param database: словарь с информацией о соединении
        """
        self.connections_list = [ManticoreConnection(database) for i in range(n)]
        self._lock = threading.Lock()

    def get_connection(self):
        """
        Функция для получения свободного объекта класса ManticoreConnection
        @return: свободный объекта класса ManticoreConnection
        """
        with self._lock:
            try:
                free_connection = [connection for connection in self.connections_list if
                                   not (connection.get_connection_status())]
                free_connection[0].set_busy()
                free_connection[0].get_connection().ping(True)
                return free_connection[0]
            except:
                print('not free connection')
                return False

    def reconnect(self, database):
        """
        Функция для пере подключения пула к другому серверу manticore
        @param database: словарь с информацией о соединении
        """
        for connection in self.connections_list:
            connection.set_connection(database)


def connect_to_manticore(database=MANTICORE):
    """
    Функция для получения объекта соединения с manticore, при отсутствии в
    пуле свободного соединения, будет производится ожидание появления свободного
    @param database: словарь с информацией о соединении
    @return: свободный объект класса соединения
    """
    while True:
        connection = SingletonManticore(n=5, database=database).get_connection()
        if connection:
            return connection
        else:
            time.sleep(0.1)


def manticore_connect(database=MANTICORE):
    """
    Функция для получения объекта соединения с manticore, главная точка входа
    @param database: словарь с информацией о соединении
    @param dataOnServer: - вырожденный параметр
    @return: свободный объект класса соединения
    """
    return connect_to_manticore(database)


def manticore_connect_reconnect(database):
    """
    Функция для пере подключения пула соединений к другому серверу manticore
    @param database: словарь с информацией о соединении
    """
    SingletonManticore(n=10, database=database).reconnect(database=database)


def manticore_disconnect(connection):
    """
    Функция для освобождения объекта соединения
    @param connection: объекта соединения
    """
    try:
        connection.free_connection()
    except Exception:
        pass


def db_shinxql(sql, wait=False, read=True, database=MANTICORE, connection=-1):
    """
    Функция для выполнения sphinxql запроса в базе данных
    @param sql: текст sphinxql запроса
    @param wait: ожидать доступности manticore
    @param read: режим чтения/записи, если True чтение, если False - запись
    @param database: словарь с информацией о соединении
    @param connection: объект соединения, если нет то -1
    @return: результат запроса на чтение, либо пустой список если успешная запись, или список с
    строкой 'error' в случае ошибки
    """

    def run(connection_manticore, db_opened, db_reconnect):
        if ((not db_opened) or db_reconnect):
            connection_manticore = manticore_connect(database=database)
        connection = connection_manticore.get_connection()
        if read:
            if AUTOCOMMIT: connection.begin()
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
            except Exception as e:
                connection_manticore.free_connection()
                raise e
            ret = cursor.fetchall()
            cursor.close()
        else:
            connection.autocommit(AUTOCOMMIT)
            try:
                connection.query(sql)
            except Exception as e:
                connection_manticore.free_connection()
                raise e

            ret = []
            ret.append(connection.insert_id())
        if not (db_opened):
            connection_manticore.free_connection()
        return ret

    if sql == '':
        return []
    db_opened = not (connection == -1)
    db_reconnect = False
    iErr = 0
    while True:
        try:
            ret = run(connection, db_opened, db_reconnect)
            isOk = True
            # logger.debug("OK "+sql[:130])
        except Exception as e:
            ret = []
            isOk = not wait
            if (iErr < 10) and wait:
                iErr += 1  # ошибка + 1
            else:
                return ['error']  # обнулить счетчик ошибок
        if isOk: break
        db_reconnect = True
        time.sleep(0.03)
    return ret
