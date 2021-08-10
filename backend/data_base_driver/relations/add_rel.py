import datetime

from data_base_driver.constants.const_dat import DAT_REL
from data_base_driver.input_output.input_output import io_set
from data_base_driver.sys_key.get_key_dump import get_key_by_id


def add_rel(group_id, key_id, object_1_id, rec_1_id, object_2_id, rec_2_id, val, date_time):
    """
    Функция для добавления связи между двумя объектами
    @param group_id: группа пользователя
    @param key_id: идентификационный номер типа связи
    @param object_1_id: тип первого объекта для связи
    @param rec_1_id: идентификационный номер первого объекта дял связи
    @param object_2_id: тип второго объекта для связи
    @param rec_2_id: идентификационный номер второго объекта дял связи
    @param val: значение идентификатора закрепленного списка если есть
    @param date_time: дата и время установления связи
    """
    if not date_time:
        date_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        date_time_str = date_time + ':00'
    if object_1_id > object_2_id:
        temp_object, temp_rec = object_1_id, rec_1_id
        object_1_id, rec_1_id = object_2_id, rec_2_id
        object_2_id, rec_2_id = temp_object, temp_rec
    key = get_key_by_id(key_id)
    if key['obj_id'] != 1:
        print('error 1')
        raise (1, 'Не связь')
    if key['rel_obj_1_id'] != object_1_id or key['rel_obj_2_id'] != object_2_id:
        print('error 2')
        raise (2, 'Не верный тип связи')
    data = [['key_id', key_id], [object_1_id, rec_1_id], [object_2_id, rec_2_id],
            [DAT_REL.DAT, date_time_str], [DAT_REL.VAL, val]]
    return io_set(group_id=group_id, obj=1, data=data)

