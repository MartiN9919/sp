import threading

import MySQLdb, MySQLdb.cursors
import time
from data_base_driver.connect.base_conection import SingletonMeta, BaseConnection
from data_base_driver.constants.connect_db import VEC_DATA
from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_KEY, DAT_OWNER

AUTOCOMMIT = True


class DB_read_lines(object):
    def __init__(self, sql, database=VEC_DATA, block_size=1000, dataOnServer=True):
        self.connection = db_connect(database=database, dataOnServer=dataOnServer)
        self.sql = sql
        self.database = database
        self.block_size = block_size
        self.dataOnServer = dataOnServer

    def __del__(self):
        db_disconnect(self.connection)

    def __iter__(self):
        icount = 3
        while icount > 0:
            try:
                self.connection.get_connection().commit()
                cursor = self.connection.cursor()
                cursor.execute(self.sql)
                break
            except Exception:
                # self.connection = bd_reconnect(connection=self.connection, database=self.database,
                #                                dataOnServer=self.dataOnServer)
                icount -= 1

        if icount == 0:
            raise Exception('Wrong execute sql: ' + self.sql)

        while True:
            rows = cursor.fetchmany(self.block_size)
            if not rows: break
            for row in rows: yield row


class DB_sql():
    """
    КЛАСС РАБОТЫ С DB
    """

    def __init__(self, database=VEC_DATA, dataOnServer=False):
        self.database = database
        self.connection = db_connect(database=database, dataOnServer=dataOnServer)

    def __del__(self):
        db_disconnect(self.connection)

    def execute(self, sql, wait=False, read=True):
        return db_sql(sql, wait, read, database=self.database, connection=self.connection)


class MySqlConnection(BaseConnection):
    """
    класс для инкапсуляции соединения с базой данных mysql и его статуса
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


class Singleton(metaclass=SingletonMeta):
    """
    класс одиночка для инициализации пула соединений к базе данных
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
        @return: свободный объекта класса MySqlConnection
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
        Функция для пере подключения пула к другой базе данных
        @param database: словарь с информацией о соединении
        """
        for connection in self.connections_list:
            connection.set_connection(database)


def connect_to_data_base(database=VEC_DATA):
    """
    Функция для получения объекта соединения с базой данных, при отсутствии в
    пуле свободного соединения, будет производится ожидание появления свободного
    @param database: словарь с информацией о соединении
    @return: свободный объект класса соединения
    """
    while True:
        connection = Singleton(n=5, database=database).get_connection()
        if connection:
            return connection
        else:
            time.sleep(0.1)


def db_connect(database=VEC_DATA, dataOnServer=False):
    """
    Функция для получения объекта соединения с базой данных, главная точка входа
    @param database: словарь с информацией о соединении
    @param dataOnServer: - вырожденный параметр
    @return: свободный объект класса соединения
    """
    return connect_to_data_base(database)


def db_reconnect(database):
    """
    Функция для пере подключения пула соединений к другой базе данных
    @param database: словарь с информацией о соединении
    """
    Singleton(n=10, database=database).reconnect(database=database)
    DAT_SYS_OBJ.DUMP._refresh_(force=True)
    DAT_SYS_KEY.DUMP._refresh_(force=True)
    DAT_OWNER.DUMP._refresh_(force=True)


def db_disconnect(connection):
    """
    Функция для освобождения объекта соединения
    @param connection: объекта соединения
    """
    try:
        connection.free_connection()
    except Exception:
        pass


def set_autocommit_off():
    """
    включения тестового режима
    """
    global AUTOCOMMIT
    AUTOCOMMIT = False


def set_autocommit_on():
    """
    Выключение тестового режима
    """
    global AUTOCOMMIT
    AUTOCOMMIT = True


def roll_back():
    """
    Откат в тестовом режиме
    """
    db_sql('ROLLBACK;')


def bd_reconnect(connection, database=VEC_DATA, dataOnServer=False):
    for attempt in range(10):
        try:
            ret = db_connect(database=database, dataOnServer=dataOnServer)
            return ret
        except Exception:
            pass


def db_sql(sql, wait=False, read=True, database=VEC_DATA, connection=-1):
    """
    Функция для выполнения sql запроса в базе данных
    @param sql: текст sql запроса
    @param wait: ожидать доступности БД
    @param read: режим чтения/записи, если True чтение, если False - запись
    @param database: словарь с информацией о соединении
    @param connection: объект соединения, если нет то -1
    @return: результат запроса на чтение, либо пустой список если успешная запись, или список с
    строкой 'error' в случае ошибки
    """
    def run(connection_my_sql, db_opened, db_reconnect):
        if ((not db_opened) or db_reconnect):
            connection_my_sql = db_connect(database=database)
        connection = connection_my_sql.get_connection()
        if read:
            if AUTOCOMMIT: connection.begin()
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
            except Exception as e:
                connection_my_sql.free_connection()
                raise e
            ret = cursor.fetchall()
            cursor.close()
        else:
            connection.autocommit(AUTOCOMMIT)
            try:
                connection.query(sql)
            except Exception as e:
                connection_my_sql.free_connection()
                raise e
            ret = []
            ret.append(connection.insert_id())
            if AUTOCOMMIT:
                connection.commit()
        if not (db_opened):
            connection_my_sql.free_connection()
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
