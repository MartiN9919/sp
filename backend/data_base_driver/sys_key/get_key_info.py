from data_base_driver.constants.const_dat import DAT_SYS_KEY


def get_key_by_id(key_id):
    """
    Функция для получения ключа классификатора по его идентификационному номеру
    @param key_id: идентификационный номер ключа классификатора
    @return: словарь содержащий информацию о ключе классификатора
    """
    if isinstance(key_id, str) and not (key_id.isdigit()):
        return 'error'
    else:
        return DAT_SYS_KEY.DUMP.get_rec(id=int(key_id))


def get_key_by_name(name):
    """
    Функция для получения ключа классификатора по его имени
    @param name: имя ключа классификатора
    @return: словарь содержащий информацию о ключе классификатора
    """
    return DAT_SYS_KEY.DUMP.get_rec(name=name)



