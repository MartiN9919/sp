# -*- coding: utf-8 -*-

import time
import json
import html

from   daemonIni            import DAEMON_INI
from   fun.funSys           import logger, setLogger, logging, logError
from   fun.funBD            import varGet
from   fun.funText          import urlsGet, findStr
from   fun.funSlack         import Slack
from   fun.funViber         import Viber
from   handlers.handlerHelp import handlerHelp
from   handlers.handlerMsg  import HandlerMsg
from   handlers.handlerSys  import handlerSysLog, \
                                   handlerSysExecStart, handlerSysExecStop, handlerSysExecRestart, handlerSysExecVerify
from   handlers.handlerMon  import handlerMonAdd, handlerMonDel
from   handlers.handlerRep  import handlerRepCreate



#==============================================================================
#    КЛАСС-МЕНЕДЖЕР BOT SLACK
#==============================================================================
class BotSlack():
    def __init__(self):
        #logger.setLevel(logging.DEBUG)
        logger.info('START!')

        try:
            self.var_owner  = 'botSlack'
            self.var_token  = varGet(self.var_owner, DAEMON_INI.WORKER, 'token')
            self.var_id     = varGet(self.var_owner, DAEMON_INI.WORKER, 'id')
            self.isStop     = False
            self.slack      = Slack(varToken=self.var_token, varID=self.var_id)
            self.var_viber  = json.loads(varGet(self.var_owner, DAEMON_INI.WORKER, 'viber'), strict=False)

            for item in self.var_viber:
                item['obj'] = Viber(urlServer=item['viberURL'], logID=item.get('viberID', ''))
            self.handlerMsg = HandlerMsg(var_owner=self.var_owner, slack=self.slack, funValDelay=self.valDelay, funViberSend=self.funViberSend)
            while not self.isStop:
                try:
                    time.sleep(1)
                    self.step()
                except (KeyboardInterrupt, SystemExit):
                    msg = 'Aborted by user'
                    logger.info(msg)
                    print('\n'+msg)

                    self.handlerMsg.stop()
                    self.isStop = True
                except Exception as e:
                    #logger.error(str(e))   # здесь бывает ошибка name 'time' is not defined. Ошибку пока не искал
                    logError(e)

        except Exception as e:
            logError(e)
        finally:
            try:
                for item in self.var_viber:
                    item['obj'].free()
                    item['obj'] = None
            except:
                pass
            logger.info('EXIT!')



    def stop(self):
        self.isStop = True



    #===========================================================================================
    # ВЫПОЛНИТЬ ШАГ
    #===========================================================================================
    def step(self):
        CMD_IND_ISADMIN   = 0                                                                   # предназначена ли команда только для администратора
        CMD_IND_ISMANAGER = 1                                                                   # предназначена ли команда только для менеджера
        CMD_IND_FUN       = 2                                                                   # функция обработки команды
        CMD_LIST  = {
            '?'         : [False, False, handlerHelp],
            'info'      : [False, False, None],
            'инфо'      : [False, False, None],
            'log'       : [True,  False, handlerSysLog],
            'лог'       : [True,  False, handlerSysLog],
            'kju'       : [True,  False, handlerSysLog],
            'дщп'       : [True,  False, handlerSysLog],
            'start'     : [True,  False, handlerSysExecStart],
            'stop'      : [True,  False, handlerSysExecStop],
            'restart'   : [True,  False, handlerSysExecRestart],
            'verify'    : [True,  False, handlerSysExecVerify],
            'контроль'  : [True,  True,  handlerMonAdd],
            'control'   : [True,  True,  handlerMonAdd],
            'контроль+' : [True,  True,  handlerMonAdd],
            'control+'  : [True,  True,  handlerMonAdd],
            'контроль-' : [True,  True,  handlerMonDel],
            'control-'  : [True,  True,  handlerMonDel],
            'report'    : [True,  True,  handlerRepCreate],
            'отчет'     : [True,  True,  handlerRepCreate],
        }

        for itemSlack in self.slack.ioGet():                                                        # message OR reaction
            channelID  = itemSlack[self.slack.KEY_CHANNEL    ]                                      # id канала, с которого пришло сообщение
            userID     = itemSlack[self.slack.KEY_USER       ]                                      # id пользователя, отправившего сообщение
            reactionID = itemSlack.get(self.slack.KEY_REACTION, None)                               # смайлик
            message    = itemSlack.get(self.slack.KEY_TEXT,     None)                               # текст сообщения

            # viber: reaction
            if reactionID:
                self.funViberSend(
                    message        = message,
                    channelID      = channelID,
                    userID         = userID,
                    reactionID     = reactionID,
                    viberForward   = 'reaction')
                return

            # message
            if not message or not channelID: return
            logger.info(channelID+'.'+userID+': '+message)
            args      = message.split()                                                             # args = [arg1, arg2, ... , argN ], где arg1 - команда
            cmd       = CMD_LIST.get(args[0].lower(), [False, False, lambda channelID, args: {}])   # поиск [isAdmin, fun]
            isAdmin   = self.__isAdmin__(userID)                                                    # наличие прав админа
            isManager = self.__isManager__(userID)                                                  # наличие прав менеджера
            isOk      = ((not cmd[CMD_IND_ISADMIN  ]) or (cmd[CMD_IND_ISADMIN  ] and isAdmin  )) or \
                        ((not cmd[CMD_IND_ISMANAGER]) or (cmd[CMD_IND_ISMANAGER] and isManager))    # наличие права выполнить команду

            if isOk:                                                                                # право выполнить команду ЕСТЬ
                if args[0].lower() in ['info', 'инфо']: val = {'text': 'Пользователь: '+userID+(' (администратор)' if isAdmin else '')+(' (менеджер)' if isManager else '')}
                else:                                   val = cmd[CMD_IND_FUN](channelID, args[1:])
            else:                                                                                   # права выполнить команду НЕТ
                val = \
                    {'text': DAEMON_INI.ICO_ERROR+' Команду может выполнить только' + \
                       (' администратор' if not isAdmin   else '') + \
                       (' менеджер'      if not isManager else '') \
                    }

            if val.get('text', '') != '':                                                           # val в канал
                val['channel'] = channelID                                                          # 'D6Y4XSPDE'
                self.slack.ioSend(val)


            # viber: auto
            self.funViberSend(
                message        = message,
                channelID      = channelID,
                userID         = userID,
                reactionID     = None,
                viberForward   = 'auto',
                quote          = True,
            )


    def funViberSend(self, message, channelID, userID, reactionID=None, viberForward='auto', firstMsg=False, quote=False):
        debug = False
        if not message: return
        message = message.strip()
        if message=='': return
        message = html.unescape(message).strip()                                                    # &amp; --> &  и прочее
        message = message.replace('charter97.org', 'charter97.link')
        message = message.replace('https://nn.by', 'http://nn.by')
        urls    = urlsGet(message)
        url     = max(urls, key=lambda x: len(x)) if len(urls)>0 else ''

        if quote:                                                                                   # цитата
            message = 'QUOTE: '+message
            for item_url in urls:
                message = message.replace('<'+item_url+'>', item_url)
        else:                                                                                       # не цитата - только ссылка
            if url=='': return
            message = url

        for var_viber_item in self.var_viber:
            if (not firstMsg) and var_viber_item.get('firstOnly', False): continue                  # фильтр по первой новости

            if var_viber_item.get('forward', '')!=viberForward: continue                            # фильтр по forward
            if debug: print('\n', message)

            item_reactions = var_viber_item.get('slackReaction', [])                                # фильтр по reactions
            if debug: print(1, reactionID, item_reactions)
            if (len(item_reactions)>0) and (not(reactionID in item_reactions)): continue

            item_channels = var_viber_item.get('slackChannels', [])                                 # фильтр по channels
            if debug: print(2, channelID, item_channels)
            if (len(item_channels)>0) and (not(channelID in item_channels)): continue

            item_users = var_viber_item.get('slackUsers', [])                                       # фильтр по users
            if debug: print(3, userID, item_users)
            if (len(item_users)>0) and (not(userID in item_users)): continue

            if debug: print('SLACK->VIBER: '+channelID+'.'+userID+'> '+message)
            logger.debug('SLACK->VIBER: '+str(channelID)+'.'+str(userID)+'> '+message)
            var_viber_item['obj'].set_msg(msg=message)



    #===========================================================================================
    # ПРОВЕРКА НА НАЛИЧИЕ ПРАВ АДМИНИСТРАТОРА
    #===========================================================================================
    def __isAdmin__(self, userID):
        ret = False
        for item in self.valAdmins().replace(' ', '').split(','):
            if item == userID:
                ret = True
                break
        return ret


    #===========================================================================================
    # ПРОВЕРКА НА НАЛИЧИЕ ПРАВ МЕНЕДЖЕРА
    #===========================================================================================
    def __isManager__(self, userID):
        ret = False
        for item in self.valManagers().replace(' ', '').split(','):
            if item == userID:
                ret = True
                break
        return ret


    #===========================================================================================
    # читать переменные из atlas.var
    #===========================================================================================
    def valAdmins(self):   return str(varGet(self.var_owner, DAEMON_INI.WORKER, 'admins',    ''))
    def valManagers(self): return str(varGet(self.var_owner, DAEMON_INI.WORKER, 'managers',  ''))
    def valDelay(self):    return int(varGet(self.var_owner, DAEMON_INI.WORKER, 'delayNext', '60'))
