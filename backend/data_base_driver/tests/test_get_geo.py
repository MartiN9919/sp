from django.test import TestCase
from data_base_driver.connect.connect_mysql import db_reconnect, set_autocommit_off, set_autocommit_on, roll_back
from data_base_driver.constants.connect_db import VEC_DATA
from data_base_driver.full_text_search.http_api.add_object_http import on_test_mode_manticore, off_test_mode_manticore
from data_base_driver.input_output.io_geo import geo_id_to_fc


class TestGetGeoBase(TestCase):
    databases = {}

    @classmethod
    def setUpTestData(cls):
        db_reconnect(VEC_DATA)
        set_autocommit_off()
        on_test_mode_manticore()

    @classmethod
    def tearDownClass(cls) -> None:
        set_autocommit_on()
        off_test_mode_manticore()


class TestGetGeoIdToFC(TestGetGeoBase):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        pass

    def test_get_point(self):
        geo = geo_id_to_fc(obj='point', group_id=0, geo_ids=[37],keys=['address'])
        self.assertEqual(geo[0].properties['address'][0],'Нижний Новгород, 40 лет Победы ул., 7')

    def test_get_geometry(self):
        geo = geo_id_to_fc(obj='geometry', group_id=0, geo_ids=[41],keys=['name'])
        self.assertEqual(geo[0].properties['name'][0], 'Тест 41')
