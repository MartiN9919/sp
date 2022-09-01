import threading
import time
from typing import List
from data_base_driver.constants.const_dat import DAT_OWNER_USERS, DAT_OWNER_GROUPS, \
    DAT_OWNER_LINES, DAT_OWNER_GROUPS_REL
from data_base_driver.connect.connect_mysql import db_sql
from data_base_driver.dump.transform_functions import tuple_to_dict_many, dict_filter


##################################################################################
# DAT_OWNER_GROUPS.DUMP
##################################################################################

def db_sql_dump_owner(sql: str, wait: bool = True, read: bool = True):
    return db_sql(sql=sql, wait=wait, read=read)


class DUMP_OWNER:
    def __init__(self, refreshDelay=60 * 15, fun_sql=db_sql_dump_owner):  # refreshDelay - время хранения кэша, в секундах
        self.fun_sql = fun_sql
        self.dump_users = None
        self.dump_groups = None
        self.dump_lines = None
        self.refreshDelay = refreshDelay
        self.refreshTime = time.time() - 1
        self._lock = threading.Lock()
        self._refresh_()

    def _refresh_(self, force=False):
        LINES = 'lines'    # ключ dump_lines: список видимых линий

        def _group_rel_(id):
            """построить DAT_OWNER_GROUPS.GROUPS_RW/RO"""
            groups_rw = set()
            groups_ro = set()

            # анализ потомков родителя id
            for rel in self.dump_rel:
                if rel[DAT_OWNER_GROUPS_REL.PARENT_ID] == id:
                    (groups_rw2, groups_ro2) = _group_rel_(rel[DAT_OWNER_GROUPS_REL.NODE_ID])
                    if rel[DAT_OWNER_GROUPS_REL.READ_ONLY]:
                        groups_ro2.add(rel[DAT_OWNER_GROUPS_REL.NODE_ID])
                        groups_ro2 = groups_ro2 | groups_rw2   # ro узлов потомка передается родителю как ro
                        groups_rw2 = set()
                    else:
                        groups_rw2.add(rel[DAT_OWNER_GROUPS_REL.NODE_ID])

                    groups_rw = groups_rw | groups_rw2
                    groups_ro = groups_ro | groups_ro2

            # родитель имеет потомков ro и rw с одним id -> оставить rw
            groups_ro.difference_update(groups_rw)
            return (groups_rw, groups_ro)


        def _line_rel_(id):
            """построить DAT_OWNER_GROUPS.LINES (group dump_rel не влияет)"""
            lines = set()

            # найти запись в dump_lines
            line_rec = dict_filter(
                list_dict=self.dump_lines,
                list_key_val=(DAT_OWNER_LINES.ID, id),
                only_first=True
            )
            if len(line_rec) != 1: raise Exception('Unknow line id: ' + str(id))

            # добавить линию
            lines.add(line_rec[0][DAT_OWNER_LINES.ID])

            # анализ потомков родителя id
            for rel in self.dump_lines:
                if rel[DAT_OWNER_LINES.PARENT_ID] == id:
                    lines = lines | _line_rel_(rel[DAT_OWNER_LINES.ID])

            return lines


        if not force and (self.refreshTime > time.time()): return
        with self._lock:
            # USERS
            dat = self.fun_sql(
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

            # LINES (TEMP)
            dat = self.fun_sql(
                sql=
                "SELECT " +
                DAT_OWNER_LINES.ID + "," +
                DAT_OWNER_LINES.PARENT_ID + " " +
                "FROM " +
                DAT_OWNER_LINES.TABLE,
                wait=True,
                read=True
            )
            self.dump_lines = tuple_to_dict_many(dat, [
                DAT_OWNER_LINES.ID,
                DAT_OWNER_LINES.PARENT_ID,
            ])

            # GROUPS
            dat = self.fun_sql(
                sql=
                "SELECT " +
                DAT_OWNER_GROUPS.ID + "," +
                DAT_OWNER_GROUPS.OWNER_LINES_ID + "," +
                DAT_OWNER_GROUPS.TITLE + " " +
                "FROM " +
                DAT_OWNER_GROUPS.TABLE,
                wait=True,
                read=True
            )
            self.dump_groups = tuple_to_dict_many(dat, [
                DAT_OWNER_GROUPS.ID,
                DAT_OWNER_GROUPS.OWNER_LINES_ID,
                DAT_OWNER_GROUPS.TITLE,
            ])

            # GROUPS_REL (TEMP)
            dat = self.fun_sql(
                sql=
                "SELECT " +
                DAT_OWNER_GROUPS_REL.NODE_ID + "," +
                DAT_OWNER_GROUPS_REL.PARENT_ID + "," +
                DAT_OWNER_GROUPS_REL.READ_ONLY + " " +
                "FROM " +
                DAT_OWNER_GROUPS_REL.TABLE,
                wait=True,
                read=True
            )
            self.dump_rel = tuple_to_dict_many(dat, [
                DAT_OWNER_GROUPS_REL.NODE_ID,
                DAT_OWNER_GROUPS_REL.PARENT_ID,
                DAT_OWNER_GROUPS_REL.READ_ONLY,
            ])

            # построить dump_lines.LINES
            for item in self.dump_lines:
                item[LINES] =_line_rel_(item[DAT_OWNER_LINES.ID])

            # построить DAT_OWNER_GROUPS.GROUPS_RW/RO, DAT_OWNER_GROUPS.LINES
            for item in self.dump_groups:
                (
                    item[DAT_OWNER_GROUPS.GROUPS_RW],
                    item[DAT_OWNER_GROUPS.GROUPS_RO]
                ) =_group_rel_(item[DAT_OWNER_GROUPS.ID])

                # найти запись в dump_lines
                line_rec = dict_filter(
                    list_dict=self.dump_lines,
                    list_key_val=(DAT_OWNER_LINES.ID, item[DAT_OWNER_GROUPS.OWNER_LINES_ID]),
                    only_first=True
                )
                if len(line_rec) != 1: raise Exception('Unknow line in group: ' + str(id))
                item[DAT_OWNER_GROUPS.LINES] = line_rec[0][LINES]

                # удалить ненужное
                del item[DAT_OWNER_GROUPS.OWNER_LINES_ID]

            # удалить ненужное
            del self.dump_lines
            del self.dump_rel

            # актуальность дампа
            self.refreshTime = time.time() + self.refreshDelay


    def update(self):
        """принудительно обновить дамп"""
        self.refreshTime = time.time() - 1


    valid_group = lambda self, group_id, valids_id: self.valid_group_rw(group_id, valids_id) | self.valid_group_ro(group_id, valids_id)
    valid_group_rw = lambda self, group_id, valids_id: self.__valid_group__(group_id, valids_id, DAT_OWNER_GROUPS.GROUPS_RW)
    valid_group_ro = lambda self, group_id, valids_id: self.__valid_group__(group_id, valids_id, DAT_OWNER_GROUPS.GROUPS_RO)
    def __valid_group__(self, group_id: int, valids_id: List[int], groups_field: str) -> bool:
        """проверить доступ группы group_id к данным хотя бы одной из групп valids_id"""
        self._refresh_()

        # доступ есть если: группа прямо указана в списке разрешенных
        if group_id in valids_id: return True

        # список доступных групп
        enabled_groups = next((x[groups_field] for x in self.dump_groups if x[DAT_OWNER_GROUPS.ID] == group_id), {})
        if len(enabled_groups) == 0: return False

        for valid_id in valids_id:
            if valid_id in enabled_groups:
                return True
        return False


    def valid_line(self, group_id: int, line_id=None) -> bool:
        """проверить доступ группы group_id к линии line_id"""
        self._refresh_()

        # если линия не задана - доступ есть всегда
        if line_id is None: return True

        # список разрешенных линий для группы
        enabled_lines = next((x[DAT_OWNER_GROUPS.LINES] for x in self.dump_groups if x[DAT_OWNER_GROUPS.ID] == group_id), {})
        return line_id in enabled_lines


    def get_group(self, user_id: int) -> int:
        """получить group_id"""
        self._refresh_()
        rec = dict_filter(list_dict=self.dump_users, list_key_val=(DAT_OWNER_USERS.ID, user_id), only_first=True)
        if len(rec) != 1: raise Exception('Unknow user_id: ' + str(user_id))
        return rec[0][DAT_OWNER_USERS.OWNER_GROUPS_ID]


    def get_groups(self):
        """получить список групп {group_id, title}"""
        return [{
            DAT_OWNER_GROUPS.ID: group[DAT_OWNER_GROUPS.ID],
            DAT_OWNER_GROUPS.TITLE: group[DAT_OWNER_GROUPS.TITLE],
        } for group in self.dump_groups]
