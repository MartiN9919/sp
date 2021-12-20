# -*- coding: utf-8 -*-
import sys

class DAEMON_INI:
    # идентификатор процесса
    WORKER = ''

    if str(__file__) == '/home/dev/sp2/backend_ml/daemons/mlServerText/daemonIni.py':
        # FOR DEVELOPER SERVER
        PATH_ROOT    = '/home/dev/sp2/backend_ml/'
        FILE_LOG     = PATH_ROOT+'daemons/mlServerText/mlServerText.log'
        FILE_PID     = PATH_ROOT+'daemons/mlServerText/mlServerText.pid'
        PATH_PROJECT = PATH_ROOT
        PATH_LIB     = '/media/sf_D_DRIVE/!!! АРХИВ !!!/!!! LIB !!!/'
    else:
        # FOR PRODUCTION SERVER
        PATH_ROOT    = '/var/www/atlas/'
        FILE_LOG     = PATH_ROOT+'sys/log/mlServerText.log'
        FILE_PID     = PATH_ROOT+'sys/log/mlServerText.pid'
        PATH_PROJECT = PATH_ROOT+'project/'
        PATH_LIB     = PATH_PROJECT+'files/db/lib/'



sys.path.append(DAEMON_INI.PATH_PROJECT)
sys.path.append(DAEMON_INI.PATH_PROJECT+'daemons/mlServerText/')

from mlServerText import start

def runPointer():
    start()
