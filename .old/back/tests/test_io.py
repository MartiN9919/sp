# -*- coding: utf-8 -*-

# pytest -v -vv -l -s -m io

import test_ini_common
import test_ini_django
import pytest

from   lib.db.const.const_dat          import DAT_SYS_OBJ, DAT_SYS_KEY
from   lib.db.io.io_class              import IO
from   lib.db.connect.connect_mysql    import db_sql
from   datetime                        import datetime, timedelta



@pytest.mark.io
class TestIO:
    OWNER           = 54

    TEST_REL_1      = (1,     'test_rel_1')
    TEST_REL_2      = (2,     'test_rel_2')
    TEST_FREE_1     = (3,     'test_free_1')
    TEST_FILE_COL_1 = (15011, 'path')               # str
    TEST_FILE_COL_2 = (15010, 'type')               # int
    TEST_FILE_ROW_1 = (4,     'test_file_row_1')
    TEST_FILE_ROW_2 = (5,     'test_file_row_2')


    def setup_class(cls):
        cls.io = IO(group_id=cls.OWNER, debug=False)
        cls.free(cls)
        cls.ini(cls)

    def teardown_class(cls):
        cls.free(cls)

    def ini(cls):
        sql = "INSERT IGNORE "+DAT_SYS_KEY.TABLE+" ("+\
            DAT_SYS_KEY.ID       +", "+\
            DAT_SYS_KEY.OBJ_ID   +", "+\
            DAT_SYS_KEY.TYPE_VAL +", "+\
            DAT_SYS_KEY.NAME     +", "+\
            DAT_SYS_KEY.TITLE    +") VALUES "+\
            "("+str(cls.TEST_REL_1     [0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val='rel' ))+"', 'int', '"+cls.TEST_REL_1     [1]+"', ''), "+\
            "("+str(cls.TEST_REL_2     [0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val='rel' ))+"', 'int', '"+cls.TEST_REL_2     [1]+"', ''), "+\
            "("+str(cls.TEST_FREE_1    [0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val='free'))+"', 'str', '"+cls.TEST_FREE_1    [1]+"', ''), "+\
            "("+str(cls.TEST_FILE_ROW_1[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val='file'))+"', 'str', '"+cls.TEST_FILE_ROW_1[1]+"', ''), "+\
            "("+str(cls.TEST_FILE_ROW_2[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val='file'))+"', 'str', '"+cls.TEST_FILE_ROW_2[1]+"', '') "
        db_sql(sql=sql, wait=True, read=False, connection=cls.io.io_org[cls.io.ORG_SQL].io_sql.connection)
        DAT_SYS_KEY.DUMP._refresh_(force=True)

    def free(cls):
        cls.io.io_org[cls.io.ORG_SQL]._del_(obj='free',     rec_id=1)
        cls.io.io_org[cls.io.ORG_SQL]._del_(obj='file',     rec_id=1)
        cls.io.io_org[cls.io.ORG_SQL]._del_(obj='file',     rec_id=2)
        cls.io.io_org[cls.io.ORG_SQL]._del_(obj='file',     rec_id=3)
        cls.io.io_org[cls.io.ORG_SQL]._del_(obj='file',     rec_id=4)
        cls.io.io_org[cls.io.ORG_SQL]._del_(obj='point',    rec_id=1)
        cls.io.io_org[cls.io.ORG_SQL]._del_(obj='geometry', rec_id=1)
        sql = "DELETE FROM "+DAT_SYS_KEY.TABLE+" WHERE id<10"
        db_sql(sql=sql, wait=True, read=False, connection=cls.io.io_org[cls.io.ORG_SQL].io_sql.connection)
        DAT_SYS_KEY.DUMP._refresh_(force=True)

    def setup(self):                   pass #print ("basic setup into class")
    def teardown(self):                pass #print ("basic teardown into class")
    def setup_method(self, method):    pass #print ("method setup")
    def teardown_method(self, method): pass #print ("method teardown")



    # добавление временных объектов и их связей
    def test_add(self):
        # obj.free: add
        ret = self.io.set(obj='free', data=( ('id',1), (self.TEST_FREE_1[1], 'test_free_1'), ), )
        assert ret[0]

        # obj.file1: add
        ret = self.io.set(obj='file', data=( ('id',1), (self.TEST_FILE_COL_1[1],'test_path_1'), (self.TEST_FILE_ROW_1[0],'val11'), (DAT_SYS_KEY.NAME_OWNER_ADD_RW, self.OWNER, '2000-01-03'), ), )
        assert ret[0]

        # obj.file1: col change
        ret = self.io.set(obj='file', data=( ('id',1), (self.TEST_FILE_COL_1[1],'test_path_2'), ), )
        assert ret[0]

        # obj.file1: col add
        ret = self.io.set(obj='file', data=( ('id',1), (self.TEST_FILE_COL_2[1],1), ), )
        assert ret[0]

        # obj.file1: row add - пропуск повторяющейся записи: ошибки быть не должно
        ret = self.io.set(obj='file', data=( ('id',1), (self.TEST_FILE_ROW_1[1],'val11'), ), )
        assert ret[0]

        # obj.file1: row add +dat  new record
        ret = self.io.set(obj='file', data=( ('id',1), (self.TEST_FILE_ROW_1[0],'val11','1999-07-07'), ), )
        assert ret[0]

        # obj.file1: row add new record
        ret = self.io.set(obj='file', data=( ('id',1), (self.TEST_FILE_ROW_2[0],'val12','2020-07-08 05:06:07'), ), )
        assert ret[0]

        # obj.file2: add
        ret = self.io.set(obj='file', data=( ('id',2), (self.TEST_FILE_ROW_1[1],'val21'), (DAT_SYS_KEY.NAME_OWNER_ADD_RW, self.OWNER, '2000-01-01'), ), )
        assert ret[0]

        # obj.point: add
        ret = self.io.set(obj='point', data=( ('id',1), ('lat',52.22222), ('lon',23.666666), ('address','Едыгейск'), ), )
        assert ret[0]

        # obj.geometry: add
        val = '{"type": "GeometryCollection", "geometries": [{"type": "Polygon", "coordinates": [[[36.475, 59.624], [42.535, 58.217], [45.175, 61.48], [36.475, 59.624]]]}]}'
        ret = self.io.set(obj='geometry', data=( ('id',1), ('parent_id', 0), ('name','test_geo'), ('location',val), ), )
        assert ret[0]
        # аналог, работает
        # val = '''
        #     {
        #     "type": "FeatureCollection",
        #     "features": [
        #         {
        #             "type": "Feature",
        #             "properties": {},
        #             "geometry": {
        #                 "type": "Polygon",
        #                 "coordinates": [ [
        #                     [36.475, 59.624],
        #                     [42.535, 58.217],
        #                     [45.175, 61.480],
        #                     [36.475, 59.624]
        #                 ] ]
        #             }
        #         }
        #     ]}
        # '''

        # rel: add
        ret = self.io.set(obj='rel', data=( ('key_id',self.TEST_REL_1[1]), ('dat','2020-09-07'), ('file',1), ('geometry',1), ), )
        assert ret[0]
        #   ['key_id',   'ngg_smoke'],      # == ['key_id', 101],
        #   ['obj_id_1', 'file'],           # ОШИБКА повтор: ['obj_1', 4, 100],
        #   ['rec_id_1', 200],
        #   ['obj_2',    3,      100],      # == ['obj_2', 'geometry', 200]
        #   ['dat',      '2020-09-07'],
        #   ['file',     198],              # == [4, 200]
        #   ['geometry', 100],

        ret = self.io.set(obj='rel', data=( ('key_id',self.TEST_REL_1[0]), ('dat','2020-09-07 01:02:03'), ('file',2), ('geometry',1), ), )
        assert ret[0]




    # чтение
    def test_get(self):
        # free
        ret = tuple(self.io.get_obj(obj='free', ids=(1,), ))
        assert ret == ((1, 3, 'test_free_1', None),)

        # file: прочитать все ключи объекта
        # keys          = ('type', 'path', 'test', 10405),
        # ids_max_block = 1,
        ret = tuple(self.io.get_obj(obj='file', ids=(1,), where_dop_row = ['not (dat is null)', 'dat>"2000-01-01"'], ))
        assert ret == ((1, 15010, 1),(1, 15011, 'test_path_2'),(1, 15000, '54', '2000-01-03 00:00:00'),(1, 5, 'val12', '2020-07-08 05:06:07'))

        # file: прочитать выбранные ключи объекта
        ret = tuple(self.io.get_obj(obj='file', ids=(1,), keys=(self.TEST_FILE_COL_1[1],self.TEST_FILE_ROW_2[0]), ids_max_block=1, ))
        assert ret == ((1, 15011, 'test_path_2'), (1, 5, 'val12', '2020-07-08 05:06:07'))

        ret = tuple(self.io.get_obj(obj='file', ids=(2,), ))
        assert ret == ((2, 4, 'val21', None), (2, 15000, '54', '2000-01-01 00:00:00'))

        # point
        ret = tuple(self.io.get_obj(obj='point', ids=(1,), keys=('address', DAT_SYS_KEY.NAME_POINT_LOCATION), ))
        assert ret == ((1, 25204, 'Едыгейск'), (1, 'location', '{"type": "Point", "coordinates": [23.666666, 52.22222]}'))

        # geometry
        ret = tuple(self.io.get_obj(obj='geometry', ids=(1,), keys=('name', DAT_SYS_KEY.NAME_GEOMETRY_LOCATION), ))
        assert ret == ((1, 30303, 'test_geo'), (1, 'location', '{"type": "GeometryCollection", "geometries": [{"type": "Polygon", "coordinates": [[[36.475, 59.624], [42.535, 58.217], [45.175, 61.48], [36.475, 59.624]]]}]}'))

        # rel
        ret = tuple(self.io.get_rel(keys=(self.TEST_REL_1[1],), obj_rel_1=('file',2)))
        assert ret == ((1, '2020-09-07 01:02:03', 15, 2, 30, 1),)
        #     keys      = ['ngg_smoke', 104],
        #     obj_rel_1 = ['file',      198],
        #     obj_rel_2 = ['point',     33],
        #     where_dop = ['dat<"2020-09-09"',],

        # ret = self.io.get_geometry_tree(parent_id=0)
        # print(ret)




    # доступ
    def test_owner(self):
        ## удалить старого и добавть нового чужого владельца с одним датой/времением не полуится (случайный порядок записей)
        # сменить владельца на чужого
        ret = self.io.set(obj='file', data=( ('id',1), (DAT_SYS_KEY.NAME_OWNER_DEL,self.OWNER,'2020-02-01'), (DAT_SYS_KEY.NAME_OWNER_ADD_RW,53,'2020-02-01'), ), )
        assert ret[0]

        # прочитать получится только вторую запись
        ret = tuple(self.io.get_obj(obj='file', ids=(1,2,), ) )
        assert ret == ((2, 4, 'val21', None), (2, 15000, '54', '2000-01-01 00:00:00'))

        # запрет на установление связи с закрытым объектом
        ret = self.io.set(obj='rel', data=( ('key_id',self.TEST_REL_1[0]), ('dat','2020-09-07'), ('file',1), ('geometry',1), ), )
        assert not ret[0]

        # запрет на чтение связи с закрытым объектом file.2; читается только с открытым file.1
        ret = tuple(self.io.get_rel(keys=(self.TEST_REL_1[0],), obj_rel_1=('geometry',1)))
        assert ret == ((1, '2020-09-07 01:02:03', 15, 2, 30, 1),)



        # изменить владение на только чтение
        ret = self.io.set(obj='file', data=( ('id',2), (DAT_SYS_KEY.NAME_OWNER_DEL,self.OWNER,'2020-02-01'), (DAT_SYS_KEY.NAME_OWNER_ADD_RO,self.OWNER,'2020-02-01'), ), )
        assert ret[0]

        # запись не получится
        ret = self.io.set(obj='file', data=( ('id',2), (self.TEST_FILE_ROW_2[1],'val22'), ), )
        assert not ret[0]

        # чтение получится
        ret = tuple(self.io.get_obj(obj='file', ids=(2,), keys=(self.TEST_FILE_ROW_1[1], ), ))
        assert ret == ((2, 4, 'val21', None),)

        # запрет на установление связи с объектом только чтение
        ret = self.io.set(obj='rel', data=( ('key_id',self.TEST_REL_2[0]), ('dat','2020-09-07'), ('file',2), ('point',1), ), )
        assert not ret[0]



        # obj.file3: владелец другой, мы только чтение на 7 суток, установлено 6 и 8 дней назад
        ret = self.io.set(obj='file', data=( ('id',3), (self.TEST_FILE_COL_1[1],'test_path_3'), (DAT_SYS_KEY.NAME_OWNER_ADD_RW,53), (DAT_SYS_KEY.NAME_OWNER_ADD_RO_LIMIT,self.OWNER,str((datetime.now()-timedelta(days=6)).replace(microsecond=0))), ), )
        assert ret[0]
        ret = self.io.set(obj='file', data=( ('id',4), (self.TEST_FILE_COL_1[1],'test_path_3'), (DAT_SYS_KEY.NAME_OWNER_ADD_RW,53), (DAT_SYS_KEY.NAME_OWNER_ADD_RO_LIMIT,self.OWNER,str((datetime.now()-timedelta(days=8)).replace(microsecond=0))), ), )
        assert ret[0]

        # прочитать получится только 3 - срок не прошел, по 4 - ограничение аннулировано через 7 дней и объект общедоступен
        ret = tuple(self.io.get_obj(obj='file', ids=(3,4,), keys=(self.TEST_FILE_COL_1[0],) ) )
        assert ret == ((3, 15011, 'test_path_3'), )
