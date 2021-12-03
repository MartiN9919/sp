import os

from data_base_driver.constants.const_admin import DEPLOY_SETTING

mode = os.environ.get('MODE')

"""
Настройки для подключения к базе данных vec_data
"""

VEC_DATA = DEPLOY_SETTING['data_base'] if mode == 'deploy' else {
    'HOST': '200.200.200.233',
    'PORT': '3306',
    'NAME': 'vec_data' if mode == 'deploy' else 'smorgon',
    'USER': 'dev',
    'PASSWORD': '1',
    'CHARSET': 'utf8',
}


OSM = DEPLOY_SETTING['osm'] if mode == 'deploy' else {
    'HOST': '200.200.200.231',
    'PORT': '5432',
    'NAME': 'gis',
    'USER': 'dev',
    'PASSWORD': '1',
    'CHARSET': 'utf8',
}

MANTICORE = {
    'HOST': '200.200.200.235',
    'PORT': '9606',
    'NAME': 'Manticore'
}

SPHINX = {
    'HOST': '200.200.200.235',
    'PORT': '9306',
    'NAME': ''
}

TEST_DATA = {
    'HOST': '200.200.200.233',
    'PORT': '3306',
    'NAME': 'test_data',
    'USER': 'dev',
    'PASSWORD': '1',
    'CHARSET': 'utf8',
}