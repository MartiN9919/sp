
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR+'/../')


from dump_owner_group import DUMP_OWNER222
import pytest

D = DUMP_OWNER222()
s = D.get_group(4)
print(
    D.valid_group(
        group_id=22,
        valids_id=[33]
    )
)

print(
    D.valid_line(
        group_id=23,
        line_id=3
    )
)


def test2():
    assert 8 == 8


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
