import os

from data_base_driver.constants.const_admin import DEPLOY_SETTING

mode = os.environ.get('MODE')


class Geocoder:
    SEARCH_URL = DEPLOY_SETTING['geocoder']['SEARCH_URL'] if mode == 'deploy' else 'http://200.200.200.239:2322/api'