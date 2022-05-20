import os

from core.deploy_settings import DEPLOY_SETTING

mode = os.environ.get('MODE')


class FullTextSearch:
    TABLES = {
        10: 'free',
        15: 'file',
        20: 'doc',
        25: 'point',
        30: 'geometry',
        35: 'person_p',
        40: 'person_l',
        45: 'case',
        50: 'transport',
        52: 'telefon'
    }
    REL_TABLE = 'rel'

    OBJECT_ID = 'object_id'
    REQUEST = 'request'
    RELATIONS = 'rels'
    RELATION_ID = 'id'
    LIST_ID = 'list_id'
    ACTUAL = 'actual'
    REL_VALUE = 'value'
    REL = 'rel'
    DATE_TIME_START = 'date_time_start'
    DATE_TIME_END = 'date_time_end'

    SEARCH_URL = DEPLOY_SETTING['manticore']['SEARCH_URL'] if mode == 'deploy' else 'http://200.200.200.235:9412/search'
    OSM_SEARCH_URL = DEPLOY_SETTING['manticore']['OSM_SEARCH_URL'] if mode == 'deploy' else 'http://200.200.200.235:9412/search'
    INSERT_URL = DEPLOY_SETTING['manticore']['INSERT_URL'] if mode == 'deploy' else 'http://200.200.200.235:9412/insert'
    UPDATE_URL = DEPLOY_SETTING['manticore']['UPDATE_URL'] if mode == 'deploy' else 'http://200.200.200.235:9412/update'
