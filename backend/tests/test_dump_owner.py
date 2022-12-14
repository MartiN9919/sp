
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR+'/')
print(BASE_DIR)

from typing import List, Dict
import data_base_driver.constants.const_dat as dat
from data_base_driver.dump.transform_functions import tuple_to_dict_many

import pytest


def db_sql_mock(table_name: str) -> List[Dict]:
    # USERS
    if table_name == dat.DAT_OWNER_USERS.TABLE:
        val = ()
        return tuple_to_dict_many(val, [
            dat.DAT_OWNER_USERS.ID,
            dat.DAT_OWNER_USERS.OWNER_GROUPS_ID,
        ])

    # LINES (TEMP)
    if table_name == dat.DAT_OWNER_LINES.TABLE:
        val = (
            (1, 0),
            (2, 1),
            (3, 30),
            (4, 2),
            (5, 2),
            (30, 2),
        )
        return tuple_to_dict_many(val, [
            dat.DAT_OWNER_LINES.ID,
            dat.DAT_OWNER_LINES.PARENT_ID,
        ])

    # GROUPS
    if table_name == dat.DAT_OWNER_GROUPS.TABLE:
        val = (
            (1, 1, 'Admin'),
            (22, 2, 'GPK A'),
            (23, 3, 'GPK O'),
            (24, 4, 'GPK I'),
            (25, 5, 'GPK D'),
            (44, 4, 'Sm I'),
        )
        return tuple_to_dict_many(val, [
            dat.DAT_OWNER_GROUPS.ID,
            dat.DAT_OWNER_GROUPS.OWNER_LINES_ID,
            dat.DAT_OWNER_GROUPS.TITLE,
        ])

    # GROUPS_REL (TEMP)
    if table_name == dat.DAT_OWNER_GROUPS_REL.TABLE:
        val = (
            (22, 1, 1),
            (23, 22, 0),
            (23, 1, 0),
            (44, 23, 1),
        )
        return tuple_to_dict_many(val, [
            dat.DAT_OWNER_GROUPS_REL.NODE_ID,
            dat.DAT_OWNER_GROUPS_REL.PARENT_ID,
            dat.DAT_OWNER_GROUPS_REL.READ_ONLY,
        ])


    raise ValueError(f"Error table name {table_name}")


# def fun_sql(sql: str, wait: bool = True, read: bool = True):
#     return []

D = dat.DUMP_OWNER(fun_sql = db_sql_mock)
print(D)

# s = D.get_groups()
# print(s)

# s = D.get_group(4)
# print(
#     D.valid_group(
#         group_id=22,
#         valids_id=[33]
#     )
# )

# print(
#     D.valid_line(
#         group_id=23,
#         line_id=3
#     )
# )


# def test2():
#     assert 8 == 8


# # @pytest.mark.parametrize(
# #     "param1,param2",
# #     [
# #         ("a", "b"),
# #         ("d", "d"),
# #     ],
# # )

# @pytest.fixture()
# def test_inc1():
#     print(1)
#     yield
#     print(2)

# def test2():
#     assert tst.mfun(2, 6) == 8


# def f():
#     raise SystemExit(1)


# def test_mytest():
#     with pytest.raises(SystemExit):
#         f()


# # class Test_mfun():
# #     @pytest.fixture
# #     def some_data(self):
# #         return 2


# #     def test_decrement(self):
# #         assert tst.mfun(2, 5) == 4

# #     # def test2(self):
# #     #     assert tst.mfun(2, 6) == 8
