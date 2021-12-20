# -*- coding: utf-8 -*-

from daemonIni import DAEMON_INI

# запуск мониторинга
def start():
    from mlServerTextClass import MLServerText
    MLServerText(DAEMON_INI.PATH_LIB, DAEMON_INI.WORKER)

# запуск без демона
if __name__ == "__main__":
    import fun.funSys
    fun.funSys.setLogger(DAEMON_INI.FILE_LOG)

    start()
