# -*- coding: utf-8 -*-
import sys

class DAEMON_INI:
    # идентификатор процесса
    WORKER = ''

    if str(__file__) == '/home/web/prog/atlas/daemons/chatSlack/daemonIni.py':
        # FOR DEVELOPER SERVER
        PATH_ROOT    = '/home/web/prog/atlas/'
        FILE_LOG     = PATH_ROOT+'daemons/chatSlack/chatSlack.log'
        FILE_PID     = PATH_ROOT+'daemons/chatSlack/chatSlack.pid'
        PATH_PROJECT = PATH_ROOT
    else:
        # FOR PRODUCTION SERVER
        PATH_ROOT    = '/var/www/atlas/'
        FILE_LOG     = PATH_ROOT+'sys/log/chatSlack.log'
        FILE_PID     = PATH_ROOT+'sys/log/chatSlack.pid'
        PATH_PROJECT = PATH_ROOT+'project/'



sys.path.append(DAEMON_INI.PATH_PROJECT)
sys.path.append(DAEMON_INI.PATH_PROJECT+'daemons/chatSlack/')
sys.path.append(DAEMON_INI.PATH_PROJECT+'daemons/mlServerText/')

from chatSlack import start

def runPointer():
    start()
