from django.test import TestCase

from data_base_driver.input_output.add_object_http import on_test_mode_manticore, off_test_mode_manticore
from data_base_driver.sys_notifications.get_notifications_info import get_notifications_by_user
from data_base_driver.sys_notifications.set_notifications_info import add_notification, remove_notification
from datetime import datetime
from data_base_driver.connect.connect_mysql import db_reconnect, set_autocommit_off, set_autocommit_on, \
    roll_back
from data_base_driver.constants.connect_db import TEST_DATA
from time import sleep


class TestNotifications(TestCase):
    databases = {}

    @classmethod
    def setUpTestData(cls):
        db_reconnect(TEST_DATA)
        set_autocommit_off()
        on_test_mode_manticore()

    @classmethod
    def tearDownClass(cls) -> None:
        set_autocommit_on()
        off_test_mode_manticore()


class TestGetObject(TestNotifications):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        add_notification(1, 'warning', 'тестовое оповещение', from_id=1, test_mode=True)
        self.date_time = datetime.today()
        self.date_time = self.date_time.replace(microsecond=0)
        add_notification(2, 'information', 'тестовое оповещение со временем', date_time=self.date_time, test_mode=True)

    def test_get_notifications(self):
        notifications = get_notifications_by_user(1, [])
        self.assertEqual(notifications.get('notifications', {})[0].get('status',None), 502)

    def test_get_notifications_with_time(self):
        notifications = get_notifications_by_user(2, [])
        self.assertEqual(notifications.get('notifications', {})[0].get('date_time', None), self.date_time.isoformat(sep=' '))

    def test_get_multiple_params(self):
        notifications = get_notifications_by_user(1, [])
        sleep(0.01)
        notifications2 = get_notifications_by_user(2, [])
        self.assertEqual(notifications.get('notifications', {})[0].get('content', None), 'тестовое оповещение')
        self.assertEqual(notifications2.get('notifications', {})[0].get('date_time', None), self.date_time.isoformat(sep=' '))


class TestDeleteObject(TestNotifications):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        id = add_notification(1, 'warning', 'тестовое оповещение', from_id=1, test_mode=True)
        remove_notification(id)

    def test_get_removed_notification(self):
        notifications = get_notifications_by_user(1, [])
        self.assertEqual(len(notifications.get('notifications', {})), 0)


class TestGetOldNotification(TestNotifications):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        self.id_notify = add_notification(2, 'warning', 'тестовое оповещение', from_id=1, test_mode=True)

    def test_get_removed_notification(self):
        notifications = get_notifications_by_user(2, [self.id_notify])
        self.assertEqual(len(notifications.get('notifications', {})), 0)
