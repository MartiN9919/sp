import datetime

from data_base_driver.additional_functions import get_date_time_from_sec
from data_base_driver.constants.const_dat import DAT_REL
from data_base_driver.input_output.input_output import io_set, io_get_rel
from data_base_driver.relations.get_rel import get_rel_cascade, get_object_relation
from data_base_driver.sys_key.get_key_dump import get_key_by_id


def add_rel(group_id, object_1_id, rec_1_id, object_2_id, rec_2_id, params, doc_rec_id=None):
    """
    Функция для добавления связи между двумя объектами
    @param group_id: группа пользователя
    @param object_1_id: тип первого объекта для связи
    @param rec_1_id: идентификационный номер первого объекта дял связи
    @param object_2_id: тип второго объекта для связи
    @param rec_2_id: идентификационный номер второго объекта дял связи
    @param params: список словарей содержащих информацию о связях в формате [{id,val,date},...,{}]
    @param doc_rec_id: идентификатор документа описывающего связь, если нет None
    """
    temp_result_list = []
    if object_1_id > object_2_id:
        temp_object, temp_rec = object_1_id, rec_1_id
        object_1_id, rec_1_id = object_2_id, rec_2_id
        object_2_id, rec_2_id = temp_object, temp_rec
    for param in params:
        date_time_str = param.get('date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + ':00'
        key_id = param.get('id')
        key = get_key_by_id(key_id)
        if key['obj_id'] != 1:
            raise (1, 'Не связь')
        if key['rel_obj_1_id'] != object_1_id or key['rel_obj_2_id'] != object_2_id:
            raise (2, 'Не верный тип связи')
        data = [['key_id', key_id], [object_1_id, rec_1_id], [object_2_id, rec_2_id],
                [DAT_REL.DAT, date_time_str], [DAT_REL.VAL, param.get('value', '')], [DAT_REL.DOCUMENT_ID, doc_rec_id]]
        result = io_set(group_id=group_id, obj=1, data=data)
        if result[0]:
            temp_result_list.append(io_get_rel(group_id, [], [], [], [], {}, False, result[1])[0])
    result_list = []
    for temp in temp_result_list:
        exist_relation = [item for item in result_list if item['id'] == int(temp['key_id'])]
        if len(exist_relation) > 0:
            exist_relation[0]['values'].append({'val': temp['val'], 'date': get_date_time_from_sec(temp['sec'])})
        else:
            result_list.append({'id': int(temp['key_id']), 'values': [{'val': temp['val'],
                                                                       'date': get_date_time_from_sec(temp['sec'])}]})
    return {
        'object_id_1': object_1_id,
        'rec_id_1': rec_1_id,
        'object_id_2': object_2_id,
        'rec_id_2': rec_2_id,
        'params': get_object_relation(group_id, object_1_id, rec_1_id, [{'object_id': object_2_id, 'rec_id': rec_2_id}])
        [0]['relations']
    }



def add_rel_by_other_object(group_id, object_id, rec_id, other_object_id, other_rec_id):
    """
    Функция для передачи всех связей одного объекта другому
    @param group_id: идентификатор группы пользователя
    @param object_id: идентификатор типа объекта
    @param rec_id: идентификатор объекта
    @param other_object_id: идентификатор типа объекта источника связей
    @param other_rec_id: идентификатор объекта источника связей
    """
    other_object_relations = get_rel_cascade(group_id, other_object_id, other_rec_id, 1)['rels']
    result = []
    for relation_object in other_object_relations:
        for relation in relation_object['relations']:
            params = [{'id': relation['id'], 'val': item['value'],
                       'date': item['date']} for item in relation['values']]
            result += add_rel(group_id, object_id, rec_id, relation_object['object_id'],
                              relation_object['rec_id'], params)
    return result
