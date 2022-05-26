# -*- coding: utf-8 -*-

from daemonIni import DAEMON_INI

# запуск мониторинга
def start():
    from loaderSiteRSSClass import LoaderSiteRSS
    LoaderSiteRSS(DAEMON_INI.WORKER)

# запуск без демона
if __name__ == "__main__":
    import lib.funSys
    lib.funSys.setLogger(DAEMON_INI.FILE_LOG)

    start()
