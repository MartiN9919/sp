from data_base_driver.constants.const_dat import DAT_SYS_PHONE_NUMBER_FORMAT
from data_base_driver.sys_key.get_key_dump import get_key_by_id


def remove_special_chars(word):
    """
    Функция для удаления из номера телефона всех символов кроме начального плюса и цифр
    @param word: введенный пользователем номер телефона
    @return: номер телефона без лишних символов и пробелов - +375 29 583-65-67 -> +375295836567
    """
    return '+' + str(''.join(i for i in word if i.isdigit()))


def get_country_by_number(phone_number):
    """
    Функция для получения страны по телефонному номеру
    @param phone_number: телефонный номер
    @return: строка содержащая название страны
    """
    phone_number_format = DAT_SYS_PHONE_NUMBER_FORMAT.DUMP.get_all()
    phone_number = remove_special_chars(phone_number)[1:]
    for format in phone_number_format:
        code, length = str(format['country_code']), format['length']
        if phone_number.find(code) == 0 and len(phone_number) == length:
            return format['country']
    return 'Неизвестно'


def validate_phone_number(phone_number):
    """
    Функция для проверки правильности формата телефонного номера
    @param phone_number: телефонный номер
    @return: True - если формат допустимый, False - если нет
    """
    phone_number_format = DAT_SYS_PHONE_NUMBER_FORMAT.DUMP.get_all()
    phone_number = remove_special_chars(phone_number)[1:]
    for format in phone_number_format:
        code, length = str(format['country_code']), format['length']
        if phone_number.find(code) == 0 and len(phone_number) == length:
            return True
    return False


def validate_record(record):
    """
    Функция для проверки правильности вносимой записи
    @param record: вносимая запись
    @return: True - если запись корректна, исключение с тестом объясняющим ошибку
    """
    if len(record['value']) == 0:
        return False
    key = get_key_by_id(record['id'])
    if key['type'] == 'phone_number' and not validate_phone_number(record['value']):
        raise Exception(1, 'Некорректный формат номера телефона')
    return True


def validate_geometry_permission(group_id):
    """
    Прототип функции для проверки доступа к изменению геометрии
    @param group_id: идентификатор группы пользователя
    @return: True - если есть доступ, False - если нет доступа
    """
    if group_id != 1:
        return False
    else:
        return True




