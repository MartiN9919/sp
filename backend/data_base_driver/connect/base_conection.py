class BaseConnection:
    """
        базоый класс для инкапсуляции соединения с базой данных и его статуса
        """

    def __init__(self, database):
        """
        Базовый конструктор, принимающий словарь с информацией о соединении
        @param database: словарь с информацией о соединении
        """
        self.set_connection(database=database)

    def set_connection(self, database):
        """
        Функция для установки соединения с базой данных
        @param database: словарь с информацией о соединении
        """
        self.connection = None
        self.busy = False

    def get_connection(self):
        """
        Функция возвращающая объект соединения mysqlDB
        @return: объект соединения mysqlDB
        """
        return self.connection

    def free_connection(self):
        """
        Функция для установки статуса как свободный
        """
        self.busy = False

    def set_busy(self):
        """
        Функция для установки статуса как занятый
        """
        self.busy = True

    def get_connection_status(self):
        """
        Функция для получения текущего статуса соединения
        @return: True/False статус соединения, где True - занято, False - свободно
        """
        return self.busy


class SingletonMeta(type):
    """
    Класс предок для создания одиночки
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

