# -*- coding: utf-8 -*-

import time
from   lib.funSys    import logger, logging, logError
from   lib.funBD     import varGet
from   lib.funBDArc  import ArcWriter
from   lib.funLoader import getNodSite
from   parserSiteRSS import parserSiteRSS


#==============================================================================
#    МЕНЕДЖЕР SITE_RSS
#==============================================================================
class LoaderSiteRSS():
    def __init__(self, worker):
        #logger.setLevel(logging.DEBUG)
        VAR_OWNER   = 'loaderSiteRSS'
        self.worker = worker
        self.isStop = False
        self.bios   = {}
        self.bios["wArc"] = ArcWriter  (10000, 1000, True, False, False)
        try:
            logger.info('START!')
            time.sleep(1)                                                                           # задержка первого старта, сек.
            while not self.isStop:
                try:
                    countRec  = 0
                    maxOld    = int(varGet(VAR_OWNER, self.worker, 'maxOld',    '4320'))*60         # качать не старше, мин., 0 - качать всё
                    delayNext = int(varGet(VAR_OWNER, self.worker, 'delayNext', '60'))              # задержка между интерациями, сек., 0-без задержки
                    timeStart = time.time()                                                         # время начала текущего цикла
                    timeNext  = timeStart+delayNext                                                 # время начала следующего цикла
                    timeOld   = 0 if maxOld == 0 else ((timeStart - maxOld) // 60 * 60)             # самое раннее время для выкачки, обязательно удалять секунды
                    logger.debug('GO! maxOld='+str(maxOld//60)+' delayNext='+str(delayNext))

                    for rec in getNodSite(self.worker):
                        try:                                                                        # ошибка в обработчике не должна прерывать процесс
                            countRec += parserSiteRSS(self.bios, rec, timeOld)                      # парсинг
                        except Exception as e:
                            logError(e)

                except Exception as e:
                    logError(e)
                finally:
                    if 'timeNext' in locals():
                        logger.info('OK! '+str(countRec).rjust(3)+' rec. '+str(round(time.time() - timeStart)).rjust(3)+' s.')
                        i = timeNext-time.time()                                                    # ожидать оставшееся время
                        if i > 0: time.sleep(i)

        except KeyboardInterrupt:
            msg = 'Aborted by user. Wait for completion of processes ...'
            logger.info(msg)
            print('\n'+msg)
        finally:
            self.bios["wArc"] .stop(True)                                                           # закрыть потоки с ожиданием
            self.bios = None
            logger.info('EXIT!')

    def stop(self):
        self.isStop = True
