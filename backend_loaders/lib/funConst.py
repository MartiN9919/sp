class BD:
      HOST         = '200.200.200.233'
      PORT         = 3306
      USER         = 'dev'
      PASSWORD     = '1'
      DB           = 'vec_load'
      CHARSET      = 'utf8'

class SPHINX:
      HOST         = '200.200.200.235'
      PORT         = 9306
      CHARSET      = 'utf8'


###############################################################################
# ARC
###############################################################################
class ARC:
      TABLE        = BD.DB+'.arc'     # T_ARC = BD_ATLAS+'.arc'
      TABLE_REP    = BD.DB+'.arc_rep'

      ID           = 'id'
      CRC          = 'crc'
      CRC_REL      = 'crc_rel'
      TYPE         = 'type'
      DATE         = 'dat'
      HOST         = 'host'
      SOURCE       = 'source'
      GROUP_ID     = 'group_id'
      TITLE_ID     = 'title_id'
      TITLE_NAME   = 'title_name'
      CONTENT      = 'content'
      AUTHOR_ID    = 'author_id'
      AUTHOR_NAME  = 'author_name'
      COUNTRY      = 'country'
      EMOTION      = 'emotion'
      VIEW_ALL     = 'view_all'
      LIKE_YES     = 'like_yes'
      LIKE_NO      = 'like_no'
      REPOST       = 'repost'
      DEL          = 'del'
      REFRESH      = 'refresh'
      INDMAIN      = 'indmain'

      TYPE_SOCIAL  = '2'
      TYPE_RSS     = '3'
      TYPE_SITE    = '4'


class IARC:
      TABLE        = 'iarc'
      TABLE_MAIN   = 'iarc_main'
      TABLE_DELTA  = 'iarc_delta'

      ID           = ARC.ID
      CRC_REL      = ARC.CRC_REL
      TYPE         = ARC.TYPE
      DATE         = ARC.DATE
      HOST         = ARC.HOST
      IHOST        = 'i'+ARC.HOST
      SOURCE       = ARC.SOURCE
      GROUP_ID     = ARC.GROUP_ID
      IGROUP_ID    = 'i'+ARC.GROUP_ID
      TITLE_ID     = ARC.TITLE_ID
      ITITLE_ID    = 'i'+ARC.TITLE_ID
      TITLE_NAME   = ARC.TITLE_NAME
      CONTENT      = ARC.CONTENT
      AUTHOR_ID    = ARC.AUTHOR_ID
      IAUTHOR_ID   = 'i'+ARC.AUTHOR_ID
      AUTHOR_NAME  = ARC.AUTHOR_NAME
      COUNTRY      = ARC.COUNTRY
      ICOUNTRY     = 'i'+ARC.COUNTRY
      EMOTION      = ARC.EMOTION
      VIEW_ALL     = ARC.VIEW_ALL
      LIKE_YES     = ARC.LIKE_YES
      LIKE_NO      = ARC.LIKE_NO
      REPOST       = ARC.REPOST
      DEL          = ARC.DEL
      SNIPPET      = 'snippet'


# class ARC_DOP:
#       TABLE        = BD.DB+'.arc_dop'

#       ID           = 'id'
#       TITLE_W2C    = 'title_w2c'


class ARC_DYNAMIC:
      TABLE        = BD.DB+'.arc_dynamic'

      CRC_ARC      = 'crc_arc'
      CRC          = 'crc'
      REFRESH      = 'refresh'
      AUTHOR_NAME  = ARC.AUTHOR_NAME
      VIEW_NOW     = 'view_now'
      VIEW_ALL     = ARC.VIEW_ALL
      LIKE_YES     = ARC.LIKE_YES
      LIKE_NO      = ARC.LIKE_NO
      REPOST       = ARC.REPOST



###############################################################################
# REL
###############################################################################
class REL:
      TABLE        = BD.DB+'.rel'

      ID           = 'id'
      CRC          = 'crc'
      TO_HOST      = 'to_host'
      TO_ID        = 'to_id'
      FROM_HOST    = 'from_host'
      FROM_ID      = 'from_id'
      TYPE         = 'type'
      HOST         = 'host'
      OBJECT       = 'object'
      SOURCE       = 'source'
      REFRESH      = 'refresh'
      INDMAIN      = 'indmain'

      TYPE_COMMON  = '0'
      TYPE_RELATIV = '1'  # родственник
      TYPE_ARC     = '5'  # публикация
      TYPE_GROUP   = '6'  # член группы
      TYPE_FRIEND  = '7'  # друг
      TYPE_FOLLOW  = '8'  # подписчик
      TYPE_LIKE    = '9'  # лайк
      TYPE_REPOST  = '10' # репост
      TYPE_ADMIN   = '50' # админ


class IREL:
      TABLE        = 'irel'
      TABLE_MAIN   = 'irel_main'
      TABLE_DELTA  = 'irel_delta'

      ID           = REL.ID
      CRC          = REL.CRC
      TO_HOST      = REL.TO_HOST
      ITO_HOST     = 'i'+REL.TO_HOST
      TO_ID        = REL.TO_ID
      ITO_ID       = 'i'+REL.TO_ID
      FROM_HOST    = REL.FROM_HOST
      IFROM_HOST   = 'i'+REL.FROM_HOST
      FROM_ID      = REL.FROM_ID
      IFROM_ID     = 'i'+REL.FROM_ID
      TYPE         = REL.TYPE
      HOST         = REL.HOST
      OBJECT       = REL.OBJECT
      SOURCE       = REL.SOURCE




###############################################################################
# UNIT
###############################################################################
class UNIT_TYPE:
      TABLE          = BD.DB+'.unit_type'

      ID             = 'id'
      NAM            = 'nam'
      DESCRIPT       = 'descript'

class UNIT:
      TABLE              = BD.DB+'.unit'
      TABLE_DYNAMIC_MAIN = BD.DB+'.unit_dynamic_main'
      TABLE_DYNAMIC_REL  = BD.DB+'.unit_dynamic_rel'

      HOST               = 'host'
      ID                 = 'id'
      UNIT_TYPE_ID_1     = 'unit_type_id_1'
      UNIT_TYPE_ID_2     = 'unit_type_id_2'
      UNIT_TYPE_ID_3     = 'unit_type_id_3'
      REFRESH            = 'refresh'
      REFRESH_REL        = 'refresh_rel'
      CRC_DYNAMIC_MAIN   = 'crc_dynamic_main'
      CRC_DYNAMIC_REL    = 'crc_dynamic_rel'

      SOURCE             = 'source'
      NAME               = 'name'
      BDATE              = 'bdate'
      RDATE              = 'rdate'
      COUNTRY            = 'country'
      CITY               = 'city'
      INFO               = 'info'
      DESCRIPT           = 'descript'

      TO_ALL             = 'to_all'
      TO_RELATIV         = 'to_relativ'
      TO_ARC             = 'to_arc'
      TO_GROUP           = 'to_group'
      TO_FRIEND          = 'to_friend'
      TO_FOLLOW          = 'to_follow'
      TO_FOLLOW_ALL      = 'to_follow_all'
      TO_LIKE            = 'to_like'
      TO_REPOST          = 'to_repost'
      TO_ADMIN           = 'to_admin'
      FROM_ALL           = 'from_all'
      FROM_ARC           = 'from_arc'
      FROM_GROUP         = 'from_group'
      FROM_FOLLOW        = 'from_follow'
      FROM_LIKE          = 'from_like'
      FROM_REPOST        = 'from_repost'
      FROM_ADMIN         = 'from_admin'

      VISIT_DATE         = 'visit_date'
      VISIT_DEVICE       = 'visit_device'

      LIST_TO = {}
      LIST_TO[REL.TYPE_RELATIV]  = TO_RELATIV
      LIST_TO[REL.TYPE_ARC]      = TO_ARC
      LIST_TO[REL.TYPE_GROUP]    = TO_GROUP
      LIST_TO[REL.TYPE_FRIEND]   = TO_FRIEND
      LIST_TO[REL.TYPE_FOLLOW]   = TO_FOLLOW
      LIST_TO[REL.TYPE_LIKE]     = TO_LIKE
      LIST_TO[REL.TYPE_REPOST]   = TO_REPOST
      LIST_TO[REL.TYPE_ADMIN]    = TO_ADMIN

      LIST_FROM = {}
      LIST_FROM[REL.TYPE_ARC]    = FROM_ARC
      LIST_FROM[REL.TYPE_GROUP]  = FROM_GROUP
      LIST_FROM[REL.TYPE_FOLLOW] = FROM_FOLLOW
      LIST_FROM[REL.TYPE_LIKE]   = FROM_LIKE
      LIST_FROM[REL.TYPE_REPOST] = FROM_REPOST
      LIST_FROM[REL.TYPE_ADMIN]  = FROM_ADMIN

      VISIT_DEVICE_UNKNOW = '0'      # не установлено
      VISIT_DEVICE_FULL   = '1'      # полная версия сайта
      VISIT_DEVICE_MOBILE = '2'      # мобильная версия сайта
      VISIT_DEVICE_APP    = '3'      # приложение



###############################################################################
# LOADER
###############################################################################
class LOADER_TYPE:
      TABLE          = BD.DB+'.loader_type'

      ID             = 'id'
      NAM            = 'nam'
      DESCRIPT       = 'descript'
      REFRESH        = 'refresh'

      ID_RSS         = '2'
      ID_SITE        = '3'
      NAM_SOCHIAL    = 'Соцсеть'

class LOADER_NOD:
      TABLE          = BD.DB+'.loader_nod'

      ID             = 'id'
      LOADER_TYPE_ID = 'loader_type_id'
      NOD_TYPE_ID    = 'nod_type_id'
      HOST           = 'host'
      GROUP_ID       = 'group_id'
      NAME           = 'name'
      URL            = 'url'
      PARAM          = 'param'
      COUNTRY        = 'country'
      TS_CORRECT     = 'ts_correct'
      WORKER         = 'worker'
      ENABLED        = 'enabled'
      VIP            = 'vip'
      DESCRIPT       = 'descript'
      REFRESH        = 'refresh'

      WORKER_STANDART = ''
      WORKER_TURBO    = 'Turbo'
      WORKER_LIST     = (
          (WORKER_STANDART, 'Стандартный'),
          (WORKER_TURBO,    'Турбо'),
      )


class LOADER_SYNC:
      TABLE          = BD.DB+'.loader_sync'

      HOST           = 'host'
      VAR1           = 'var1'
      VAR2           = 'var2'
      VAL            = 'val'
      DESCRIPT       = 'descript'


class LOADER_URL:
      TABLE          = BD.DB+'.loader_url'

      URL            = 'url'
      DATE_DEL       = 'date_del'


class LOADER_LIST:
      TABLE          = BD.DB+'.loader_list'

      OWNER          = 'owner'
      WORKER         = 'worker'
      VAL1           = 'val1'
      VAL2           = 'val2'
      VAL3           = 'val3'
      VAL4           = 'val4'
      DAT            = 'dat'



###############################################################################
# NOD
###############################################################################
class NOD_TYPE:
      TABLE          = BD.DB+'.nod_type'

      ID             = 'id'
      NAM            = 'nam'
      DESCRIPT       = 'descript'
      REFRESH        = 'refresh'


class NOD:
      TABLE          = BD.DB+'.nod'

      ID             = 'id'
      NOD_TYPE_ID    = 'nod_type_id'
      NAM            = 'nam'
      VAL            = 'val'
      ENABLED        = 'enabled'
      DESCRIPT       = 'descript'
      REFRESH        = 'refresh'

      NAM_ALL        = 'ALL'              # псевдообъект интереса: все за исключением @, результат приблизительный

###############################################################################
# MON
###############################################################################
class MON:
      TABLE          = BD.DB+'.mon'

      MON_TYPE_ID    = 'mon_type_id'
      DATE           = 'dat'
      HOST           = 'host'
      NAM            = 'nam'
      VAL            = 'val'
      URL            = 'url'
      BORN           = 'born'


class MON_TYPE:
      TABLE          = BD.DB+'.mon_type'

      ID             = 'id'
      WORKER         = 'worker'
      SORT           = 'sort'
      TITLE          = 'title'
      HANDLER        = 'handler'
      PARAM_1        = 'param_1'
      PARAM_2        = 'param_2'
      PARAM_3        = 'param_3'
      NOD            = 'nod'
      STEP           = 'step'
      ROW_COUNT      = 'row_count'
      WIDTH          = 'width'
      COLOR          = 'color'
      ENABLED        = 'enabled'
      DESCRIPT       = 'descript'
      READY          = 'ready'
      DATE           = 'dat'
      REFRESH        = 'refresh'

      WORKER_STANDART = ''
      WORKER_TURBO    = 'Turbo'
      WORKER_LIST     = (
          (WORKER_STANDART, 'Стандартный'),
          (WORKER_TURBO,    'Турбо'),
      )

      SORT_AUTO      = '1000'

      HANDLER_REPORT = 'report'
      HANDLER_GROUP  = 'group'
      HANDLER_UNIQUE = 'unique'
      HANDLER_DYNAMIC= 'dynamic'
      HANDLER_ANOMALY= 'anomaly'
      HANDLER_SQL    = 'sql'
      HANDLER_LIST   = (
          ('',              ''),
          (HANDLER_GROUP,   'Группировка'),
          (HANDLER_DYNAMIC, 'Динамика'),
          (HANDLER_UNIQUE,  'Уникальности'),
          (HANDLER_ANOMALY, 'Аномалии'),
          (HANDLER_SQL,     'Произвольный запрос'),
      )

      PARAM_2_ALL    = 'all'

      # связано с classMonBlock.js COLOR_LIST
      COLOR_BLUE     = 'Blue'
      COLOR_NAVY     = 'Navy'
      COLOR_GREEN    = 'Green'
      COLOR_TURQUOISE= 'Turquoise'
      COLOR_PURPLE   = 'Purple'
      COLOR_YELLOW   = 'Yellow'
      COLOR_RED      = 'Red'
      COLOR_BROWN    = 'Brown'
      COLOR_PEACH    = 'Peach'
      COLOR_GRAY     = 'Gray'
      COLOR_WHITE    = 'White'
      COLOR_BLACK    = 'Black'
      COLOR_LIST   = (
          ('',              ''),
          (COLOR_BLUE,      'Голубой'),
          (COLOR_NAVY,      'Синий'),
          (COLOR_GREEN,     'Зеленый'),
          (COLOR_TURQUOISE, 'Бирюзовый'),
          (COLOR_PURPLE,    'Фиолетовый'),
          (COLOR_YELLOW,    'Оранжевый'),
          (COLOR_RED,       'Красный'),
          (COLOR_BROWN,     'Коричневый'),
          (COLOR_PEACH,     'Персиковый'),
          (COLOR_GRAY,      'Серый'),
          (COLOR_WHITE,     'Белый'),
          (COLOR_BLACK,     'Черный'),
      )



###############################################################################
# BOT
###############################################################################
class BOT:
      TABLE          = BD.DB+'.bot'

      ID             = 'id'
      BOT_TYPE_ID    = 'bot_type_id'
      HOST           = 'host'
      MSG_VAL        = 'msg_val'
      MSG_NAM        = 'msg_nam'
      URL            = 'url'
      DATE           = 'dat'
      REFRESH        = 'refresh'
      SHOW_SLACK     = 'show_slack'
      SLACK_TS       = 'slack_ts'

      MSG_BOLD_START = '[BOLD]'
      MSG_BOLD_END   = '[/BOLD]'



class BOT_TYPE:
      TABLE          = BD.DB+'.bot_type'

      ID             = 'id'
      MON_TYPE_ID    = 'mon_type_id'
      WORKER         = 'worker'
      SORT           = 'sort'
      CHANNEL_SLACK  = 'channel_slack'
      TITLE_VAL      = 'title_val'
      TITLE_NAM      = 'title_nam'
      VAL_SORT       = 'val_sort'
      VAL_MIN        = 'val_min'
      VAL_RISE       = 'val_rise'
      VAL_FRESH      = 'val_fresh'
      VAL_TOP        = 'val_top'
      ENABLED        = 'enabled'
      DESCRIPT       = 'descript'
      REFRESH        = 'refresh'

      WORKER_STANDART = ''
      SORT_AUTO       = '1000'

      VAL_SORT_TO_NAME = {
          '0': 'Отсутствует',
          '1': 'Абс. значение',
          '2': 'Рост, абс.',
          '3': 'Рост, %',
      }



###############################################################################
# REPORTS
###############################################################################
class REP:
      TABLE          = BD.DB+'.rep'

      ID             = 'id'
      REP_TYPE_ID    = 'rep_type_id'
      DATE_DEL       = 'date_del'



class REP_TYPE:
      TABLE          = BD.DB+'.rep_type'

      ID             = 'id'
      WORKER         = 'worker'
      SORT           = 'sort'
      PARAM          = 'param'
      ARGS           = 'args'
      TIMING         = 'timing'
      START_ONCE     = 'start_once'
      ENABLED        = 'enabled'
      DESCRIPT       = 'descript'
      REFRESH        = 'refresh'



###############################################################################
# HOST
###############################################################################
class HOST:
      LOCAL          = 'local'
      REPORT         = 'report'
      TALKS          = 'talks.by'
      ONLINER        = 'onliner.by'
      VK             = 'vk.com'
      TG             = 'telegram.org'
      TW             = 'twitter.com'
      FB             = 'facebook.com'

class HOST_SHORT:
      LOCAL          = 'local'
      REPORT         = 'report'
      TALKS          = 'talks'
      ONLINER        = 'onliner'
      VK             = 'vk'
      TG             = 'tg'
      TW             = 'tw'
      FB             = 'fb'

HOST2HOST_SHORT      = {
      HOST.LOCAL     : HOST_SHORT.LOCAL,
      HOST.REPORT    : HOST_SHORT.REPORT,
      HOST.TALKS     : HOST_SHORT.TALKS,
      HOST.ONLINER   : HOST_SHORT.ONLINER,
      HOST.VK        : HOST_SHORT.VK,
      HOST.TG        : HOST_SHORT.TG,
      HOST.TW        : HOST_SHORT.TW,
      HOST.FB        : HOST_SHORT.FB,
}



###############################################################################
# FILE
###############################################################################
class FILE:
      TABLE          = BD.DB+'.file'

      PATH           = 'path'
      SOURCE         = 'source'
      HOST           = 'host'
      ARC_CRC        = 'arc_crc'
      UNIT_ID        = 'unit_id'
      ACTION         = 'action'
      DESCRIPT       = 'descript'
      REFRESH        = 'refresh'

      # TYPE_NONE      = 0
      # TYPE_PHOTO     = 1
      # TYPE_VIDEO     = 2
      # TYPE_AUDIO     = 3
      # TYPE_DOC       = 4
      # TYPE_REPORT    = 10

      ACTION_NONE    = 0
      ACTION_LOAD    = 1
      ACTION_DEL     = 2

      NONE_32        = 'none32.png'
      NONE_128       = 'none128.png'


# ПУТЬ К ФАЙЛУ ИКОНКИ ЮНИТА (НЕ ПУТАТЬ С ИКОНКАМИ ХОСТА)
FILE_UNIT_ICON = {
      HOST.TALKS       : 'icon.gif',
      #HOST.ONLINER    : 'icon.png',
      HOST.VK          : 'icon.jpg',
      HOST.TG          : 'icon.jpg',
      #HOST.TW         : 'icon.jpg',
      #HOST.FB         : 'icon.png',
      HOST_SHORT.TALKS : 'icon.gif',
      HOST_SHORT.VK    : 'icon.jpg',
      HOST_SHORT.TG    : 'icon.jpg',
}


###############################################################################
# PHONE
###############################################################################
class PHONE_LIST:
      TABLE          = BD.DB+'.phone_list'

      PHONE          = 'phone'
      ENABLED_TG     = 'enabled_tg'
      DESCRIPT       = 'descript'

      ENABLED_HOST   = {
          HOST.TG:   ENABLED_TG,
      }


class PHONE_ACCOUNT:
      TABLE          = BD.DB+'.phone_account'

      HOST           = 'host'
      ID             = 'id'
      PHONE          = 'phone'
      NAME           = 'name'
      NAME_VISIBLE   = 'name_visible'
      URL            = 'url'
      REFRESH        = 'refresh'



###############################################################################
# EMO
###############################################################################
class EMO:
      TABLE          = BD.DB+'.emo'

      ID             = 'id'
      LEX            = 'lex'
      WEIGHT         = 'weight'


###############################################################################
# ML_EMO
###############################################################################
class ML_EMO:
      TABLE          = BD.DB+'.ml_emo'

      ID             = 'id'
      TEXT           = 'text'
      WEIGHT         = 'weight'


###############################################################################
# ML_BOT
###############################################################################
class ML_BOT:
      TABLE          = BD.DB+'.ml_bot'

      ID             = 'id'
      CRC            = 'crc'
      TYPE_ID        = 'type_id'
      QUESTION       = 'question'
      ANSWER         = 'answer'
      HOST           = 'host'
      AUTHOR_ID      = 'author_id'
      DATE           = 'dat'

      HOST_SLACK     = 'slack'


class ML_BOT_TYPE:
      TABLE          = BD.DB+'.ml_bot_type'

      ID             = 'id'
      NAM            = 'nam'
      DESCRIPT       = 'descript'

      ID_COMMON      = 1


###############################################################################
# SQL_TAB
###############################################################################
class SQL_TAB:
      TABLE          = BD.DB+'.sql_tab'

      ID             = 'id'
      PARENT_ID      = 'parent_id'
      TITLE          = 'title'
      HINT           = 'hint'
      REQUEST        = 'request'
      EXEC           = 'exec'
      ENABLED        = 'enabled'
      DESCRIPT       = 'descript'



###############################################################################
# VAR
###############################################################################
class VAR:
      TABLE          = BD.DB+'.var'

      OWNER          = 'owner'
      WORKER         = 'worker'
      NAME           = 'name'
      VALUE          = 'value'
      ENABLED        = 'enabled'
      DESCRIPT       = 'descript'
      REFRESH        = 'refresh'



###############################################################################
# NOTE
###############################################################################
class NOTE:
      TABLE          = BD.DB+'.note'

      ID             = 'id'
      TITLE          = 'title'
      MSG            = 'msg'
      USER           = 'user'
      REFRESH        = 'refresh'



###############################################################################
# MANUAL
###############################################################################
class MANUAL:
      TABLE          = BD.DB+'.manual'

      ID             = 'id'
      ID_ITEM        = 'id_item'
      ID_PARENT      = 'id_parent'
      ID_ICON        = 'id_icon'
      TITLE          = 'title'
      CONTENT        = 'content'
      ENABLED        = 'enabled'



###############################################################################
class MSG:
      ERR_COMMON     = ["Ошибка сервера"]
      NO_TEXT        = '<текста нет>'


class CHR:
      RUS_ = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
      BEL  = 'іўІ'
      RUS  = RUS_+BEL
      ENG  = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
      ANY  = ' !"#$€%&~^*_+-|/\№;:?,.()<>=[]{}'+chr(10)+chr(13)
      NUM  = '0123456789'
      ALL  = RUS+ENG+ANY+NUM
