# -*- coding: utf-8 -*-

##################################################################################################################
# pip3 install -U PySocks     https://github.com/Anorov/PySocks#installation
# pip3 install -U telethon
##################################################################################################################

##################################################################################################################
# ИСПОЛЬЗОВАТЬ ID ДЛЯ ИДЕНТИФИКАЦИИ КАНАЛА НЕЛЬЗЯ, ТАК КАК КАНАЛ МОЖНО ПОЛУЧИТЬ ТОЛЬКО ЕСЛИ ОН РАНЕЕ ОБРАБАТЫВАЛСЯ
# поэтому
# arc.loader_nod: заполняем url ВРУЧНУЮ, а group_id и name заполняются АВТОМАТИЧЕСКИ
# для закрытых каналов в url указывать: joinchat/инвайт-код, а group_id, name, vip заполняются АВТОМАТИЧЕСКИ
##################################################################################################################

# для запуска без демона
from   daemonIni     import DAEMON_INI
#if __name__ == "__main__":
import sys
sys.path.append('.')  #/home/web/prog/atlas/')
sys.path.append('../../')

import lib.funSys
lib.funSys.setLogger(DAEMON_INI.FILE_LOG)





import time
from   tgApi         import TGRandom, TG_BD
from   tgParser      import TGParser

from   lib.funConst  import HOST, LOADER_NOD
from   lib.funSys    import logger, logError, tsNow, Periods
from   lib.funText   import textNormal, findStr
from   lib.funBD     import varGet
from   lib.funLoader import getNodObjects, GetNodObjects, setNodField



class LoaderTG():
    VAR_OWNER          = 'loaderTG'
    VAR_PRIOR_PERIOD   = 'priorPeriod'                                                          # период выкачки, мин. 0 - динамический
    VAR_PRIOR_ADVANCED = 'priorAdvanced'                                                        # полная выкачка, 0 - динамическая
    VAR_DELAY_NEXT     = 'delayNext'                                                            # минимальный промежуток между интерациями, мин
    VAR_DELAY_CHANNEL  = 'delayChannel'                                                         # задержка между каналами, сек
    VAR_DELAY_REQUEST  = 'delayRequest'                                                         # максимальная задержка между запросами, сек
    VAR_REC_ADVANCED   = 'recAdvanced'                                                          # сколько читать с канала сообщений в advanced режиме
    VAR_REC_NORMAL     = 'recNormal'                                                            # сколько читать с канала сообщений в normal режиме

    parser    = None
    tg        = None


    #####################################################
    # КОНСТРУКТОР
    #####################################################
    def __init__(self):
        #logger.setLevel(logging.DEBUG)
        logger.info('START!')
        try:
            self.tg = TGRandom(owner=self.VAR_OWNER, worker=DAEMON_INI.WORKER, varName='connect')
            print(self.tg)
            if self.tg == None: raise ValueError('LoaderTG.__init__: error ini telegram api')
            self.tg.client.session.save_entities = True                                             # сохранять локально input entites

            self.parser = TGParser(self.tg)
            if self.parser == None: raise ValueError('LoaderTG.__init__: error ini parser')
            if self.parser.isError: raise ValueError('LoaderTG.__init__: error ini parser')

            periods = Periods(DAEMON_INI.PERIODS, [60, False])
            if periods == None: raise ValueError('LoaderTG.__init__: error ini periods')

            while True:
                # синхронизацция (сверка) времени с ресурсом
                #if not vkParser.fun.isLoaderSync(): continue

                # интерация
                self.step(periods.getVal())

        except KeyboardInterrupt:
            msg = 'Aborted by user. Wait for completion of processes ...'
            logger.info(msg)
            print('\n'+msg)
        except (SystemExit, GeneratorExit, Exception) as e:
            logError(e)
        finally:
            if self.parser != None:
                self.parser.free()
                self.parser = None

            if self.tg != None:
                self.tg.free()
                self.tg = None
            logger.info('EXIT!')




    #####################################################
    # period - период выкачки в минутах, 0 - качать всё
    #####################################################
    def step(self, arg):
        ret           = False

        period        = int(varGet(self.VAR_OWNER, DAEMON_INI.WORKER, self.VAR_PRIOR_PERIOD))   # период выкачки, мин. 0 - динамический
        advanced      = int(varGet(self.VAR_OWNER, DAEMON_INI.WORKER, self.VAR_PRIOR_ADVANCED)) # полная выкачка, 0 - динамическая
        if period   == 0: period    = arg[0]
        if advanced == 0: advanced  = arg[1]

        delayNext     = int(varGet(self.VAR_OWNER, DAEMON_INI.WORKER, self.VAR_DELAY_NEXT))*60  # минимальный промежуток между интерациями, мин
        delayChannel  = int(varGet(self.VAR_OWNER, DAEMON_INI.WORKER, self.VAR_DELAY_CHANNEL))  # задержка между каналами, сек
        self.tg.delayRequest = int(varGet(self.VAR_OWNER, DAEMON_INI.WORKER, self.VAR_DELAY_REQUEST)) # максимальная задержка между запросами, сек
        self.tg.recMaxCount  = int(varGet(self.VAR_OWNER, DAEMON_INI.WORKER, (self.VAR_REC_ADVANCED if advanced else self.VAR_REC_NORMAL))) # сколько читать с канала сообщений

        timeStart     = time.time()                                                             # время начала текущего цикла
        timeNext      = timeStart+delayNext                                                     # время начала следующего цикла
        logger.info('GO! period='+str(period)+' advanced='+str(advanced)+' delayNext='+str(delayNext)+' delayChannel='+str(delayChannel)+' delayRequest='+str(self.tg.delayRequest)+' recMaxCount='+str(self.tg.recMaxCount))
        tsScanStart   = tsNow() // 60 * 60                                                      # обязательно удалять секунды
        tsPeriodStart = 0 if period == 0 else ((tsNow() - (period * 60)) // 60 * 60)            # обязательно удалять секунды
        countItem     = 0
        try:
            for item in getNodObjects(HOST.TG, DAEMON_INI.WORKER):                              # читать из LOADER_NOD в item
                try:                                                                            # ошибка не должна прерывать обрабоку других item
                    item_id    = item[GetNodObjects.GROUP_ID].strip()                           # из БД: id канала
                    item_name  = item[GetNodObjects.NAME]                                       # из БД: отображаемое имя канала
                    item_url   = item[GetNodObjects.URL].strip().lower()                        # из БД: url-наименование канала (обязательно в нижнем регистре)
                    item_vip   = bool(item[GetNodObjects.VIP])                                  # из БД: признак join к каналу
                    item_invite= findStr(item[GetNodObjects.URL].strip(), r'^joinchat/(.+)')    # инвайт для закрытого канала
                    item_entity= item_url if item_invite=='' else ('https://t.me/joinchat/'+item_invite) # идентификатор для определения entity_global и entity_local
                    countItem0 = countItem

                    if item_url == '':
                        logger.warning('Is not correct filed ['+LOADER_NOD.URL+']: '+LOADER_NOD.TABLE+'.'+item_id)
                        continue

                    logger.info('Channel: '+item_url)
                    #if delayChannel > 0: time.sleep(delayChannel)                              # задержка между каналами, сек

                    if advanced or (item_id == '') or (item_name == ''):                        # обновить LOADER_NOD

                        if item_invite != '':                                                   # для закрытого канала
                            if not self.tg.setMemberPrivate(item_invite):                       # подписаться на канал
                                logger.warning('Error subscribe on private channel')
                                continue
                            setNodField(HOST.TG, DAEMON_INI.WORKER, LOADER_NOD.URL, item_url, LOADER_NOD.VIP, 1)

                        entity_global = self.tg.getGlobalEntity(item_entity)
                        if entity_global is None:
                            logger.warning('Entity not found')
                            continue

                        item_id_new   = str(entity_global.id)
                        item_name_new = self.tg.getName(entity_global)
                        if item_name_new == '':
                            logger.warning('The name entity(api) is empty')
                            continue

                        if item_id   != item_id_new:   setNodField(HOST.TG, DAEMON_INI.WORKER, LOADER_NOD.URL,      item_url,    LOADER_NOD.GROUP_ID, item_id_new)
                        if item_name != item_name_new: setNodField(HOST.TG, DAEMON_INI.WORKER, LOADER_NOD.GROUP_ID, item_id_new, LOADER_NOD.NAME,     item_name_new)
                        #item_id   = item_id_new
                        #item_name = item_name_new

                    entity_local = self.tg.getLocalEntity(item_entity)                          # для ускорения input_entity
                    if entity_local is None:
                        logger.warning('Local entity not found')
                        continue

                    if advanced and item_invite=='': self.tg.setMember(entity_local, item_vip)  # установить vip-статус участника ПУБЛИЧНОГО канала (для закрытого устанавливается выше)
                    countItem += self.parser.parseChannel(entity_local, tsPeriodStart, advanced)# парсить канал
                    logger.info('Found: '+str(countItem-countItem0))

                # ошибка чтения канала не должна влиять на чтение других каналов
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    logError(e)

            if tsPeriodStart != 0: self.parser.parseArcMarkDel(tsPeriodStart, tsScanStart)      # отметить удаленные записи

            logger.info('OK! '+str(countItem).rjust(3)+' rec. '+str(round(time.time() - timeStart) // 60).rjust(3)+' m.')
            ret = True
        except Exception as e:
            logError(e)
        finally:
            i = timeNext-time.time()                                                            # ожидать оставшееся время
            if i > 0:
                disconnect = (i > 60)
                if disconnect: self.tg.disconnect()                                             # при длительном простое теряется связь
                logger.info('WAIT! '+str(i//60).rjust(3)+' m.')
                time.sleep(i)
                if disconnect: self.tg.connect()

            return ret

################################################################################
start = lambda: LoaderTG()

# для запуска без демона
if __name__ == "__main__": start()
