# -*- coding: utf-8 -*-
import sys

class DAEMON_INI:
    WORKER = ''                                                                     # идентификатор процесса
    IS_DEV = (str(__file__) == '/home/web/prog/atlas/daemons/botSlack/daemonIni.py') # признак работы в среде разработчика

    ICO_OK    = ':heavy_check_mark:'
    ICO_ERROR = ':no_entry:'
    ICO_LIST  = {
        '[alert]'     : [':zap:',                     'очень важно'],
        '[new]'       : [':new:',                     'новый объект'],
        '[anomaly]'   : [':question:',                'аномалия'],
        '[del]'       : [':skull_and_crossbones:',    'удалено'],

        '[nod]'       : [':star:',                    'объект интереса'],
        '[group]'     : [':busts_in_silhouette:',     'группа'],
        '[title]'     : [':triangular_flag_on_post:', 'тема'],                        # :triangular_flag_on_post: :waving_white_flag: :waving_black_flag:
        '[author]'    : [':bust_in_silhouette:',      'автор'],
        '[content]'   : [':writing_hand:',            'публикации (комментарии)'],    # :writing_hand: :speech_balloon: :memo:

        '[view]'      : [':eye:',                     'просмотры'],
        '[like_yes]'  : [':+1:',                      'лайки'],
        '[like_no]'   : [':-1:',                      'дизлайки'],
        '[repost]'    : [':loudspeaker:',             'репосты'],                     # :speaking_head_in_silhouette:
        '[repeat]'    : [':arrows_clockwise:',        'повторы'],                     # :arrows_clockwise: :repeat: :recycle: :arrows_counterclockwise:

        '[report]'    : [':bar_chart:',               'отчеты'],                      # :clipboard: :inbox_tray:
    }

    if IS_DEV:

        # FOR DEVELOPER SERVER
        PATH_ROOT    = '/home/web/prog/atlas/'
        FILE_LOG     = PATH_ROOT+'daemons/botSlack/botSlack.log'
        FILE_PID     = PATH_ROOT+'daemons/botSlack/botSlack.pid'
        PATH_VIBER   = PATH_ROOT+'daemons/botSlack/botSlack_'
        PATH_PROJECT = PATH_ROOT


        VERIFY_FILES = [
            PATH_ROOT+'daemons/loaderRSS/loaderRSSTurbo.pid',
            PATH_ROOT+'daemons/loaderRSS/loaderRSS.pid',
            PATH_ROOT+'daemons/loaderRSS/loaderSiteRSSTurbo.pid',
            PATH_ROOT+'daemons/loaderRSS/loaderSiteRSS.pid',
            PATH_ROOT+'daemons/loaderVK/loaderVK.pid',
            PATH_ROOT+'daemons/loaderVK/loaderTG.pid',
            PATH_ROOT+'daemons/loaderVK/loaderTW.pid',
            PATH_ROOT+'daemons/loaderVK/loaderFB.pid',
            PATH_ROOT+'daemons/loaderTalks/loaderTalks.pid',
            PATH_ROOT+'daemons/loaderOnliner/loaderOnliner.pid',
            PATH_ROOT+'daemons/loaderFile/loaderFile.pid',
            PATH_ROOT+'daemons/baseMon/baseMonTurbo.pid',
            PATH_ROOT+'daemons/baseMon/baseMon.pid',
            PATH_ROOT+'daemons/baseRep/baseRep.pid',
            PATH_ROOT+'daemons/baseBot/baseBot.pid',
            PATH_ROOT+'daemons/baseUnitRel/baseUnitRel.pid',
            PATH_ROOT+'daemons/botSlack/botSlack.pid',
            PATH_ROOT+'daemons/chatSlack/chatSlack.pid',
            PATH_ROOT+'daemons/mlServerText/mlServerText.pid',
        ]
        CONTENT_FILES = [
            PATH_ROOT+'daemons/loaderRSS/loaderRSSTurbo.log',
            PATH_ROOT+'daemons/loaderRSS/loaderRSS.log',
            PATH_ROOT+'daemons/loaderRSS/loaderSiteRSSTurbo.log',
            PATH_ROOT+'daemons/loaderRSS/loaderSiteRSS.log',
            PATH_ROOT+'daemons/loaderVK/loaderVK.log',
            PATH_ROOT+'daemons/loaderVK/loaderTG.log',
            PATH_ROOT+'daemons/loaderVK/loaderTW.log',
            PATH_ROOT+'daemons/loaderVK/loaderFB.log',
            PATH_ROOT+'daemons/loaderTalks/loaderTalks.log',
            PATH_ROOT+'daemons/loaderOnliner/loaderOnliner.log',
            PATH_ROOT+'daemons/loaderFile/loaderFile.log',
            PATH_ROOT+'daemons/baseMon/baseMonTurbo.log',
            PATH_ROOT+'daemons/baseMon/baseMon.log',
            PATH_ROOT+'daemons/baseRep/baseRep.log',
            PATH_ROOT+'daemons/baseBot/baseBot.log',
            PATH_ROOT+'daemons/baseUnitRel/baseUnitRel.log',
            PATH_ROOT+'daemons/botSlack/botSlack.log',
            PATH_ROOT+'daemons/chatSlack/chatSlack.log',
            PATH_ROOT+'daemons/mlServerText/mlServerText.log',
        ]

    else:

        # FOR PRODUCTION SERVER
        PATH_ROOT    = '/var/www/atlas/'
        FILE_LOG     = PATH_ROOT+'sys/log/botSlack.log'
        FILE_PID     = PATH_ROOT+'sys/log/botSlack.pid'
        PATH_VIBER   = PATH_ROOT+'sys/log/botSlack_'
        PATH_PROJECT = PATH_ROOT+'project/'


        VERIFY_FILES = [
            PATH_ROOT+'sys/log/loaderRSSTurbo.pid',
            PATH_ROOT+'sys/log/loaderRSS.pid',
            PATH_ROOT+'sys/log/loaderSiteRSSTurbo.pid',
            PATH_ROOT+'sys/log/loaderSiteRSS.pid',
            PATH_ROOT+'sys/log/loaderVK.pid',
            PATH_ROOT+'sys/log/loaderTG.pid',
            PATH_ROOT+'sys/log/loaderTW.pid',
            PATH_ROOT+'sys/log/loaderFB.pid',
            PATH_ROOT+'sys/log/loaderTalks.pid',
            PATH_ROOT+'sys/log/loaderOnliner.pid',
            PATH_ROOT+'sys/log/loaderFile.pid',
            PATH_ROOT+'sys/log/baseMonTurbo.pid',
            PATH_ROOT+'sys/log/baseMon.pid',
            PATH_ROOT+'sys/log/baseRep.pid',
            PATH_ROOT+'sys/log/baseBot.pid',
            PATH_ROOT+'sys/log/baseUnitRel.pid',
            PATH_ROOT+'sys/log/botSlack.pid',
            PATH_ROOT+'sys/log/chatSlack.pid',
            PATH_ROOT+'sys/log/mlServerText.pid',
        ]
        CONTENT_FILES = [
            PATH_ROOT+'sys/log/loaderRSSTurbo.log',
            PATH_ROOT+'sys/log/loaderRSS.log',
            PATH_ROOT+'sys/log/loaderSiteRSSTurbo.log',
            PATH_ROOT+'sys/log/loaderSiteRSS.log',
            PATH_ROOT+'sys/log/loaderVK.log',
            PATH_ROOT+'sys/log/loaderTG.log',
            PATH_ROOT+'sys/log/loaderTW.log',
            PATH_ROOT+'sys/log/loaderFB.log',
            PATH_ROOT+'sys/log/loaderTalks.log',
            PATH_ROOT+'sys/log/loaderOnliner.log',
            PATH_ROOT+'sys/log/loaderFile.log',
            PATH_ROOT+'sys/log/baseMonTurbo.log',
            PATH_ROOT+'sys/log/baseMon.log',
            PATH_ROOT+'sys/log/baseRep.log',
            PATH_ROOT+'sys/log/baseBot.log',
            PATH_ROOT+'sys/log/baseUnitRel.log',
            PATH_ROOT+'sys/log/botSlack.log',
            PATH_ROOT+'sys/log/chatSlack.log',
            PATH_ROOT+'sys/log/mlServerText.log',
        ]


sys.path.append(DAEMON_INI.PATH_PROJECT)
sys.path.append(DAEMON_INI.PATH_PROJECT+'daemons/botSlack/')
sys.path.append(DAEMON_INI.PATH_PROJECT+'daemons/mlServerText/')
#sys.path.append(DAEMON_INI.PATH_PROJECT+'daemons/botSlackTurbo/')

from botSlack import start

def runPointer():
    start()
