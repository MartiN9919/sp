
import time
import copy

from   pprint                       import pprint
from   lib.sys                      import tuple_to_dict_many, dict_filter
from   lib.db.const.const_connect   import CONNECT
from   lib.db.const.const_dat       import DAT_OWNER_USERS, DAT_OWNER_GROUPS, DAT_OWNER_BASE, DAT_OWNER_REGIONS, DAT_OWNER_LINES
from   lib.db.connect.connect_mysql import DB_sql


##################################################################################
# DAT_OWNER_GROUPS.DUMP
##################################################################################
class DUMP_OWNER:
    def __init__(self, refreshDelay = 60*15):    # refreshDelay - время хранения кэша, в секундах
        self.key_id        = DAT_OWNER_REGIONS.ID
        self.key_parent_id = DAT_OWNER_REGIONS.PARENT_ID
        self.key_chain     = 'chain'
        self.key_owner_id  = 'owner_id'
        self.dump_users    = None
        self.dump_groups   = None
        self.dump_regions  = None
        self.dump_lines    = None
        self.refreshDelay  = refreshDelay
        self.refreshTime   = time.time()-1
        self._refresh_()

    def _refresh_(self, force=False):
        if not force and (self.refreshTime > time.time()): return
        db  = DB_sql(database=CONNECT.DATA)

        # USERS
        dat = db.execute(
            sql=
                "SELECT "+
                    DAT_OWNER_USERS.ID              +","+
                    DAT_OWNER_USERS.OWNER_GROUPS_ID +" "+
                "FROM "+
                    DAT_OWNER_USERS.TABLE+" "+
                "WHERE "+
                    DAT_OWNER_USERS.ENABLED+"=1",
            wait=True,
            read=True
        )
        self.dump_users = tuple_to_dict_many(dat, [
            DAT_OWNER_USERS.ID,
            DAT_OWNER_USERS.OWNER_GROUPS_ID,
        ])

        # GROUPS
        dat = db.execute(
            sql=
                "SELECT "+
                    DAT_OWNER_GROUPS.ID              +","+
                    DAT_OWNER_GROUPS.OWNER_REGIONS_ID+","+
                    DAT_OWNER_GROUPS.OWNER_LINES_ID  +","+
                    DAT_OWNER_GROUPS.TITLE           +","+
                    DAT_OWNER_GROUPS.DESCRIPT        +" "+
                "FROM "+
                    DAT_OWNER_GROUPS.TABLE,
            wait=True,
            read=True
        )
        self.dump_groups = tuple_to_dict_many(dat, [
            DAT_OWNER_GROUPS.ID,
            DAT_OWNER_GROUPS.OWNER_REGIONS_ID,
            DAT_OWNER_GROUPS.OWNER_LINES_ID,
            DAT_OWNER_GROUPS.TITLE,
            DAT_OWNER_GROUPS.DESCRIPT,
        ])

        # REGIONS (TEMP)
        dat = db.execute(
            sql=
                "SELECT "+
                    DAT_OWNER_REGIONS.ID       +","+
                    DAT_OWNER_REGIONS.PARENT_ID+" "+
                "FROM "+
                    DAT_OWNER_REGIONS.TABLE,
            wait=True,
            read=True
        )
        self.dump_regions = tuple_to_dict_many(dat, [
            DAT_OWNER_REGIONS.ID,
            DAT_OWNER_REGIONS.PARENT_ID,
        ])


        # LINES (TEMP)
        dat = db.execute(
            sql=
                "SELECT "+
                    DAT_OWNER_LINES.ID       +","+
                    DAT_OWNER_LINES.PARENT_ID+" "+
                "FROM "+
                    DAT_OWNER_LINES.TABLE,
            wait=True,
            read=True
        )
        self.dump_lines = tuple_to_dict_many(dat, [
            DAT_OWNER_LINES.ID,
            DAT_OWNER_LINES.PARENT_ID,
        ])


        TMP_REGIONS_ID = 'tmp_regions_id'
        TMP_LINES_ID   = 'tmp_lines_id'
        # списки REGIONS/LINES в self.dump_groups
        tmp_regions = self.__child_nodes__(list_src=self.dump_regions)  # {1: [2,3,...], ...}
        tmp_lines   = self.__child_nodes__(list_src=self.dump_lines)    # {1: [2,3,...], ...}
        for item_group in self.dump_groups:                             # item_group = {'id': 1, 'owner_regions_id': 1, 'owner_lines_id': 1, ...}
            item_group[TMP_REGIONS_ID] = [item_group[DAT_OWNER_GROUPS.OWNER_REGIONS_ID]]+tmp_regions.get(item_group[DAT_OWNER_GROUPS.OWNER_REGIONS_ID], [])
            item_group[TMP_LINES_ID  ] = [item_group[DAT_OWNER_GROUPS.OWNER_LINES_ID  ]]+tmp_lines  .get(item_group[DAT_OWNER_GROUPS.OWNER_LINES_ID  ], [])
        # списки child_groups в self.dump_groups
        for item_group in self.dump_groups:
            # индексы групп регионов и линий в индексы групп
            group_regions = list(map(lambda x: x[DAT_OWNER_GROUPS.ID], filter(lambda x: x[DAT_OWNER_GROUPS.OWNER_REGIONS_ID] in item_group[TMP_REGIONS_ID], self.dump_groups)))
            group_lines   = list(map(lambda x: x[DAT_OWNER_GROUPS.ID], filter(lambda x: x[DAT_OWNER_GROUPS.OWNER_LINES_ID  ] in item_group[TMP_LINES_ID  ], self.dump_groups)))
            # индекс группы принимается при его упоминании И в индесе регионов И в индексе линий ОДНОВРЕМЕННО
            item_group[DAT_OWNER_GROUPS.GROUPS_ID] = list(set(group_regions) & set(group_lines))
        # словарь словарей по id
        self.dump_groups = { item[DAT_OWNER_GROUPS.ID]: {
            DAT_OWNER_GROUPS.GROUPS_ID: item[DAT_OWNER_GROUPS.GROUPS_ID],
            DAT_OWNER_GROUPS.TITLE:     item[DAT_OWNER_GROUPS.TITLE],
            DAT_OWNER_GROUPS.DESCRIPT:  item[DAT_OWNER_GROUPS.DESCRIPT],
            } for item in self.dump_groups }
        # удалить ненужное
        del self.dump_regions
        del self.dump_lines

        # актуальность дампа
        self.refreshTime = time.time()+self.refreshDelay



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
    valid_user = lambda self, user_id, valids_id: self.valid_group(group_id=self.get_group(user_id), valids_id=valids_id)
    # проверить доступ группы group_id к данным хотя бы одной из групп valids_id
    def valid_group(self, group_id, valids_id):
        self._refresh_()

        # НЕДОПУСТИМО, т.к. чтение может быть разрешено через ro={} при запрете через rw
        # # если списка разрешенных групп нет - доступ есть
        # if len(valids_id)==0: return True

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
        if len(rec)!=1: raise Exception('Unknow user_id: '+str(user_id))
        return rec[0][DAT_OWNER_USERS.OWNER_GROUPS_ID]

