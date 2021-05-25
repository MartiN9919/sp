# -*- coding: utf-8 -*-

class CONNECT:
    class DATA:
        HOST       = '127.0.0.1'
        PORT       = '3306'
        NAME       = 'vec_data'
        USER       = 'evgestrogan'
        PASSWORD   = '0990qweasd'
        CHARSET    = 'utf8'

    class DJANGO:
        HOST = '127.0.0.1'
        PORT = '3306'
        NAME = 'vec_django'
        USER = 'evgestrogan'
        PASSWORD = '0990qweasd'
        CHARSET = 'utf8'

    class SPHINX:
        HOST       = '192.168.30.109'
        PORT       = 9306
        CHARSET    = 'utf8'

    class OSM:
        HOST       = '192.168.56.104'
        PORT       = '5433'
        NAME       = 'gis'
        USER       = 'pymain'
        PASSWORD   = '1111'
        CHARSET    = 'utf8'

# os.getenv('SECRET_KEY', 'my-default-key')
# os.environ.get('SECRET_KEY')
