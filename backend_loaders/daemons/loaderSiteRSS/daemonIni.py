# -*- coding: utf-8 -*-
import sys
from   pathlib import Path

class DAEMON_INI:
    WORKER       = 'RSS'     # идентификатор процесса

    PATH_ROOT    = str(Path(__file__).resolve().parent.parent.parent)+'/'
    FILE_LOG     = PATH_ROOT+'log/loaderSiteRSS.log'
    FILE_PID     = PATH_ROOT+'pid/loaderSiteRSS.pid'
    PATH_PROJECT = PATH_ROOT

sys.path.append(DAEMON_INI.PATH_PROJECT)

from loaderSiteRSS import start

def runPointer():
    start()
