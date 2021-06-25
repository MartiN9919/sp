import json
from geojson import GeometryCollection, Point, LineString, Polygon
from time import sleep
from django.test import TestCase

from data_base_driver.connect.connect_manticore import on_test_mode, off_test_mode
from data_base_driver.input_output.io import io_set, io_get_obj, io_get_rel
from data_base_driver.connect.connect_mysql import db_connect, db_reconnect, set_autocommit_on, set_autocommit_off, \
    roll_back
from data_base_driver.constants.connect_db import TEST_DATA


class TestInputOutputBase(TestCase):
    databases = {}

    @classmethod
    def setUpTestData(cls):
        db_reconnect(TEST_DATA)
        set_autocommit_off()
        on_test_mode()

    @classmethod
    def tearDownClass(cls) -> None:
        set_autocommit_on()
        off_test_mode()


class TestGetObject(TestInputOutputBase):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        io_set(group_id=0, obj='file', data=[['owner_del', 4], ['owner_add_ro_limit', 5]])
        io_set(group_id=0, obj='file', data=[['owner_del', 5], ['owner_add_ro_limit', 2]])
        io_set(group_id=0, obj='file', data=[['owner_del', 3], ['owner_add_ro_limit', 9]])

    def test_get_file(self):
        file = io_get_obj(group_id=0, obj='file', keys=['owner_del'], where_dop_row=[], ids=[])
        self.assertEqual('4', file[0][2])

    def test_get_file_2(self):
        file = io_get_obj(group_id=0, obj='file', keys=['owner_add_ro_limit'], where_dop_row=[], ids=[])
        sleep(0.01)
        file = io_get_obj(group_id=0, obj='file', keys=['owner_del'], where_dop_row=[], ids=[])
        self.assertEqual('3', file[2][2])


class TestGetRel(TestInputOutputBase):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        io_set(group_id=0, obj='rel', data=[['key_id', 31], ['geometry', 100], ['file', 200]])
        io_set(group_id=0, obj='rel', data=[['key_id', 'ngg_opg'], ['point', 45], ['case', 398]])
        io_set(group_id=0, obj=1, data=[['key_id', 1301], ['transport', 12], ['geometry', 74]])

    def test_get_rel(self):
        rel = io_get_rel(group_id=0, keys=[], where_dop=[])
        self.assertEqual(200, rel[0][3])

    def test_get_rel_2(self):
        rel = io_get_rel(group_id=0, keys=[1301], where_dop=[])
        sleep(0.01)
        rel_2 = io_get_rel(group_id=0, keys=['ngg_opg'], where_dop=[])
        self.assertEqual(74, rel[0][3])
        self.assertEqual(398, rel_2[0][5])


class TestGetGeometry(TestInputOutputBase):
    databases = {}

    def setUp(self):
        io_set(group_id=0, obj='geometry', data=[['location',
                                                  '{"type":"GeometryCollection","geometries":[{"type":"Polygon","coordinates":[[[36.475, 59.624],[42.535, 58.217],[45.175, 61.48],[36.475, 59.624]]]}]}']])

    def tearDown(self) -> None:
        roll_back()

    def test_get_fc_by_rel(self):
        geo = io_get_obj(group_id=0, obj='geometry', keys=['ST_AsGeoJSON(location) AS location'])
        geoCollections = GeometryCollection(
            [Polygon([[(36.475, 59.624), (42.535, 58.217), (45.175, 61.48), (36.475, 59.624)]])])
        geo = json.loads(geo[0][2])['geometries'][0]['coordinates']
        geoCollections = geoCollections.get('geometries')[0].get('coordinates')
        self.assertEqual(geoCollections, geo)


class TestSetCase(TestInputOutputBase):
    databases = {}

    def setUp(self):
        io_set(group_id=0, obj='case', data=[['type', 'ДОУ'], [45505, 'пример описания дела'], [45520, '20-12-2019']])
        io_set(group_id=0, obj=25, data=[[25204, 5]])
        io_set(group_id=0, obj='transport', data=[['color', 'красный'], [50005, '9']])

    def test_get_case(self):
        case = io_get_obj(group_id=0, obj=45, keys=[45505])
        self.assertEqual(case[0][2], 'пример описания дела')
        car = io_get_obj(group_id=0, obj='transport', keys=['color'])
        self.assertEqual(car[0][2], 'красный')
        car = io_get_obj(group_id=0, obj='transport', keys=[50005])
        self.assertEqual(car[0][2], '9')
