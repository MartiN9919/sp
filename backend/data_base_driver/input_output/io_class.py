from data_base_driver.constants.const_dat import DAT_SYS_OBJ, DAT_SYS_KEY, DAT_REL
from data_base_driver.input_output.data_keys_parser.io_pars_data import IO_PARS_DATA
from data_base_driver.input_output.data_keys_parser.io_pars_keys import IO_PARS_KEYS
from data_base_driver.input_output.data_keys_parser.io_pars_rels import IO_PARS_RELS
from data_base_driver.input_output.io_org_sql import IO_ORG_SQL
from data_base_driver.input_output.io_permit import IO_PERMIT, permit


###########################################
# БАЗОВЫЙ КЛАСС ВВОДА/ВЫВОДА
###########################################
class IO():
    ORG_SQL = 0
    ORG_SPH = 1

    def __init__(self, group_id):
        self.group_id = group_id
        self.is_admin = group_id == 0

        # органайзеры доступа к хранилищам данных
        self.io_org = {
            self.ORG_SQL: IO_ORG_SQL(),
            # self.ORG_SPH: ... ,
        }

    def __del__(self):
        del self.io_org[self.ORG_SQL]

    def set(self, obj, data):
        try:
            data_pars = IO_PARS_DATA(obj=obj, data=data)
            # проверка доступа obj
            if not self.is_admin and \
                    data_pars.obj_id != DAT_SYS_OBJ.ID_REL and \
                    data_pars.rec_id and \
                    not permit(
                        write=True,
                        io_org_item=self.io_org[self.ORG_SQL],
                        obj_id=data_pars.obj_id,
                        rec_id=data_pars.rec_id,
                        group_id=self.group_id,
                    ): raise Exception('Access denied')

            # проверка доступа rel
            if not self.is_admin and \
                    data_pars.obj_id == DAT_SYS_OBJ.ID_REL and \
                    not (
                            permit(
                                write=True,
                                io_org_item=self.io_org[self.ORG_SQL],
                                obj_id=data_pars.row_dic[0][DAT_REL.OBJ_ID_1],
                                rec_id=data_pars.row_dic[0][DAT_REL.REC_ID_1],
                                group_id=self.group_id,
                            ) and \
                            permit(
                                write=True,
                                io_org_item=self.io_org[self.ORG_SQL],
                                obj_id=data_pars.row_dic[0][DAT_REL.OBJ_ID_2],
                                rec_id=data_pars.row_dic[0][DAT_REL.REC_ID_2],
                                group_id=self.group_id,
                            )): raise Exception('Access denied')

            # запись
            self.io_org[self.ORG_SQL].set(data_pars=data_pars)
            return True, int(data_pars.rec_id) if data_pars.rec_id else data_pars.rec_id
        except Exception as e:
            # logging.getLogger(settings.PROJECT_LOG_MAIN).error(str(e))
            return False, str(e)

    # ГЕНЕРАТОР
    # item: (id, key_id, val, [dat])
    # желательно указывать ids
    def get_obj(self, obj, keys=[], ids=[], ids_max_block=None, where_dop_row=[]):
        try:
            keys_pars = IO_PARS_KEYS(obj=obj, keys=keys)
            permit = IO_PERMIT(io_org_item=self.io_org[self.ORG_SQL], obj_id=keys_pars.obj_id, ids=ids,
                               ids_max_block=ids_max_block) if not self.is_admin else None
            # выборка всех записей без проверки ограничений доступа
            for item in self.io_org[self.ORG_SQL].get_obj(keys_pars=keys_pars, ids=ids, ids_max_block=ids_max_block,
                                                          where_dop_row=where_dop_row):
                # item = (31, 30302, 0), (31, 30303, 'Тест 2'), ...
                # только разрешенные записи
                if self.is_admin or permit.valid(write=False, group_id=self.group_id, rec_id=item[0]): yield item
        except Exception as e:
            # logging.getLogger(settings.PROJECT_LOG_MAIN).error(str(e))
            raise e

    # ГЕНЕРАТОР
    # ПРОВЕРКА ЗАПИСЕЙ НА ПОВТОРЫ (ВАРИАНТЫ 1,2) НЕ ВЕДЕТСЯ
    # item: (key_id, dat, obj_id_1, rec_id_1, obj_id_2, rec_id_2)
    def get_rel(self, keys=[], obj_rel_1=None, obj_rel_2=None, where_dop=[]):
        try:
            keys_pars = IO_PARS_KEYS(obj=DAT_SYS_OBJ.ID_REL, keys=keys)
            rels_pars = IO_PARS_RELS(obj_rel_1=obj_rel_1, obj_rel_2=obj_rel_2)
            for item in self.io_org[self.ORG_SQL].get_rel(keys_pars=keys_pars, rels_pars=rels_pars,
                                                          where_dop=where_dop):
                # оставить только разрешенные записи
                if self.is_admin or ( \
                                permit(
                                    write=False,
                                    io_org_item=self.io_org[self.ORG_SQL],
                                    obj_id=item[2],
                                    rec_id=item[3],
                                    group_id=self.group_id,
                                ) and \
                                permit(
                                    write=False,
                                    io_org_item=self.io_org[self.ORG_SQL],
                                    obj_id=item[4],
                                    rec_id=item[5],
                                    group_id=self.group_id,
                                )): yield item

        except Exception as e:
            # logging.getLogger(settings.PROJECT_LOG_MAIN).error(str(e))
            raise e

    # ОТКЛЮЧЕНО ЗА НЕНАБНОСТЬЮ
    # # ЧИТАТЬ ДЕРЕВО ГЕОМЕТРИЙ С УЧЕТОМ РАЗРЕШЕНИЙ
    # # parent_id = 0 - верхний уровень
    # # ret = [ {id: , name: , icon: }, ... ]
    # def get_geometry_tree(self, parent_id, write=True):
    #     try:
    #         obj_id = DAT_SYS_OBJ.DUMP.to_id(val=DAT_SYS_OBJ.NAME_GEOMETRY)
    #         key_id_parent = DAT_SYS_KEY.DUMP.to_id(obj_id=obj_id, val=DAT_SYS_KEY.NAME_GEOMETRY_PARENT_ID)
    #         key_id_name = DAT_SYS_KEY.DUMP.to_id(obj_id=obj_id, val=DAT_SYS_KEY.NAME_GEOMETRY_NAME)
    #         key_id_icon = DAT_SYS_KEY.DUMP.to_id(obj_id=obj_id, val=DAT_SYS_KEY.NAME_GEOMETRY_ICON)

    #         keys = (key_id_parent, key_id_name, key_id_icon,)
    #         keys_pars = IO_PARS_KEYS(obj=obj_id, keys=keys)

    #         # выборка всех записей без проверки ограничений доступа
    #         # tmp = [{id: ..., parent_id: ..., name_id: ...}, ... ]
    #         tmp = {}
    #         for item in self.io_org[self.ORG_SQL].get_obj(keys_pars=keys_pars, ids=[]):
    #             # item = (31, 30302, 0), (31, 30303, 'Тест 2'), ...
    #             # только разрешенные записи
    #             if self.is_admin or permit(
    #                     write=write,
    #                     io_org_item=self.io_org[self.ORG_SQL],
    #                     obj_id=obj_id,
    #                     rec_id=item[0],
    #                     group_id=self.group_id,
    #             ):
    #                 val = tmp.get(item[0], {})
    #                 val[item[1]] = item[2]
    #                 tmp[item[0]] = val

    #         # только с заданным родителем
    #         ret = []
    #         for tmp_item in tmp:
    #             if tmp[tmp_item][key_id_parent] == parent_id:
    #                 ret.append({
    #                     'id': tmp_item,
    #                     'name': tmp[tmp_item][key_id_name],
    #                     'icon': tmp[tmp_item][key_id_icon],
    #                 })
    #         return ret

    #     except Exception as e:
    #         # logging.getLogger(settings.PROJECT_LOG_MAIN).error(str(e))
    #         raise e
