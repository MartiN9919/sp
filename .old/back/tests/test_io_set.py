# -*- coding: utf-8 -*-

# pytest -v -vv -l -s -m io_set

import test_ini_common
import test_ini_django
import pytest

from   lib.db.const.const_dat          import DAT_SYS_OBJ, DAT_SYS_KEY
from   lib.db.io.io_class              import IO
from   lib.db.connect.connect_mysql    import db_sql
from   datetime                        import datetime, timedelta


@pytest.mark.io_set
class TestIO:
    OWNER           = 54

    KEY_FREE_1      = (80, 'test_free_30')
    KEY_GEO_1       = (81, 'test_geo_color')

    KEY_REL_01      = (31, 'photo_panorama')
    KEY_REL_02      = (32, 'ngg_smoke')
    KEY_REL_03      = (33, 'ngg_migrate')
    KEY_REL_04      = (34, 'ngg_tmc')
    KEY_REL_05      = (35, 'ngg_opg')
    KEY_REL_06      = (36, 'ngg_npr')
    KEY_REL_10      = (41, 'arial_1')
    KEY_REL_11      = (42, 'arial_2')
    KEY_REL_12      = (43, 'arial_3')

    OBJ_ID_REL      = DAT_SYS_OBJ.DUMP.to_id(val='rel')
    OBJ_ID_FREE     = DAT_SYS_OBJ.DUMP.to_id(val='free')
    OBJ_ID_POINT    = DAT_SYS_OBJ.DUMP.to_id(val='point')
    OBJ_ID_GEOMETRY = DAT_SYS_OBJ.DUMP.to_id(val='geometry')
    OBJ_ID_CASE     = DAT_SYS_OBJ.DUMP.to_id(val='case')



    def setup_class(cls):
        cls.io = IO(group_id=cls.OWNER, debug=False)
        cls.free(cls)
        cls.ini(cls)

    def teardown_class(cls):
        pass #cls.free(cls)

    def ini(cls):
        sql = "INSERT IGNORE "+DAT_SYS_KEY.TABLE+" ("+\
            DAT_SYS_KEY.ID       +", "+\
            DAT_SYS_KEY.OBJ_ID   +", "+\
            DAT_SYS_KEY.TYPE_VAL +", "+\
            DAT_SYS_KEY.NAME     +", "+\
            DAT_SYS_KEY.TITLE    +") VALUES "+\
            "("+str(cls.KEY_FREE_1[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_FREE    ))+"', 'str', '"+cls.KEY_FREE_1[1]+"', '"+cls.KEY_FREE_1[1]+"'), "+\
            "("+str(cls.KEY_GEO_1 [0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_GEOMETRY))+"', 'int', '"+cls.KEY_GEO_1 [1]+"', '"+cls.KEY_GEO_1 [1]+"'), "+\
            "("+str(cls.KEY_REL_01[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_REL     ))+"', 'int', '"+cls.KEY_REL_01[1]+"', '"+cls.KEY_REL_01[1]+"'), "+\
            "("+str(cls.KEY_REL_02[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_REL     ))+"', 'int', '"+cls.KEY_REL_02[1]+"', '"+cls.KEY_REL_02[1]+"'), "+\
            "("+str(cls.KEY_REL_03[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_REL     ))+"', 'int', '"+cls.KEY_REL_03[1]+"', '"+cls.KEY_REL_03[1]+"'), "+\
            "("+str(cls.KEY_REL_04[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_REL     ))+"', 'int', '"+cls.KEY_REL_04[1]+"', '"+cls.KEY_REL_04[1]+"'), "+\
            "("+str(cls.KEY_REL_05[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_REL     ))+"', 'int', '"+cls.KEY_REL_05[1]+"', '"+cls.KEY_REL_05[1]+"'), "+\
            "("+str(cls.KEY_REL_06[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_REL     ))+"', 'int', '"+cls.KEY_REL_06[1]+"', '"+cls.KEY_REL_06[1]+"'), "+\
            "("+str(cls.KEY_REL_10[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_REL     ))+"', 'int', '"+cls.KEY_REL_10[1]+"', '"+cls.KEY_REL_10[1]+"'), "+\
            "("+str(cls.KEY_REL_11[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_REL     ))+"', 'int', '"+cls.KEY_REL_11[1]+"', '"+cls.KEY_REL_11[1]+"'), "+\
            "("+str(cls.KEY_REL_12[0])+", '"+str(DAT_SYS_OBJ.DUMP.to_id(val=cls.OBJ_ID_REL     ))+"', 'int', '"+cls.KEY_REL_12[1]+"', '"+cls.KEY_REL_12[1]+"')"
        db_sql(sql=sql, wait=True, read=False, connection=cls.io.io_org[cls.io.ORG_SQL].io_sql.connection)
        DAT_SYS_KEY.DUMP._refresh_(force=True)

    def free(cls):
        exec_sql = lambda sql: db_sql(sql=sql, wait=True, read=False, connection=cls.io.io_org[cls.io.ORG_SQL].io_sql.connection)
        exec_sql("DELETE FROM rel              WHERE obj_id_1="+str(cls.OBJ_ID_FREE    )+" AND rec_id_1 BETWEEN 30 AND 100")
        exec_sql("DELETE FROM rel              WHERE obj_id_2="+str(cls.OBJ_ID_FREE    )+" AND rec_id_2 BETWEEN 30 AND 100")
        exec_sql("DELETE FROM rel              WHERE obj_id_1="+str(cls.OBJ_ID_POINT   )+" AND rec_id_1 BETWEEN 30 AND 100")
        exec_sql("DELETE FROM rel              WHERE obj_id_2="+str(cls.OBJ_ID_POINT   )+" AND rec_id_2 BETWEEN 30 AND 100")
        exec_sql("DELETE FROM rel              WHERE obj_id_1="+str(cls.OBJ_ID_GEOMETRY)+" AND rec_id_1 BETWEEN 30 AND 100")
        exec_sql("DELETE FROM rel              WHERE obj_id_2="+str(cls.OBJ_ID_GEOMETRY)+" AND rec_id_2 BETWEEN 30 AND 100")
        exec_sql("DELETE FROM rel              WHERE obj_id_1="+str(cls.OBJ_ID_CASE    )+" AND rec_id_1 BETWEEN 30 AND 100")
        exec_sql("DELETE FROM rel              WHERE obj_id_2="+str(cls.OBJ_ID_CASE    )+" AND rec_id_2 BETWEEN 30 AND 100")
        exec_sql("DELETE FROM obj_point_col    WHERE id BETWEEN 30 AND 100")
        exec_sql("DELETE FROM obj_geometry_col WHERE id BETWEEN 30 AND 100")
        exec_sql("DELETE FROM obj_case_row     WHERE id BETWEEN 30 AND 100")
        exec_sql("DELETE FROM obj_free_row     WHERE id BETWEEN 30 AND 100")

        sql = "DELETE FROM "+DAT_SYS_KEY.TABLE+" WHERE id IN ("+\
            str(cls.KEY_FREE_1[0])+","+\
            str(cls.KEY_GEO_1 [0])+","+\
            str(cls.KEY_REL_01[0])+","+\
            str(cls.KEY_REL_02[0])+","+\
            str(cls.KEY_REL_03[0])+","+\
            str(cls.KEY_REL_04[0])+","+\
            str(cls.KEY_REL_05[0])+","+\
            str(cls.KEY_REL_06[0])+","+\
            str(cls.KEY_REL_10[0])+","+\
            str(cls.KEY_REL_11[0])+","+\
            str(cls.KEY_REL_12[0])+\
            ")"
        db_sql(sql=sql, wait=True, read=False, connection=cls.io.io_org[cls.io.ORG_SQL].io_sql.connection)
        DAT_SYS_KEY.DUMP._refresh_(force=True)

    def setup(self):                   pass #print ("basic setup into class")
    def teardown(self):                pass #print ("basic teardown into class")
    def setup_method(self, method):    pass #print ("method setup")
    def teardown_method(self, method): pass #print ("method teardown")


    @pytest.mark.parametrize("data", [
        ('geometry', ('id',30), ('parent_id',0),  ('name','Группа 0'),  ('icon','fa-folder')),
        ('geometry', ('id',31), ('parent_id',0),  ('name','Группа 1'),  ('icon','fa-folder')),
        ('geometry', ('id',32), ('parent_id',30), ('name','Группа 11'), ('icon','fa-folder')),
        ('geometry', ('id',41), ('parent_id',32), ('name','Тест 41'),   ('icon','fa-lock'), (KEY_GEO_1[1],  5),    ('location','{"type":"GeometryCollection","geometries":[{"type":"Polygon","coordinates":[[[36.475, 59.624],[42.535, 58.217],[45.175, 61.48],[36.475, 59.624]]]}]}')),
        ('geometry', ('id',42), ('parent_id',30), ('name','Тест 41'),   ('icon','fa-lock'), (KEY_GEO_1[1], -1),    ('location','{"type":"GeometryCollection","geometries":[{"type":"Polygon","coordinates":[[[26.475, 59.624],[32.535, 58.217],[35.175, 61.48],[26.475, 59.624]]]}]}')),
        ('geometry', ('id',51), ('parent_id',0),  ('name','Тест 51'),   ('icon','fa-lock'), (KEY_GEO_1[1],  0.05), ('location','{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[26.147461,54.138306]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[23.840332,53.232345],[24.095764,53.335793],[24.315491,53.465161],[24.505005,53.704836],[24.397888,53.89301],[24.178162,53.951237],[23.969421,53.926986],[23.799133,53.938305],[23.5849,53.931837],[23.518982,53.946388],[23.549194,53.834702],[23.562927,53.753583],[23.672791,53.499483],[23.840332,53.232345]]]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[24.785156,53.745462]}}]}')),
        ('geometry', ('id',52), ('parent_id',0),  ('name','Тест 52'),   ('icon','fa-lock'), (KEY_GEO_1[1],  50),   ('location','{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[24.873047,54.038425],[24.785156,54.094839],[25.296021,54.08034],[25.485535,53.933454],[25.136719,53.842805],[24.873047,54.038425]]]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[26.191406,55.166319],[27.301025,56.26166],[29.421387,55.447711],[28.421631,55.153766],[27.784424,54.952386],[26.191406,55.166319]]]}},{"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":[[25.97168,55.973798],[26.290283,56.279961],[26.696777,56.127184],[26.048584,55.453941],[26.05957,54.977614],[27.224121,54.393352],[28.081055,54.226708],[29.685059,54.57843],[31.717529,54.711929]]}}]}')),
        ('geometry', ('id',53), ('parent_id',0),  ('name','Тест 53'),   ('icon','fa-lock'), (KEY_GEO_1[1], -5),    ('location','{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[24.971924,54.661124],[25.026855,54.901882],[26.015625,54.692884],[25.927734,54.290882],[24.971924,54.661124]]]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[24.971924,56.26166],[25.993652,56.249454],[26.564941,55.899956],[26.169434,55.627996],[24.971924,56.26166]]]}}]}')),
        ('geometry', ('id',54), ('parent_id',0),  ('name','Тест 54'),   ('icon','fa-lock'), (KEY_GEO_1[1],  100),  ('location','{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[27.652588,53.962549],[27.897034,53.923751],[27.850342,53.792539],[27.405396,53.686949],[27.100525,53.813626],[27.012634,53.999697],[27.182922,54.099671],[27.652588,53.962549]]]}},{"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":[[26.575928,54.239551],[27.498779,54.622978],[27.938232,54.175297],[28.861084,54.239551],[28.959961,53.943155]]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[26.334229,54.001312]}}]}')),
        ('geometry', ('id',55), ('parent_id',0),  ('name','Тест 55'),   ('icon','fa-lock'), (KEY_GEO_1[1],  0),    ('location','{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[25.400391,52.676382]}},{"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":[[26.224365,52.227799],[26.202393,52.922151],[28.190918,52.335339],[26.960449,52.227799]]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[25.356445,53.787672],[27.147217,54.290882],[26.729736,53.442264],[25.356445,53.787672]]]}}]}')),
        ('geometry', ('id',56), ('parent_id',0),  ('name','Тест 56'),   ('icon','fa-lock'), (KEY_GEO_1[1],  20),   ('location','{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[24.710999,52.414985],[25.006256,52.414985],[25.006256,52.533349],[24.815369,52.486125],[24.710999,52.533349],[24.710999,52.414985]]]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[24.510498,52.875761]}}]}')),
        ('geometry', ('id',57), ('parent_id',0),  ('name','Тест 57'),   ('icon','fa-lock'), (KEY_GEO_1[1], -3),    ('location','{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[27.355957,54.584797]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[26.938477,55.621793],[28.443604,55.497527],[28.048096,56.383502],[26.938477,55.621793]]]}}]}')),
        ('geometry', ('id',58), ('parent_id',0),  ('name','Тест 58'),   ('icon','fa-lock'), (KEY_GEO_1[1],  4),    ('location','{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":[[26.218872,54.377358],[26.130981,53.972243],[24.587402,53.901102],[25.114746,54.654769],[26.092529,54.85764]]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[24.949951,54.072283],[25.664063,54.501948],[25.900269,54.127041],[24.949951,54.072283]]]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[26.564941,54.27164]}}]}')),

        ('point', ('id',33), ('lat',52.0839356), ('lon',23.650415 ), ('address','Брест, ул.Русакова,124')),
        ('point', ('id',34), ('lat',54.4773572), ('lon',26.3932509), ('address','Сморгонь, ул.Белинского,124')),
        ('point', ('id',35), ('lat',55.4798043), ('lon',28.7796702), ('address','Полоцк, ул.Софии Полоцкой, 3')),
        ('point', ('id',36), ('lat',53.8870722), ('lon',27.962096 ), ('address','Самолеты Минск')),
        ('point', ('id',37), ('lat',53.2628595), ('lon',23.8672983), ('address','Нижний Новгород, 40 лет Победы ул., 7')),
        ('point', ('id',38), ('lat',53.2255994), ('lon',23.8739022), ('address','Нижний Новгород, 60-летия Октября б-р, 2а, САЮС')),
        ('point', ('id',39), ('lat',53.2241874), ('lon',23.8191839), ('address','Нижний Новгород, Агрономов ул, 77')),
        ('point', ('id',40), ('lat',53.2490319), ('lon',24.0470196), ('address','Нижний Новгород, Адмирала Макарова ул., 16-40')),
        ('point', ('id',41), ('lat',52.8521343), ('lon',23.9992328), ('address','Нижний Новгород, Акимова ул., 50')),
        ('point', ('id',42), ('lat',52.8345252), ('lon',23.9736483), ('address','Нижний Новгород, Алексеевская ул., 1')),
        ('point', ('id',43), ('lat',52.8685392), ('lon',24.1087106), ('address','Нижний Новгород, Алексеевская ул., 6/16')),
        ('point', ('id',44), ('lat',53.9232459), ('lon',24.466538 ), ('address','Нижний Новгород, Алексеевская ул., 8а1')),
        ('point', ('id',45), ('lat',53.7653914), ('lon',24.3036483), ('address','Нижний Новгород, Анкудиновское ш, 184')),
        ('point', ('id',46), ('lat',53.3524766), ('lon',24.7062152), ('address','Нижний Новгород, Анкудиновское ш, 3а')),
        ('point', ('id',47), ('lat',54.8527277), ('lon',27.0920334), ('address','Нижний Новгород, Анкудиновское ш, 85')),
        ('point', ('id',48), ('lat',55.5022909), ('lon',27.939888 ), ('address','Нижний Новгород, Аральская ул., 23')),
        ('point', ('id',49), ('lat',54.7061863), ('lon',30.5381097), ('address','Нижний Новгород, Артельная ул., 3')),
        ('point', ('id',50), ('lat',53.7793249), ('lon',30.3136429), ('address','Нижний Новгород, Артемовская ул., 30')),
        ('point', ('id',51), ('lat',52.3222736), ('lon',30.2990905), ('address','Нижний Новгород, Аэропорт ул., 1')),
        ('point', ('id',52), ('lat',52.3162907), ('lon',28.5324098), ('address','Нижний Новгород, Б. Корнилова ул., 5/1')),
        ('point', ('id',53), ('lat',52.3969908), ('lon',28.3072926), ('address','Нижний Новгород, Б. Корнилова ул., 6/1')),
        ('point', ('id',54), ('lat',53.6174398), ('lon',27.9788652), ('address','<strong>НГГ</strong><br />ушел и не поймали')),
        ('point', ('id',55), ('lat',53.4621   ), ('lon',26.9469   ), ('address','Тест 1')),
        ('point', ('id',56), ('lat',53.4506   ), ('lon',26.8133   ), ('address','Тест 2')),
        ('point', ('id',57), ('lat',53.4718   ), ('lon',26.6726   ), ('address','Тест 3')),
        ('point', ('id',58), ('lat',53.5038   ), ('lon',26.9488   ), ('address','Тест 4')),

        ('case',  ('id',30), (45502,'ДОУ'), (45505,'Описание и только')),
        ('case',  ('id',31), (45502,'УД'),  (45505,'Описание 2')),
        ('case',  ('id',32), (45502,'АД'),  (45505,'Описание 3')),
        ('case',  ('id',33), (45502,'АД'),  (45505,'Описание 4')),

        ('free', ('id',30), (KEY_FREE_1[0],'val 1','2020-01-01')),
        ('free', ('id',30), (KEY_FREE_1[1],'val 2','2020-01-02')),
        ('free', ('id',30), (KEY_FREE_1[0],'val 3','2020-02-02')),

        ('rel',  ('key_id',KEY_REL_02[0]),                       ('point',38), ('case',30)),
        ('rel',  ('key_id',KEY_REL_02[0]),                       ('point',39), ('case',33)),
        ('rel',  ('key_id',KEY_REL_02[0]),                       ('point',40), ('case',32)),
        ('rel',  ('key_id',KEY_REL_02[0]),                       ('point',41), ('case',32)),
        ('rel',  ('key_id',KEY_REL_02[1]),                       ('point',42), ('case',32)),
        ('rel',  ('key_id',KEY_REL_03[0]), ('dat','2020-04-15'), ('point',33), ('case',33)),
        ('rel',  ('key_id',KEY_REL_03[1]), ('dat','2020-05-04'), ('point',34), ('case',30)),
        ('rel',  ('key_id',KEY_REL_03[0]), ('dat','2020-01-23'), ('point',35), ('case',31)),
        ('rel',  ('key_id',KEY_REL_03[0]), ('dat','2020-06-03'), ('point',36), ('case',33)),
        ('rel',  ('key_id',KEY_REL_03[1]), ('dat','2020-07-03'), ('point',37), ('case',31)),
        ('rel',  ('key_id',KEY_REL_02[0]), ('dat','2020-01-07'), ('point',43), ('case',30)),
        ('rel',  ('key_id',KEY_REL_04[0]), ('dat','2020-01-08'), ('point',44), ('case',31)),
        ('rel',  ('key_id',KEY_REL_04[0]), ('dat','2020-01-08'), ('point',45), ('case',33)),
        ('rel',  ('key_id',KEY_REL_04[0]), ('dat','2020-04-10'), ('point',46), ('case',31)),
        ('rel',  ('key_id',KEY_REL_04[1]), ('dat','2020-01-10'), ('point',47), ('case',30)),
        ('rel',  ('key_id',KEY_REL_04[0]), ('dat','2020-01-10'), ('point',48), ('case',31)),
        ('rel',  ('key_id',KEY_REL_05[0]), ('dat','2020-02-21'), ('point',49), ('case',32)),
        ('rel',  ('key_id',KEY_REL_05[0]), ('dat','2020-05-12'), ('point',50), ('case',33)),
        ('rel',  ('key_id',KEY_REL_05[0]), ('dat','2020-01-13'), ('point',51), ('case',30)),
        ('rel',  ('key_id',KEY_REL_05[1]), ('dat','2020-01-23'), ('point',52), ('case',33)),
        ('rel',  ('key_id',KEY_REL_05[0]), ('dat','2020-07-13'), ('point',53), ('case',30)),
        ('rel',  ('key_id',KEY_REL_06[0]), ('dat','2020-02-14'), ('point',54), ('case',31)),
        ('rel',  ('key_id',KEY_REL_06[1]), ('dat','2020-01-14'), ('point',55), ('case',32)),
        ('rel',  ('key_id',KEY_REL_06[0]), ('dat','2020-03-14'), ('point',56), ('case',33)),
        ('rel',  ('key_id',KEY_REL_06[0]), ('dat','2020-04-34'), ('point',57), ('case',32)),
        ('rel',  ('key_id',KEY_REL_06[0]), ('dat','2020-01-14'), ('point',58), ('case',31)),

        ('rel',  ('key_id',KEY_REL_10[0]), ('dat','2020-05-01'), ('geometry',42), ('case',31)),
        ('rel',  ('key_id',KEY_REL_10[0]), ('dat','2020-05-05'), ('geometry',52), ('case',31)),
        ('rel',  ('key_id',KEY_REL_10[0]), ('dat','2020-05-06'), ('geometry',53), ('case',31)),
        ('rel',  ('key_id',KEY_REL_10[0]), ('dat','2020-05-07'), ('geometry',54), ('case',33)),
        ('rel',  ('key_id',KEY_REL_10[0]), ('dat','2020-05-01'), ('geometry',55), ('case',33)),
        ('rel',  ('key_id',KEY_REL_11[1]), ('dat','2020-05-02'), ('geometry',55), ('case',31)),
        ('rel',  ('key_id',KEY_REL_11[1]), ('dat','2020-05-08'), ('geometry',56), ('case',31)),
        ('rel',  ('key_id',KEY_REL_11[1]), ('dat','2020-05-09'), ('geometry',57), ('case',32)),
        ('rel',  ('key_id',KEY_REL_11[1]), ('dat','2020-05-02'), ('geometry',58), ('case',33)),
        ('rel',  ('key_id',KEY_REL_12[0]), ('dat','2020-05-03'), ('geometry',52), ('case',31)),
        ('rel',  ('key_id',KEY_REL_12[1]), ('dat','2020-05-04'), ('geometry',56), ('case',32)),
    ])
    def test_add(self, data):
        val = list(data)
        obj = val[0]
        del val[0]
        ret = self.io.set(obj=obj, data=val )
        assert ret[0]
