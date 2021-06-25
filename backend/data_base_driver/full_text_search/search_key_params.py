from data_base_driver.connect.connect_manticore import db_shinxql
from data_base_driver.constants.fulltextsearch import FullTextSearch


def find_key_value(object_id, key_id, value):
    """
    Функция для нахождения в базе данных по отдельным полям
    @param object_id: идентификатор типа объекта
    @param key_id: ключ искомого классификатора
    @param value: искомое значение
    @return: список идентификатор объектов
    """
    fetchall = db_shinxql('SELECT id FROM obj_' + FullTextSearch.TABLES[object_id] + '_row '
                                        'WHERE MATCH(\'@key_id ' + str(key_id) + ' '\
                                        '@val ' + str(value) + '\');')
    return [item[0] for item in fetchall]
