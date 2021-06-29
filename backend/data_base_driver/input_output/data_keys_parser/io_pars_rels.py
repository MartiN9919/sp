from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_REL

DEBUG = False


###########################################
# РАСПАРСИТЬ RELS (СВЯЗЫВАЕМЫЕ ОБЪЕКТЫ В REL)
# ДЛЯ ПОСЛЕДУЮЩИХ SQL-ЗАПРОСОВ
###########################################
class IO_PARS_RELS(dict):
    # ключи dict
    EQU_1 = 'equ_1'  # вариант 1 условий для SQL запроса
    EQU_2 = 'equ_2'  # вариант 2 ...

    def __init__(self, obj_rel_1=None, obj_rel_2=None):
        obj_id_1 = None
        obj_id_2 = None
        rec_id_1 = None
        rec_id_2 = None
        if obj_rel_1:
            if len(obj_rel_1) > 0: obj_id_1 = DAT_SYS_OBJ.DUMP.to_id(obj_rel_1[0])
            if len(obj_rel_1) > 1: rec_id_1 = obj_rel_1[1]

        if obj_rel_2:
            if len(obj_rel_2) > 0: obj_id_2 = DAT_SYS_OBJ.DUMP.to_id(obj_rel_2[0])
            if len(obj_rel_2) > 1: rec_id_2 = obj_rel_2[1]

        # порядок следования
        if obj_rel_1 and obj_rel_2:
            # obj_id с меньшим индексом всегда obj_id_1
            if obj_id_1 > obj_id_2:
                obj_id_1, obj_id_2 = obj_id_2, obj_id_1
                rec_id_1, rec_id_2 = rec_id_2, rec_id_1
            # только для известных rec_id
            elif rec_id_1 and rec_id_2:
                # если obj_id равны: rec_id с меньшим индексом всегда rec_id_1
                if obj_id_1 == obj_id_2 and rec_id_1 > rec_id_2:
                    rec_id_1, rec_id_2 = rec_id_2, rec_id_1
                # если obj_id и rec_id равны: ошибка - связь объекта с самим собой не существует
                elif obj_id_1 == obj_id_2 and rec_id_1 == rec_id_2:
                    raise Exception('OBJ/REC_1 == OBJ/REC_2: ' + str(obj_id_1) + ', ' + str(rec_id_1))

        # если один элемент, то первый
        if obj_rel_2 and not obj_rel_1:
            obj_id_1, obj_id_2 = obj_id_2, None
            rec_id_1, rec_id_2 = rec_id_2, None

        self.equ_1 = self[self.EQU_1] = []
        self.equ_2 = self[self.EQU_2] = []

        # заданы два obj_id и rec_id - только один вариант (порядок объектов в записи-связи известен)
        if obj_id_1 and rec_id_1 and obj_id_2 and rec_id_2:
            self.equ_1 += [
                DAT_REL.OBJ_ID_1 + '=' + str(obj_id_1),
                DAT_REL.REC_ID_1 + '=' + str(rec_id_1),
                DAT_REL.OBJ_ID_2 + '=' + str(obj_id_2),
                DAT_REL.REC_ID_2 + '=' + str(rec_id_2),
            ]

        # заданы два РАЗНЫХ obj_id - только один вариант (порядок объектов в записи-связи известен)
        elif obj_id_1 and obj_id_2 and obj_id_1 != obj_id_2:
            self.equ_1.append(DAT_REL.OBJ_ID_1 + '=' + str(obj_id_1))
            self.equ_1.append(DAT_REL.OBJ_ID_2 + '=' + str(obj_id_2))
            if rec_id_1: self.equ_1.append(DAT_REL.REC_ID_1 + '=' + str(rec_id_1))
            if rec_id_2: self.equ_1.append(DAT_REL.REC_ID_2 + '=' + str(rec_id_2))

        # заданы два ОДИНАКОВЫХ obj_id, отсутствуют оба rec_id - только один вариант (порядок объектов в записи-связи не важен)
        elif obj_id_1 and obj_id_2 and not rec_id_1 and not rec_id_2:
            self.equ_1.append(DAT_REL.OBJ_ID_1 + '=' + str(obj_id_1))
            self.equ_1.append(DAT_REL.OBJ_ID_2 + '=' + str(obj_id_2))
            if rec_id_1: self.equ_1.append(DAT_REL.REC_ID_1 + '=' + str(rec_id_1))
            if rec_id_2: self.equ_1.append(DAT_REL.REC_ID_2 + '=' + str(rec_id_2))

        # два варианта (порядок объектов в записи-связи НЕ известен)
        else:
            if obj_id_1:
                self.equ_1.append(DAT_REL.OBJ_ID_1 + '=' + str(obj_id_1))
                self.equ_2.append(DAT_REL.OBJ_ID_2 + '=' + str(obj_id_1))
            if rec_id_1:
                self.equ_1.append(DAT_REL.REC_ID_1 + '=' + str(rec_id_1))
                self.equ_2.append(DAT_REL.REC_ID_2 + '=' + str(rec_id_1))
            if obj_id_2:
                self.equ_1.append(DAT_REL.OBJ_ID_2 + '=' + str(obj_id_2))
                self.equ_2.append(DAT_REL.OBJ_ID_1 + '=' + str(obj_id_2))
            if rec_id_2:
                self.equ_1.append(DAT_REL.REC_ID_2 + '=' + str(rec_id_2))
                self.equ_2.append(DAT_REL.REC_ID_1 + '=' + str(rec_id_2))
