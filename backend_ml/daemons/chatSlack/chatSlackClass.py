# -*- coding: utf-8 -*-

import time
from   termcolor              import colored

from   daemonIni              import DAEMON_INI
from   fun.funConst           import ML_BOT
from   fun.funSys             import logger, logError, logging
from   fun.funBD              import varGet
from   fun.funText            import textToJSON, findStr
from   fun.funSlack           import Slack

from   mlClientText           import MLClientText



class ChatSlack():
    def __init__(self, worker):
        #logger.setLevel(logging.DEBUG)
        VAR_OWNER = 'chatSlack'
        logger.info('START!')

        try:
            self.var_token            = varGet(VAR_OWNER, DAEMON_INI.WORKER, 'token')
            self.var_id               = varGet(VAR_OWNER, DAEMON_INI.WORKER, 'id')
            self.var_channelAnswer    = varGet(VAR_OWNER, DAEMON_INI.WORKER, 'channelAnswer')
            self.var_channelQuestion  = varGet(VAR_OWNER, DAEMON_INI.WORKER, 'channelQuestion')
            self.var_usersFakeComment = varGet(VAR_OWNER, DAEMON_INI.WORKER, 'usersFakeComment').replace(' ', '').split(',')
            self.isStop               = False
            self.slack                = Slack(self.var_token, self.var_id)

            while not self.isStop:
                connect                  = textToJSON(varGet(VAR_OWNER, DAEMON_INI.WORKER, 'mlServerText'))
                self.host                = connect.get('host',        '')
                self.port                = connect.get('post',        5000)
                try:
                    time.sleep(1)
                    self.step()
                except (KeyboardInterrupt, SystemExit):
                    msg = 'Aborted by user'
                    logger.info(msg)
                    print('\n'+msg)

                    #self.handlerMsg.stop()
                    self.isStop = True
                except Exception as e:
                    #logger.error(str(e))   # здесь бывает ошибка name 'time' is not defined. Ошибку пока не искал
                    logError(e)

        except Exception as e:
            logError(e)
        finally:
            self.stop()
            logger.info('EXIT!')


    def stop(self):
        self.isStop = True
        if hasattr(self, 'mlClient'): self.mlClient.stop()                                                # при ошибке может быть не инициализирован



    ##########################################################
    # ВЫПОЛНИТЬ ШАГ
    ##########################################################
    def step(self):
        for item in self.slack.ioGet():
            channelID  = item[self.slack.KEY_CHANNEL    ]                                           # id канала, с которого пришло сообщение
            userID     = item[self.slack.KEY_USER       ]                                           # id пользователя, отправившего сообщение
            text       = item[self.slack.KEY_TEXT       ]                                           # текст сообщения
            ts         = item[self.slack.KEY_TS         ]                                           # timestamp сообщения
            parentID   = item.get(self.slack.KEY_PARENT_USER, '')                                   # id родительского сообщения
            parentText = item.get(self.slack.KEY_PARENT_TEXT, '')                                   # текст родительского сообщения
            if (not text) or (not channelID) or (parentID==self.var_id): return

            text       = self.cutText(text)
            parentText = self.cutText(parentText)

            ##########################################################
            # ОТВЕТ
            ##########################################################
            if parentID == '':
                # получить ответ
                client = MLClientText(host=self.host, port=self.port)
                try:
                    answer = client.botGetAnswer(text)
                except Exception as e:
                    client = None
                    raise e
                if answer in ('', None): continue

                # ответ в канал-источник как комментарий
                self.slack.ioSend({
                    'text'    : answer,
                    'channel' : channelID,
                    'ts'      : ts,
                })

                # ответ в целевой канал
                if (self.var_channelAnswer != '') and (channelID == self.var_channelQuestion):
                    self.slack.ioSend({
                        'text'    : ':triangular_flag_on_post: *'+text+'*\n:writing_hand: '+answer,
                        'channel' : self.var_channelAnswer,
                    })

                # ответ в консоль
                print('Вопрос: '+text)
                print('Ответ: ' +colored(answer, 'green')+'\n')


            ##########################################################
            # ОБУЧЕНИЕ
            ##########################################################
            elif (parentID != '') and (not userID in self.var_usersFakeComment):
                # записать ответ
                client = MLClientText(host=self.host, port=self.port)
                try:
                    isOk = client.botAddRec(quest=parentText, answer=text, host=ML_BOT.HOST_SLACK, author_id=str(userID))
                except Exception as e:
                    client = None
                    raise e

                # отметка об успешной операции
                self.slack.ioSendReaction(channel=channelID, name=('heavy_check_mark' if isOk else 'x'), ts=ts)                 # thumbsup

                # ответ в консоль
                print('Вопрос: '+parentText)
                print('Ответ: ' +colored(text, 'red')+'\n')


    def cutText(self, text):
        ret = findStr(text, r':triangular_flag_on_post: \*(.+)\*>')
        if ret == '': ret = text
        return ret

