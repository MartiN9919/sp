"""
Настройки для подключения к базе данных vec_data
"""
VEC_DATA = {
    'HOST': '200.200.200.233',
    'PORT': '3306',
    'NAME': 'smorgon',
    'USER': 'dev',
    'PASSWORD': '1',
    'CHARSET': 'utf8',
}

OSM = {
    'HOST': '200.200.200.231',
    'PORT': '5432',
    'NAME': 'gis',
    'USER': 'dev',
    'PASSWORD': '1',
    'CHARSET': 'utf8',
}

MANTICORE = {
    'HOST': '200.200.200.235',
    'PORT': '9306',
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