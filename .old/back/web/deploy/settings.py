# -*- coding: utf-8 -*-

"""
debuger
pip install django-werkzeug-debugger-runserver
pip uninstall Werkzeug
pip install Werkzeug==0.16.0
python3 manage.py runserver 0.0.0.0:8000

INSTALLED_APPS = (
    # ...
    'werkzeug_debugger_runserver',
    'django.contrib.staticfiles',
    # ...
)

"""




##################################################################################
# PATH
##################################################################################
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR  = BASE_DIR+'/../log/'
sys.path.append(BASE_DIR+'/../')

# Для переноса шаблонов с уровня приложения на уровень проекта
STATICFILES_DIRS = (
    os.path.normpath(os.path.join(BASE_DIR, 'static')),
    os.path.normpath('static/')
)

STATIC_URL   = '/static/'
STATIC_ROOT  = os.path.normpath(os.path.join(BASE_DIR, 'static_root/'))   # Только на PRODUCTION
#MEDIA_URL   = '/'
#MEDIA_ROOT  = os.path.normpath(os.path.join(BASE_DIR, ''))

ROOT_URLCONF = 'deploy.urls'

from   lib.const                    import PROJECT_TITLE, PROJECT_ID
from   lib.db.const.const_connect   import CONNECT



##################################################################################
# SETTINGS
##################################################################################
PROJECT_TITLE_NAME   = PROJECT_TITLE       # отображаемый заголовок web-страницы
PROJECT_LOG_MAIN     = 'MAIN'              # логгер главный
PROJECT_LOG_USERS    = 'USERS'             # логгер пользователи
PROJECT_LOG_REQUESTS = 'REQUESTS'          # логгер запросы



##################################################################################
# SETTINGS DJANGO
##################################################################################
SECRET_KEY    = 'u%3h$$)p30lv)*&mlp$v&o#25hao86b!lko=8ua^7&p8-jyt-!'
DEBUG         = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    #'192.168.56.1',
    '192.168.56.104',       # dev host
    '192.168.56.1',
    '200.200.200.31',       # intranet
    '134.17.226.2',         # internet
]


##################################################################################
# LOGING
##################################################################################
if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)

import logging
import logging.handlers
logger = {}

handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'.log', when='midnight', interval=1, backupCount=5)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s', datefmt='%H:%M:%S'))  # %Y-%m-%d
handler.setLevel(logging.INFO)
logger['root'] = logging.getLogger()
logger['root'].setLevel(logging.INFO)
logger['root'].addHandler(handler)

handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_main.log', when='midnight', interval=1, backupCount=10)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s', datefmt='%H:%M:%S'))  # %Y-%m-%d
handler.setLevel(logging.INFO)
logger['main'] = logging.getLogger(PROJECT_LOG_MAIN)
logger['main'].setLevel(logging.INFO)
logger['main'].addHandler(handler)

handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_users.log', when='midnight', interval=1, backupCount=30)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%H:%M:%S'))
handler.setLevel(logging.INFO)
logger['user'] = logging.getLogger(PROJECT_LOG_USERS)
logger['user'].setLevel(logging.INFO)
logger['user'].addHandler(handler)

handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_requests.log', when='midnight', interval=1, backupCount=30)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%H:%M:%S'))  # %Y-%m-%d
handler.setLevel(logging.INFO)
logger['requests'] = logging.getLogger(PROJECT_LOG_REQUESTS)
logger['requests'].setLevel(logging.INFO)
logger['requests'].addHandler(handler)

logger['main'].info('Start')



##################################################################################
# Application definition
##################################################################################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',                                      # Фреймворк аутентификации и моделей по умолчанию
    'django.contrib.contenttypes',                              # Django контент-типовая система (даёт разрешения, связанные с моделями)
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'compressor',

    'admin_dop',
    'authent',
    'map',
    'graph',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',     # Управление сессиями между запросами
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Связывает пользователей, использующих сессии, запросами
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),                # Для переноса шаблонов с уровня приложения на уровень проекта
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'nav': 'templatetags.nav',
            },
        },
    },
]

WSGI_APPLICATION = 'deploy.wsgi.application'



##################################################################################
# DATABASES
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# https://docs.djangoproject.com/en/2.2/topics/db/multi-db/
##################################################################################
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'HOST':     CONNECT.DJANGO.HOST,
        'PORT':     CONNECT.DJANGO.PORT,
        'NAME':     CONNECT.DJANGO.NAME,
        'USER':     CONNECT.DJANGO.USER,
        'PASSWORD': CONNECT.DJANGO.PASSWORD,
    },
    'vec_data': {
        'ENGINE':   'django.db.backends.mysql',
        'HOST':     CONNECT.DATA.HOST,
        'PORT':     CONNECT.DATA.PORT,
        'NAME':     CONNECT.DATA.NAME,
        'USER':     CONNECT.DATA.USER,
        'PASSWORD': CONNECT.DATA.PASSWORD,
    },
}
DATABASE_ROUTERS = ['admin_dop.models.AccountRouter']



##################################################################################
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
##################################################################################
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 10 # set just 10 seconds to test
# SESSION_SAVE_EVERY_REQUEST = True


##################################################################################
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
##################################################################################
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE     = 'Europe/Minsk'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True
