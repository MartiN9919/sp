# -*- coding: utf-8 -*-
import sys

class DAEMON_INI:
    # идентификатор процесса
    WORKER       = ''

    # [период сканирования в минутах, полный функционал: members, ...], [[даты запуска], [часы запуска]]
    PERIODS      = [[[60,    False], [[-1], [-1]]],                                 # час
                    [[1500,  False], [[-1], [6 ]]],                                 # сутки   1440
                    [[1500,  True ], [[-1], [23]]]]                                 # сутки   1440

    if str(__file__) == '/home/dev/sp2/backend_loaders/daemons/loaderTG/daemonIni.py':
        # FOR DEVELOPER SERVER
        PATH_ROOT    = '/home/dev/sp2/backend_loaders/'
        FILE_LOG     = PATH_ROOT+'log/loaderTG.log'
        FILE_PID     = PATH_ROOT+'pid/loaderTG.pid'
        FILE_BASE    = PATH_ROOT+'files/db/'
        PATH_DAEMON  = PATH_ROOT+'daemons/loaderTG/'
        PATH_PROJECT = PATH_ROOT
    else:
        # FOR PRODUCTION SERVER
        PATH_ROOT    = '/var/www/atlas/'
        FILE_LOG     = PATH_ROOT+'sys/log/loaderTG.log'
        FILE_PID     = PATH_ROOT+'sys/log/loaderTG.pid'
        FILE_BASE    = PATH_ROOT+'project/files/db/'
        PATH_DAEMON  = PATH_ROOT+'project/daemons/loaderTG/'
        PATH_PROJECT = PATH_ROOT+'project/'

sys.path.append(DAEMON_INI.PATH_PROJECT)

from loaderTG import start

def runPointer():
    start()
