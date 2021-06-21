from data_base_driver.input_output.io import io_set


def add_record(group_id, object_id, object_info):
    """
    функция для добавления объекта в базу данных
    @param group_id: идентификационный номер группы пользователя
    @param object_id: идентификационный номер типа объекта
    @param object_info: информация об объекте в формате [[key:value],[],...,[]]
    для добавления информации о уже существующем объекте необходимо в качестве ключа передать id,
    а в качестве значение точный идентификационный номер объекта
    @return:
    """
    result = io_set(group_id=group_id, obj=object_id, data=object_info)
    if result[0]:
        return result[1]
    else:
        return -1


# test_object = {'object_id': 45, 'rec_id': 34, 'params': [{'id': 45001, 'val': 'val1'}, {'id': 45002, 'val': 'val2'}]}
def add_data(group_id, object):
    data = [[param['id'], param['val']] for param in object['params']]
    if object.get('rec_id'):
        data.append(['id', object.get('rec_id')])
    return add_record(group_id=group_id, object_id=object.get('object_id'), object_info=data)
