import os

from django.test import TestCase

from data_base_driver.constants.const_script import BASE_PATH_TO_USER_SCRIPTS
from data_base_driver.script.script_parsec import parse_text_to_python


class TestInputOutputBase(TestCase):
    databases = {}

    script_text_true = 'if keys_rel.find(', ') != -1:\n' + \
                       '\tkeys_rel = [int(item) for item in keys_rel.split(', ')]\n' + \
                       'else:\n' + \
                       '\tkeys_rel = [int(keys_rel)]\n' + \
                       'res = rel_to_geo_fc(obj, 0, keys_rel=keys_rel, keys_obj=[\'parent_id\'],where_dop=[])\n'

    script_text_false = 'if keys_rel.find(', ') != -1:\n' + \
                        '\tkeys_rel = [int(item) for item in keys_rel.split(', ')]\n' + \
                        'else:\n' + \
                        '\tkeys_rel = [int(keys_rel)]\n' + \
                        'res = rel_to_geo_fc_2(obj, 0, keys_rel=keys_rel, keys_obj=[\'parent_id\'],where_dop=[])\n'

    params = 'keys_rel;str;\n' \
             'obj;int;'

    def test_script_create_true(self):
        self.script_text_true = ''.join(self.script_text_true)
        status = parse_text_to_python('test', self.script_text_true, self.params, type='map')
        path = BASE_PATH_TO_USER_SCRIPTS + 'test.py'
        os.remove(path)
        self.assertEqual(status[0], True)

    def test_script_create_false(self):
        self.script_text_false = ''.join(self.script_text_false)
        status = parse_text_to_python('test', self.script_text_false, self.params, type='map')
        path = BASE_PATH_TO_USER_SCRIPTS + 'test.py'
        self.assertEqual(status[0], False)
