from datetime import datetime, timedelta
from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_OWNER
from data_base_driver.input_output.data_keys_parser.io_pars_keys import IO_PARS_KEYS


DEBUG = False

# доступ одной записи obj_id.rec_id для группы group_id
permit = lambda write, io_org_item, obj_id, rec_id, group_id: \
    IO_PERMIT(io_org_item=io_org_item, obj_id=obj_id, ids=(int(rec_id),)).valid(write=write, group_id=group_id,
                                                                                rec_id=rec_id)

# ids = list int or list str
class IO_PERMIT():
    def __init__(self, io_org_item, obj_id, ids, ids_max_block=None):
        if DEBUG:
            print('\nIO_PERMIT.ini:', '\nobj_id =', obj_id, '\nids =', ids)

        # разрешения на доступ: множества разрешенных групп {88: {25}, 45: {24, 33}}
        self.permits_rw = {}
        self.permits_ro = {}
        self.ids = [str(item) for item in ids]
        self.skip = True
        obj_id = int(obj_id)

        # если объект не защищаемый
        if obj_id not in DAT_SYS_KEY.DUMP.owners.keys(): return

        # permits - список всех установленных разрешений: [(88, 'owner_add_rw', 23, datetime.datetime(2019, 1, 2, 0, 0)), ...]
        keys_owner = DAT_SYS_KEY.DUMP.owners[obj_id]  # [10000, 10001, 10002, 10003]
        key_pars = IO_PARS_KEYS(obj=obj_id, keys=keys_owner)
        permits = tuple(io_org_item.get_obj(keys_pars=key_pars, ids=ids, ids_max_block=ids_max_block, where_dop_row=[]))
        permits = list(map(lambda x: (  # begin           [(88, 10000, '23', '2019-01-02'), ...]
            x[0],  # key_id
            DAT_SYS_KEY.NAME_OWNER_LIST[keys_owner.index(x[1])],  # 10000        -> 'owner_add_rw'
            int(x[2]),  # '23'         -> 23
            datetime.strptime(x[3] if x[3] != None else '2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
        # '2019-01-02' -> datetime.datetime(2019, 1, 2, 0, 0)
        ), permits))  # end             [(88, 'owner_add_rw', 23, datetime.datetime(2019, 1, 2, 0, 0)), ...]
        permits.sort(key=lambda x: x[3])  # сортировать по возрастанию даты

        # сформировать разрешения на доступ
        for item in permits:
            groups_rw = self.permits_rw.get(item[0], set())
            groups_ro = self.permits_ro.get(item[0], set())
            if item[1] == DAT_SYS_KEY.NAME_OWNER_ADD_RW:
                groups_rw.add(item[2])
            elif item[1] == DAT_SYS_KEY.NAME_OWNER_ADD_RO:
                groups_ro.add(item[2])
            elif item[1] == DAT_SYS_KEY.NAME_OWNER_ADD_RO_LIMIT:
                # only data
                # if (item[3]+timedelta(days=7)).datetime() >= datetime.now().datetime(): groups_ro.add(item[2])
                if (item[3] + timedelta(days=7)) >= datetime.now(): groups_ro.add(item[2])
            elif item[1] == DAT_SYS_KEY.NAME_OWNER_DEL:
                groups_rw.discard(item[2]); groups_ro.discard(item[2])
            elif item[1] == DAT_SYS_KEY.NAME_OWNER_VISIBLE:
                continue
            else:
                raise Exception('Error key_id: ' + str(item))
            self.permits_rw[item[0]] = groups_rw
            self.permits_ro[item[0]] = groups_ro

        # удалить пустые множества
        for item in dict(self.permits_rw):  # for по копии, т.к. нельзя удалять
            if len(self.permits_rw[item]) == 0: del self.permits_rw[item]
        for item in dict(self.permits_ro):
            if len(self.permits_ro[item]) == 0: del self.permits_ro[item]

        # имеет ли смысл проверка
        self.skip = (len(self.permits_rw) + len(self.permits_ro)) == 0

    # доступ группы group_id к записи rec_id
    # write - доступ на запись и чтение, иначе только чтение
    # НЕТ СМЫСЛА УСТАНАВЛИВАТЬ RO ПРИ ОТСУТСТВИИ RW
    def valid(self, write, group_id, rec_id):
        if DEBUG:
            print('\nIO_PERMIT.valid:', '\nwrite =', write, '\ngroup_id =', group_id, '\nrec_id =', rec_id)

        # разрешения не установлены - доступ есть
        if self.skip: return True

        # приведение типов
        group_id = int(group_id)
        rec_id = int(rec_id)

        # id не заявлялся при инициализации - ошибка
        if not str(rec_id) in self.ids: raise Exception('Error rec_id: ' + str(rec_id))

        # разрешенные группы для записи rec_id
        groups_rw = self.permits_rw.get(rec_id, set())
        groups_ro = self.permits_ro.get(rec_id, set())

        # разрешения не установлены -> запись не защищаемая -> доступ есть
        if len(groups_rw) == 0 and len(groups_ro) == 0: return True

        # разрешение следует из дерева владельцев
        if DEBUG: print('\nwrite:', write, '/ group_id:', group_id, '/ rec_id:', rec_id)

        # проверка: чтение/запись
        ret = DAT_OWNER.DUMP.valid_group_rw(group_id=group_id, valids_id=groups_rw)
        if DEBUG: print('valid rw:', groups_rw, ret)

        # проверка: только чтение
        if not write:
            # чтение можеть быть разрешено ИЛИ в ro, ИЛИ в rw
            if not ret:
                ret = DAT_OWNER.DUMP.valid_group_ro(group_id=group_id, valids_id=groups_ro)
                if DEBUG: print('valid ro:', groups_ro, ret)

        if DEBUG: print('ret:', ret)
        return ret
