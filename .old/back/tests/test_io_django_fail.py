# -*- coding: utf-8 -*-

# pytest -v -vv -l -s -m io_script

import test_ini_common
import test_ini_django
import pytest

from   lib.db.const.const_dat           import DAT_SYS_OBJ, DAT_SYS_KEY
#from   django.test                     import Client


# @pytest.mark.io_ajax222
# class TestAjax:
#     OWNER           = 54
#     AJ              = '/aj/script/'

#     TEST_REL_1      = (1,     'test_rel_1')
#     TEST_REL_2      = (2,     'test_rel_2')


#     def setup_class(cls):
#         cls.c = Client(enforce_csrf_checks=False)
#         cls.c.login(username='sysadmin', password='2988810')
#         # response = cls.c.get(path='/auth/login/', data={'username': 'sysadmin', 'password': '2988810'}, follow=True)  # , secure=True
#         # assert response.status_code==200
#         # response = cls.c.post(path='/auth/login/', data={'username': 'sysadmin', 'password': '2988810'}, follow=True)  # , secure=True
#         # assert response.status_code==200

#     def teardown_class(cls):
#         pass
#         #response = cls.c.get('/auth/logout/', {})
#         #assert response.status_code==200

#     def ini(cls):
#         pass

#     def free(cls):
#         pass

#     def setup(self):                   pass #print ("basic setup into class")
#     def teardown(self):                pass #print ("basic teardown into class")
#     def setup_method(self, method):    pass #print ("method setup")
#     def teardown_method(self, method): pass #print ("method teardown")




#     # добавление объектов и их связей
#     def test_add(self):
#         pass
#         # response = self.c.get(path='/', follow=True)
#         # print(111, response.status_code, response.content)

#         # response = self.c.post(path=self.AJ, data={'script': 'rel_to_geo', 'obj_name': 'point', 'keys_rel': ['ngg_tmc',], 'keys_obj': ['address']}, follow=True)
#         # print(11111, response.status_code, response.content)
