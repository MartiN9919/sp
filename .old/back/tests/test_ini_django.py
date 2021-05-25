# -*- coding: utf-8 -*-

# отключить предупреждения
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import imp


import os
import django
from   django.test.runner import DiscoverRunner

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.deploy.settings'


