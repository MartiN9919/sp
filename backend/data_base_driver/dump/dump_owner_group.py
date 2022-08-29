import threading
import time
from data_base_driver.constants.const_dat import DAT_OWNER_USERS, DAT_OWNER_GROUPS, DAT_OWNER_BASE, \
    DAT_OWNER_GROUPS_REL
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.dump.transform_functions import tuple_to_dict_many, dict_filter


##################################################################################
# DAT_OWNER_GROUPS.DUMP
##################################################################################

class DUMP_OWNER222:
    def __init__(self, refreshDelay=60 * 15):  # refreshDelay - время хранения кэша, в секундах
        self.key_chain = 'chain'
        self.key_owner_id = 'owner_id'
        self.dump_users = None
        self.dump_groups = None
        self.dump_groups_rw = None
        self.dump_groups_ro = None
        self.dump_rel = None
        self.refreshDelay = refreshDelay
        self.refreshTime = time.time() - 1
        self._lock = threading.Lock()
        self._refresh_()

    def _refresh_(self, force=False):
        GROUP_RW = 'group_rw'
        GROUP_RO = 'group_ro'
        def _rel_( id):
            _groups_rw = set()
            _groups_ro = set()

            for rel in self.dump_groups_rel:
                 if rel[DAT_OWNER_GROUPS_REL.PARENT_ID] == id:
                     (_groups_rw2, _groups_ro2) = _rel_(rel[DAT_OWNER_GROUPS_REL.NODE_ID])
                     if rel[DAT_OWNER_GROUPS_REL.READ_ONLY]:
                        _groups_ro2.add(rel[DAT_OWNER_GROUPS_REL.NODE_ID])
                        _groups_ro2 = _groups_ro2 | _groups_rw2
                        _groups_rw2 = set()
                     else:
                        _groups_rw2.add(rel[DAT_OWNER_GROUPS_REL.NODE_ID])

                     _groups_rw = _groups_rw | _groups_rw2
                     _groups_ro = _groups_ro | _groups_ro2


            _groups_ro.difference_update(_groups_rw)

            return (_groups_rw, _groups_ro)



        GROUP_RW = 'group_rw'
        GROUP_RO = 'group_ro'
        if not force and (self.refreshTime > time.time()): return
        with self._lock:
            # USERS
            dat = db_sql(
                sql=
                "SELECT " +
                DAT_OWNER_USERS.ID + "," +
                DAT_OWNER_USERS.OWNER_GROUPS_ID + " " +
                "FROM " +
                DAT_OWNER_USERS.TABLE_SHORT + " " +
                "WHERE " +
                DAT_OWNER_USERS.ENABLED + "=1",
                wait=True,
                read=True
            )
            self.dump_users = tuple_to_dict_many(dat, [
                DAT_OWNER_USERS.ID,
                DAT_OWNER_USERS.OWNER_GROUPS_ID,
            ])

            # GROUPS
            dat = db_sql(
                sql=
                "SELECT " +
                DAT_OWNER_GROUPS.ID + "," +
                DAT_OWNER_GROUPS.TITLE + "," +
                DAT_OWNER_GROUPS.DESCRIPT + " " +
                "FROM " +
                DAT_OWNER_GROUPS.TABLE,
                wait=True,
                read=True
            )
            self.dump_groups = tuple_to_dict_many(dat, [
                DAT_OWNER_GROUPS.ID,
                DAT_OWNER_GROUPS.TITLE,
                DAT_OWNER_GROUPS.DESCRIPT,
            ])

            # GROUPS_REL
            dat = db_sql(
                sql=
                "SELECT " +
                DAT_OWNER_GROUPS_REL.NODE_ID + "," +
                DAT_OWNER_GROUPS_REL.PARENT_ID + "," +
                DAT_OWNER_GROUPS_REL.READ_ONLY + "," +
                DAT_OWNER_GROUPS_REL.DESCRIPT + " " +
                "FROM " +
                DAT_OWNER_GROUPS_REL.TABLE,
                wait=True,
                read=True
            )
            self.dump_groups_rel = tuple_to_dict_many(dat, [
                DAT_OWNER_GROUPS_REL.NODE_ID,
                DAT_OWNER_GROUPS_REL.PARENT_ID,
                DAT_OWNER_GROUPS_REL.READ_ONLY,
                DAT_OWNER_GROUPS_REL.DESCRIPT,
            ])

            for item in self.dump_groups:
                (groups_rw, groups_ro) =_rel_( item[DAT_OWNER_GROUPS.ID])

                ###

                item[GROUP_RW] = groups_rw
                item[GROUP_RO] = groups_ro



            print(self.dump_groups)

            # актуальность дампа
            self.refreshTime = time.time() + self.refreshDelay

    def update(self):
        self.refreshTime = time.time() - 1

    def __child_nodes__(self, list_src):
        ret_total = {}

        def step(parent_id):
            ret_step = []
            for item in filter(lambda x: x[DAT_OWNER_BASE.PARENT_ID] == parent_id, list_src):
                ret_step += [item[DAT_OWNER_BASE.ID]]
                ret_step += step(parent_id=item[DAT_OWNER_BASE.ID])
            if len(ret_step) > 0: ret_total[parent_id] = ret_step
            return ret_step

        step(parent_id=0)
        return ret_total

    # проверить доступ пользователя user_id к данным хотя бы одной из групп valids_id
    valid_io_user = lambda self, user_id, valids_id: self.valid_io_group(group_id=self.get_group(user_id),
                                                                         valids_id=valids_id)

    # проверить доступ группы group_id к данным хотя бы одной из групп valids_id
    def valid_io_group(self, group_id, valids_id):
        self._refresh_()

        # если группа прямо указана в списке разрешенных - доступ есть
        if group_id in valids_id: return True

        # список разрешенных групп: упоминающихся И по регионам И по линиям ОДНОВРЕМЕННО
        enabled_groups = self.dump_groups.get(group_id, {}).get(DAT_OWNER_GROUPS.GROUPS_ID, [])
        if len(enabled_groups) <= 1: return False

        for item_valid in valids_id:
            if item_valid in enabled_groups:
                return True
        return False

    # получить group_id
    def get_group(self, user_id):
        self._refresh_()
        rec = dict_filter(list_dict=self.dump_users, list_key_val=(DAT_OWNER_USERS.ID, user_id), only_first=True)
        if len(rec) != 1: raise Exception('Unknow user_id: ' + str(user_id))
        return rec[0][DAT_OWNER_USERS.OWNER_GROUPS_ID]

    def get_groups_list(self):
        return [{'id': group, 'title': self.dump_groups[group]['title']} for group in self.dump_groups]
