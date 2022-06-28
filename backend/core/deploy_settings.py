from pathlib import Path

from data_base_driver.constants.connect_db import VEC_DATA
from core.projectSettings.constant import DEPLOY_SETTING, MEDIA_ROOT

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = DEPLOY_SETTING['secret_key']

DEBUG = False

ALLOWED_HOSTS = DEPLOY_SETTING['allowed_hosts']

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.projectSettings.middleware.logging_middleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/deploy_storage/static/src/vue/dist/'
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


# SESSION_EXPIRE_AT_BROWSER_CLOSE = True