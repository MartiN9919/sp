from datetime import datetime
from django.test import TestCase

from data_base_driver.connect.connect_mysql import db_reconnect, set_autocommit_off, set_autocommit_on, roll_back
from data_base_driver.constants.connect_db import TEST_DATA
from data_base_driver.sys_templates.get_template_info import get_templates_list, get_template
from data_base_driver.sys_templates.set_templates_info import add_template, update_template, remove_template


class TestTemplates(TestCase):
    databases = {}

    @classmethod
    def setUpTestData(cls):
        db_reconnect(TEST_DATA)
        set_autocommit_off()

    @classmethod
    def tearDownClass(cls) -> None:
        set_autocommit_on()


class TestAddTemplate(TestTemplates):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        add_template(23, 'test_template_1', 'aaa', 'bbb')
        add_template(1, 'test_template_2', 'ccc', 'ddd')

    def test_get_added_template(self):
        templates = get_templates_list(2)
        self.assertEqual(templates[0].get('title', None), 'test_template_1')
        self.assertEqual(len(templates), 1)


class TestUpdateTemplate(TestTemplates):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        id = add_template(23, 'test_template_1', 'aaa', 'bbb')
        update_template(id, 2, 'update_test_template_1', 'aaa', 'bbb')

    def test_get_added_template(self):
        templates = get_templates_list(2)
        self.assertEqual(templates[0].get('title', None), 'update_test_template_1')


class TestDeleteTemplate(TestTemplates):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        id = add_template(1, 'test_template_1', 'aaa', 'bbb')
        remove_template(1, id)

    def test_get_added_template(self):
        templates = get_templates_list(1)
        self.assertEqual(len(templates), 0)


class TestGetTemplate(TestTemplates):
    databases = {}

    def tearDown(self) -> None:
        roll_back()

    def setUp(self):
        self.id_template = add_template(23, 'test_template_1', 'aaa', 'bbb')

    def test_get_template(self):
        template = get_template(self.id_template, 2)
        self.assertEqual(template.get('activeAnalysts', None), 'aaa')

