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


    SEARCH_URL = 'http://200.200.200.235:9312/search'
    LOCAL_SEARCH_URL = 'http://127.0.0.1:9312/search'
    INSERT_URL = 'http://200.200.200.235:9312/insert'
