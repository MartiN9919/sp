from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_ID


def get_all_objects():
    """
    Функция для получения списка всех объектов
    @return: список всех объектов
    """
    return DAT_SYS_OBJ.DUMP.get_all()


def get_object_by_name(name):
    """
    Функция для получения объекта по его имени
    @param name: имя объекта
    @return: словарь содержащий информацию о объекте
    """
    return DAT_SYS_OBJ.DUMP.get_rec(name=name)


def get_object_by_id(id):
    """
    Функция для получения объекта по его идентификационному номеру
    @param id: идентификационный номер объекта
    @return: словарь содержащий информацию о объекте
    """
    return DAT_SYS_OBJ.DUMP.get_rec(id=id)


