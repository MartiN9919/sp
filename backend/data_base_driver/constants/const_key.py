TYPES = [
    'str',
    'int',
    'float',
    'bit', 'data',
    'datatime',
    'geometry'
]


class SYS_KEY_CONSTANT:

    REL_ID = 1
    FREE_ID = 10
    FILE_ID = 15
    DOC_ID = 20
    POINT_ID = 25
    GEOMETRY_ID = 30
    PERSON_P_ID = 35
    PERSON_L_ID = 40
    CASE_ID = 45
    TRANSPORT_ID = 50
    TELEFON_ID = 52

    FILE_CLASSIFIER_ID = 50183
    FILE_TEXT_CLASSIFIER_ID = 50216

    PHONE_NUMBER_CLASSIFIER_ID = 50054
    PHONE_NUMBER_COUNTRY_ID = 50055

    POINT_CLASSIFIER_ID = 25204
    POINT_TYPE_CLASSIFIER_ID = 50200

    BORDER_POINT = 50105

    GEOMETRY_CLASSIFIER_ID = 30304
    GEOMETRY_TYPE_CLASSIFIER_ID = 50199

    PARENT_ID_CLASSIFIER_ID = 30302

    PHOTO_PERSON_CLASSIFIER_ID = 50142
    PHOTO_GEOMETRY_CLASSIFIER_ID = 50204
    PHOTO_POINT_CLASSIFIER_ID = 50205
    PHOTO_TRANSPORT_CLASSIFIER_ID = 50207

    GEOMETRY_TYPES = [
        POINT_TYPE_CLASSIFIER_ID,
        GEOMETRY_TYPE_CLASSIFIER_ID,
    ]

    GEOMETRY_TRANSFER_LIST = [
        POINT_TYPE_CLASSIFIER_ID,
        GEOMETRY_TYPE_CLASSIFIER_ID,
    ]

    NOT_VALUE_TRANSFER_LIST = [
        30302,
        10000,
        10001,
        10002,
        10003,
        15000,
        15001,
        15002,
        15003,
        20001,
        20002,
        20003,
        20004
    ]

    LIST_ICONS_ID = 49