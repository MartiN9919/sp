# -*- coding: utf-8 -*-

import threading, os, time, gc

from   daemonIni              import DAEMON_INI
from   fun.funSys             import logger, logError
from   fun.funConst           import BOT_TYPE, BOT, HOST, MSG
from   fun.funSys             import tsNow
from   fun.funBD              import bdConnect, bdDisconnect, bdSQL, varGet
from   fun.funBDBot           import botTypeGet, botSlackGet, botSlackMark
from   fun.funText            import textToJSON, JSONNormal, replStr

from   mlClientText           import MLClientText


#==============================================================================
#    МЕНЕДЖЕР СООБЩЕНИЙ ИЗ ТАБЛИЦЫ ATLAS.BOT (САМОСТОЯТЕЛЬНЫЙ ПОТОК)
#==============================================================================
#    var_owner      - 'botSlack'
#    slack          - экземпляр класса Slack
#    funValDelay    - функция получения величины задержки между циклами, сек.
#    funViberSend   - функция дублирования сообщений в Viber
#==============================================================================
#    1. для каждой enabled-записи BOT_TYPE
#    2. берет данные из MON (BOT_TYPE.MON_TYPE_ID)
#    3. накладывает на эти данные фильтры (BOT_TYPE.VAL_...)
#    4. результат публикует в канал и помещает в BOT (для исключения повторов)
#==============================================================================
class HandlerMsg():
    def __init__(self, var_owner, slack, funValDelay, funViberSend=None):
        self.thread = MsgAutoThread(var_owner, slack, funValDelay, funViberSend)
        #self.daemon = True
        self.thread.start()

    def stop(self):
        self.thread.stop()
        self.thread.join()


class MsgAutoThread(threading.Thread):
    def __init__(self, var_owner, slack, funValDelay, funViberSend=None):
        threading.Thread.__init__(self)
        self.var_owner      = var_owner
        self.slack          = slack
        self.funValDelay    = funValDelay
        self.funViberSend   = funViberSend
        self.isStop         = False


    def stop(self):
        self.isStop = True


    def run(self):
        time.sleep(5)
        while not self.isStop:
            try:
                countMsg    = 0
                countFile   = 0
                bd          = bdConnect()                                                                   # если сделать это в классе, то виснет

                delayNext   = self.funValDelay()
                timeStart   = time.time()                                                                   # время начала текущего цикла
                timeNext    = timeStart+delayNext                                                           # время начала следующего цикла
                tsStart     = tsNow()

                connect     = textToJSON(varGet(self.var_owner, DAEMON_INI.WORKER, 'mlServerText'))         # параметры взаимодействия с сервером mlServerText
                host        = connect.get('host',        '')
                port        = connect.get('post',        5000)
                sim_min     = connect.get('sim_min',     0.18)                                              # если 0.0 - группировка отключена
                sim_correct = connect.get('sim_correct', True)
                tsOld       = tsStart-60*60*connect.get('period', 12)                                       # группировка новостей за period часов

                # ТЕСТ
                # ts = self.slack.ioSend({
                #     'channel' : 'G46U0JJJ0',
                #     'text'    : 'Тест!!!!!!!!!!!!!!',
                #     'text2'   : '',
                #     'ts'      : "1558083473.146500",
                #     #'important': str(rec[self.IND_IMPORTANT]),
                #     'unfurl_links' : False,
                #     'unfurl_media' : False,
                # })
                # print('!')
                # raise

                # logger.debug('GO! delayNext='+str(delayNext)+' '+str(connect))

                # очистить список используемых slack-каналов
                self.channelList = []

                # список BOT_TYPE
                for rec_bot_type in botTypeGet(DAEMON_INI.WORKER, [BOT_TYPE.ID, BOT_TYPE.CHANNEL_SLACK], bd):
                    channels = list(map(lambda x: x.strip(), rec_bot_type[1].split(',')))                   # список каналов для BOT_TYPE
                    if len(channels) == 0: continue

                    # список необработанных BOT для BOT_TYPE[rec_bot_type] (show_slack=0)
                    for rec_bot in botSlackGet(rec_bot_type[0], [BOT.ID, BOT.HOST, BOT.MSG_VAL, BOT.MSG_NAM, BOT.URL, BOT.DATE, BOT.SLACK_TS], bd):
                        rec_bot_id       = rec_bot[0]
                        rec_bot_host     = rec_bot[1]
                        rec_bot_msg_val  = rec_bot[2]
                        rec_bot_msg_nam  = rec_bot[3]
                        rec_bot_url      = rec_bot[4]
                        rec_bot_slack_ts = self.fieldTsToDict(rec_bot[6])

                        ###########################################################
                        # обработка отчетов
                        ###########################################################
                        if rec_bot_host == HOST.REPORT:
                            for channel in channels:
                                file = DAEMON_INI.PATH_PROJECT[:-1]+rec_bot_url                             # [-1] - обрезать в пути последний /
                                filename, fileext = os.path.splitext(file)
                                filename = 'report'+fileext
                                if self.slack.ioSendFile({
                                    'channel'  : channel,
                                    'text'     : rec_bot_msg_nam,                                           # .replace(BOT.MSG_BOLD_START, '').replace(BOT.MSG_BOLD_END, ''),
                                    'file'     : file,
                                    'filename' : filename,
                                }):
                                    botSlackMark(bot_id=rec_bot_id, bot_ts='', bd=bd)                       # установить признак: отработано
                                    countFile += 1
                            continue


                        ###########################################################
                        # обработка сообщений
                        ###########################################################
                        # data_new - новые данные
                        # удалить в msg_nam [BOLD][/BOLD][title]...
                        data_new = [replStr(rec_bot_msg_nam, '', r'(\[[\w\/]+\])').strip()]
                        crc_new  = data_new[0]+rec_bot_host

                        # заменить условные обозначения
                        if rec_bot_host != '':
                            rec_bot_host = ('['+rec_bot_host+'] ') \
                                .replace('[talks.by]',     ':talks:') \
                                .replace('[onliner.by]',   ':onliner:') \
                                .replace('[vk.com]',       ':vk:') \
                                .replace('[t.me]',         ':tg:') \
                                .replace('[telegram.org]', ':tg:') \
                                .replace('[twitter.com]',  ':tw:') \
                                .replace('[facebook.com]', ':fb:') \
                                .replace('[viber.com]',    ':vb:')

                        rec_bot_msg_val = (rec_bot_host + ' ' + rec_bot_msg_val).strip()
                        if rec_bot_url != '': rec_bot_msg_nam = '<'+rec_bot_url+'|'+rec_bot_msg_nam+'>'

                        text = rec_bot_msg_val+': '+rec_bot_msg_nam                                         # обязательно пробелы по обе стороны '>'
                        for item in DAEMON_INI.ICO_LIST: text = text.replace(item, DAEMON_INI.ICO_LIST[item][0])
                        text = text.replace(BOT.MSG_BOLD_START, '*').replace(BOT.MSG_BOLD_END, '*')

                        # обработать каждый канал
                        for channel in channels:
                            #if channel!='G46U0JJJ0': continue   # D6Y4XSPDE

                            ##########################################################
                            # определить родительский узел ts_parent
                            ##########################################################
                            ts_parent = None
                            if sim_min>0.0:
                                # список активных BOT_TYPE.ID каналов, в которых есть channel: ids = '1,...'
                                sql = \
                                    "SELECT "+ BOT_TYPE.ID+" "+ \
                                    "FROM "  + BOT_TYPE.TABLE+" "+ \
                                    "WHERE " + BOT_TYPE.ENABLED+"=1 AND ("+BOT_TYPE.CHANNEL_SLACK+" LIKE '%"+channel+"%');"
                                val = bdSQL(sql=sql, wait=False, read=True, db=bd)
                                ids = list(map(lambda item: str(item[0]), val))
                                ids = ",".join(ids)

                                # data_old - старые данные
                                # исключить наличие символа _ в msg_nam (для telegram)
                                # исключить MSG.NO_TEXT в msg_nam
                                # исключить ссылку на data_new
                                #
                                # удалить в msg_nam [BOLD][/BOLD][title]...
                                # исключить одинаковые (host, msg_nam) с разных каналов, оставить более раннюю опубликованную запись
                                # если одинаковые (host, msg_nam) old и new - пропустить
                                sql = \
                                    "SELECT "+ BOT.ID+", "+BOT.MSG_NAM+", "+BOT.SLACK_TS+", "+BOT.HOST+" "+ \
                                    "FROM "  + BOT.TABLE+" "+ \
                                    "WHERE " + \
                                        BOT.DATE+">="+str(tsOld)+" AND "+ \
                                        BOT.BOT_TYPE_ID+" IN ("+ids+") AND "+ \
                                        BOT.ID+"<>"+str(rec_bot_id)+" AND "+ \
                                        BOT.MSG_NAM+" NOT LIKE '%\\_%' AND "+ \
                                        BOT.MSG_NAM+" NOT LIKE '%"+MSG.NO_TEXT+"%' "+ \
                                    "ORDER BY "+BOT.REFRESH+" ASC;"
                                data_old_orig = bdSQL(sql=sql, wait=False, read=True, db=bd)
                                data_old_orig = list(map(lambda item: [item[0], replStr(item[1], '', r'(\[[\w\/]+\])').strip(), item[2], item[3]], data_old_orig))
                                data_old      = []
                                isContinue    = False
                                for item in data_old_orig:
                                    crc_old = item[1]+item[3]
                                    if crc_old==crc_new:
                                        isContinue = True
                                        break
                                    if not crc_old in [x[1]+x[3] for x in data_old]:
                                        data_old.append(item)
                                if isContinue: continue
                                data_old = list(map(lambda item: [item[0], item[1]], data_old))

                                # определить родительский узел
                                if len(data_old)>0:
                                    client = MLClientText(host=host, port=port)
                                    try:
                                        data_sim  = client.tfidfSim(docs1=data_old, docs2=data_new, isCorrect=False)    # data_sim   = [[docs1.id, sim], ...]   len = len(docs2)
                                    except Exception as e:
                                        client = None
                                        raise e

                                    if data_sim is None: raise ValueError('Server not respond')                     # Exception('Server not respond')
                                    if data_sim[0][1] >= sim_min:
                                        field     = list(filter(lambda rec: rec[0]==data_sim[0][0], data_old_orig))[0][2]
                                        ts_parent = self.fieldTsToTs(field=field, channel=channel)

                            ts = self.slack.ioSend({
                                'channel' : channel,
                                'text'    : text,
                                'text2'   : '',
                                'ts'      : ts_parent,                                          # если ts_parent не верный то публикации НЕ БУДЕТ
                                #'important': str(rec[self.IND_IMPORTANT]),
                                'unfurl_links' : False,
                                'unfurl_media' : False,
                            })
                            rec_bot_slack_ts[channel] = ts if ts_parent==None else ts_parent    # если запись вложена, то взать ts основной записи
                            if self.funViberSend: self.funViberSend(
                                message        = text,
                                channelID      = channel,
                                userID         = 'bot',
                                reactionID     = None,
                                viberForward   = 'auto',
                                firstMsg       = ts_parent==None,
                            )

                        # установить признак: отработано
                        botSlackMark(bot_id=rec_bot_id, bot_ts=rec_bot_slack_ts, bd=bd)

                        countMsg += 1

            except (KeyboardInterrupt, SystemExit):
                self.isStop = True

            except Exception as e:
                logError(e)

            finally:
                bdDisconnect(bd)
                gc.collect()
                if 'timeNext' in locals():
                    if (countMsg+countFile) > 0: logger.info('OK! '+((str(countMsg).rjust(3)+' msg. ') if countMsg>0 else '')+((str(countFile).rjust(3)+' file') if countFile>0 else '')+str(round(time.time() - timeStart)).rjust(3)+' s.')
                    i = timeNext-time.time()
                    if (i > 0) and (not self.isStop): time.sleep(i)


    def fieldTsToDict(self, field):
        ret = JSONNormal(field) if not field in (None, '') else {}
        return ret

    def fieldTsToTs(self, field, channel):
        val = self.fieldTsToDict(field)
        return val.get(channel, None)

