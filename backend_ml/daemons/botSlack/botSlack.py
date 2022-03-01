# -*- coding: utf-8 -*-

from daemonIni import DAEMON_INI

# from fun.funViber import Viber
# from fun.funSys   import logger, logError
# import time

# v = Viber(urlServer='https://remvb.herokuapp.com/', logFilePath='/home/web/prog/atlas/daemons/botSlack/viber.log')
# n = v.set_msg(msg='!!! https://tech.onliner.by/2019/07/09/phones-2019-1')
# print('!!!!!!', n)
# try:
#     time.sleep(6660)
# except KeyboardInterrupt:
#     msg = 'Aborted by user. Wait for completion of processes ...'
#     logger.info(msg)
#     print('\n'+msg)
# except (SystemExit, GeneratorExit, Exception) as e:
#     logError(e)
# finally:
#     if v != None:
#         v.free()
#         v = None
#     logger.info('EXIT!')
# raise

# n = v.get_log()
# print('!!!!!!', n)
# raise


# запуск мониторинга
def start():
    from botSlackClass import BotSlack
    BotSlack()

# запуск без демона
if __name__ == "__main__":
    import fun.funSys
    fun.funSys.setLogger(DAEMON_INI.FILE_LOG)                   # root также в demon.ini

    start()
