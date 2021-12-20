# -*- coding: utf-8 -*-

class CONNECT:
    HOST                   = ''
    PORT                   = 5000

class SERVER_TEXT:
    KEY_TYPE               = 'type'
    KEY_PARAM              = 'param'
    KEY_DATA               = 'data'

    KEY_RET_FLAG           = 'flag'
    KEY_RET_DATA           = 'data'

    TYPE_W2V_SIM           = 0
    TYPE_TFIDF_SIM         = 1
    TYPE_TFIDF_GROUP       = 2
    TYPE_DATA              = 3
    TYPE_SQL               = 4

    TYPE_BOT_GET           = 10                      # ML_BOT.TABLE: выбрать ответ
    TYPE_BOT_SET           = 11                      # ML_BOT.TABLE: добавить запись
    TYPE_BOT_IMPORT        = 12                      # ML_BOT.TABLE: импортировать записи

    DATA_BOT_QUEST         = 'quest'
    DATA_BOT_ANSWER        = 'answer'
    DATA_BOT_HOST          = 'host'
    DATA_BOT_AUTHOR_ID     = 'author_id'
    DATA_BOT_DATE_FROM     = 'date_from'

    PARAM_COUNT            = 'count'
    PARAM_SIM              = 'sim'
    PARAM_DATA_2           = 'data_2'
    PARAM_UNIQUE           = 'unique'
    PARAM_CORRECT          = 'correct'
    PARAM_SQL_TYPE         = 'sql_type'
    PARAM_SQL_TYPE_2       = 'sql_type_2'
    PARAM_SQL_TYPE_AUTO    = 0
    PARAM_SQL_TYPE_BD      = 1
    PARAM_SQL_TYPE_SPHINX  = 2
