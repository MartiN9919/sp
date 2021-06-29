class FullTextSearch:
    TABLES = {
        10: 'free',
        15: 'file',
        20: 'free',
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
    RELATION_ID = 'rel_id'
    LIST_ID = 'list_id'

    SEARCH_URL = 'http://200.200.200.235:9312/search'
