"""
Настройки для подключения к базе данных vec_data
"""
VEC_DATA = {
    'HOST': '200.200.200.233',
    'PORT': '3306',
    'NAME': 'vec_data_dev',
    'USER': 'dev',
    'PASSWORD': '1',
    'CHARSET': 'utf8',
}

"""
Настройки для подключения к базе данных vec_django
"""
VEC_DJANGO = {
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'NAME': 'vec_django',
    'USER': 'evgestrogan',
    'PASSWORD': '0990qweasd',
    'CHARSET': 'utf8',
}

OSM = {
    'HOST': '192.168.56.102',
    'PORT': '5432',
    'NAME': 'gis',
    'USER': 'pushkin',
    'PASSWORD': '1111',
    'CHARSET': 'utf8',
}

MANTICORE = {
    'HOST': '127.0.0.1',
    'PORT': '9306',
    'NAME': 'Manticore'
}

TEST_DATA = {
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'NAME': 'test_data',
    'USER': 'pushkin',
    'PASSWORD': '1111',
    'CHARSET': 'utf8',
}