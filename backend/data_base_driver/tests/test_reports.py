import json

from django.test import TestCase

from data_base_driver.connect.connect_manticore import on_test_mode, off_test_mode
from data_base_driver.sys_reports.get_files_info import get_list_files_by_user, get_file_path
from data_base_driver.sys_reports.set_file_info import add_file, set_file_status, set_file_path

from datetime import datetime
from data_base_driver.connect.connect_mysql import db_reconnect, set_autocommit_off, set_autocommit_on, \
    roll_back
from data_base_driver.constants.connect_db import TEST_DATA


class TestReports(TestCase):
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


class TestGetObject(TestReports):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        data = {'id': 12, 'val': {'par': 10}}
        data2 = {'id': 13, 'val': {'par': 45}}
        add_file('test/file.txt', 1, 1, params=json.dumps(data, ensure_ascii=False))
        self.date_time = datetime.today()
        self.date_time = self.date_time.replace(microsecond=0)
        add_file('test/file2.txt', 3, 2, params=json.dumps(data2, ensure_ascii=False), status='done',
                 date_auto_remove=self.date_time)

    def test_get_reports(self):
        reports = get_list_files_by_user(1)
        self.assertEqual(reports[0].get('name', []), 'file.txt')

    def test_get_reports_data(self):
        reports = get_list_files_by_user(2)
        self.assertEqual(reports[0].get('date'), self.date_time.isoformat(sep=' '))
