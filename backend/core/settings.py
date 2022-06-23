from pathlib import Path

from django.contrib import admin
from django.middleware.csrf import rotate_token

from core.projectSettings.constant import MEDIA_ROOT
from data_base_driver.constants.connect_db import VEC_DATA


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '^7t+b0=(7#x)$7hqca+=9h1q+n40bwf*70gnxh$h#r($p!b=2e'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_admin_logs',

    'django_monaco_editor',
    'authentication',
    'script',
    'classifier',
    'data_base_driver',
    'official_documents',
    'admin_control',
    'objects',
    'files',
]
#
# ADMIN_ORDERING = [
#     ('classifier', [
#         'ModelObject',
#         'ObjectKey',
#         'Rel',
#         'ModelList',
#         'ModelPhoneNumberFormat'
#     ]),
# ]
#
#
# def get_app_list(self, request):
#     app_dict = self._build_app_dict(request)
#     for app_name, object_list in ADMIN_ORDERING:
#         app = app_dict[app_name]
#         app['models'].sort(key=lambda x: object_list.index(x['object_name']))
#         yield app
#
#
# admin.AdminSite.get_app_list = get_app_list

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.projectSettings.middleware.logging_middleware'
]

ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.__str__() + '/static/src/vue/dist/'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': VEC_DATA['HOST'],
        'PORT': VEC_DATA['PORT'],
        'NAME': VEC_DATA['NAME'],
        'USER': VEC_DATA['USER'],
        'PASSWORD': VEC_DATA['PASSWORD'],
        'TEST': {
            'NAME': 'test_vec_data',
        },
    },
}

AUTH_USER_MODEL = 'authentication.ModelCustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Minsk'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = 'var/static_root'
STATICFILES_DIRS = [
    "static",
]
