# -*- coding: utf-8 -*-

##################################################################################################################
# работа ТОЛЬКО через remvb
##################################################################################################################


import logging, logging.handlers
import requests
import datetime
import time
import threading

from   fun.funSys   import logger, logError


#####################################################
# ВЗАИМОДЕЙСТВИЕ С VIBER
#####################################################
# logID - если не задан - лог не ведется
#####################################################
class Viber():
    PATH_SET_MSG = 'set/msg/'
    PATH_GET_LOG = 'get/log/'

    def __init__(self, urlServer, logID=''):
        self.urlServer = urlServer
        self.logID     = logID

        if self.logID!='':
            self.threadLog = LoggerThread(logID=self.logID, funViber=self.get_log, interval=10)
            self.threadLog.start()
        logger.debug(self.logID+' GO!')


    def free(self):
        if self.logID!='':
            self.threadLog.stop()
            self.threadLog.join()
        logger.debug(self.logID+' STOP!')



    #####################################################
    # ОТПРАВИТЬ СООБЩЕНИЕ
    #####################################################
    def set_msg(self, msg=''):
        msg=msg.strip()
        if msg=='': return {}
        try:
            ret = requests.post(self.urlServer+self.PATH_SET_MSG, json={'msg':msg}).json()
        except Exception as e:
            logger.error((self.logID+' ERROR set_msg: {}').format(e))
            ret = {}
        return ret


    #####################################################
    # ПОЛУЧИТЬ ЛОГИ
    #####################################################
    def get_log(self):
        try:
            ret = requests.post(self.urlServer+self.PATH_GET_LOG, json={})
            ret = ret.json() if ret.status_code==200 else {}
        except Exception as e:
            logger.error((self.logID+' ERROR get_log: {}').format(e))
            ret = {}
        return ret



class LoggerThread(threading.Thread):
    def __init__(self, logID, funViber, interval=10):
        threading.Thread.__init__(self)
        self.isStop   = False
        self.logID    = logID
        self.interval = interval
        logger.debug(self.logID+' GO Thread!')
        self.funViber = funViber

    def run(self):
        iCount = self.interval-3
        while True:
            if self.isStop: break
            try:
                time.sleep(1)
                iCount += 1
                if iCount>=self.interval:
                    iCount = 0

                    dat = self.funViber()
                    if dat.get('ret', '')!='ok': continue
                    for item in dat.get('log', []):
                        logger.info(self.logID+' '+item)
                        print(self.logID, item)
            except Exception as e:
                logError(e)

    def stop(self):
        self.isStop = True
        logger.debug(self.logID+' STOP Thread!')
