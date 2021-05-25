##################################################################################
# кортеж или список в словарь
# src_tuple = (..)
##################################################################################
def tuple_to_dict(src_tuple, desc_keys):
    ret = {}
    for desc_keys_ind, desc_keys_item in enumerate(desc_keys):
        val = src_tuple[desc_keys_ind]
        if isinstance(val, bytes): val = (val==b'\x01')
        ret[desc_keys_item] = val
    return ret


##################################################################################
# кортеж или список в словарь
# src_tuple = ((..), (..), ..)
##################################################################################
def tuple_to_dict_many(src_tuple, desc_keys):
    ret = []
    for src_tuple_item in src_tuple:
        ret.append(tuple_to_dict(src_tuple_item, desc_keys))
    return ret


##################################################################################
# найти в списке словарей list_dict записи и их индексы по парам ключ-значение list_key_val
# list_dict    - [{...}, {...}, ...]
# list_key_val - (key,val) или ((key1,val1),(key2,val2), ...)
# результат: список найденных записей
##################################################################################
def dict_filter(list_dict, list_key_val, only_first=False):
    list_key_val_standart = list_key_val if isinstance(list_key_val[0], (list, tuple)) else (list_key_val,)  # list_key_val к виду (())
    ret = []
    for dict_item in list_dict:
        # подходит ли очередная запись
        valid = True
        for key_val in list_key_val_standart:
            if dict_item[key_val[0]]!=key_val[1]:
                valid = False
                break

        # запись подходит: запомнить
        if valid:
            ret.append(dict_item)
            if only_first: break

    return ret
