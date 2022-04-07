# -*- coding: utf-8 -*-

##################################################################################################################
# pip3 install slackclient==1.3.0       http://python-slackclient.readthedocs.io/en/latest/
##################################################################################################################
# если появляется ошибка 'NoneType' object has no attribute 'recv'
# pip install -U python-meteor          https://github.com/hharnisc/python-meteor/issues/5
##################################################################################################################
# https://media.readthedocs.org/pdf/python-slackclient/latest/python-slackclient.pdf
##################################################################################################################


import os, io, time
import websocket
from   slackclient  import SlackClient
from   fun.funConst import BOT_TYPE
from   fun.funSys   import tsNow, logging, logger, logError


#####################################################
# ВЗАИМОДЕЙСТВИЕ СО SLACK
#####################################################
# varOwner     - ALAS.VAR.OWNER
#####################################################
# для кнопок нужно создавать Slack App
# https://tutorials.botsfloor.com/slack-app-or-bot-user-integration-842c3843eea8
#####################################################
class Slack():
    KEY_CHANNEL     = 'channel'
    KEY_USER        = 'user'
    KEY_TEXT        = 'text'
    KEY_REACTION    = 'reaction'
    KEY_TS          = 'ts'
    KEY_PARENT_TS   = 'parent_ts'
    KEY_PARENT_TEXT = 'parent_text'
    KEY_PARENT_USER = 'parent_user'

    def __init__(self, varToken, varID):
        self.client = SlackClient(varToken)
        self.varID  = varID

        # auto_reconnect=True
        self.ioConnect()



    #####################################################
    # ИНТЕРФЕЙС: СОЕДИНЕНИЕ
    #####################################################
    def ioConnect(self):
        try:
            ret = self.client.rtm_connect()
            if ret: logger.info ('Connected')
            else:   logger.error('Error connected')
        except Exception as e:
            logError(e)
            ret = False
        return ret



    #####################################################
    # ИНТЕРФЕЙС: ОТПРАВИТЬ ФАЙЛ
    #####################################################
    # channel         - id канала
    # val.text
    # val.file
    # [val.filename]  - отображаемое имя файла
    # title           - заголовок
    # initial_comment - комментарий
    #####################################################
    def ioSendFile(self, val, isWait=False):
        ret = False
        if (val.get('channel', '') == '') or (val.get('text', '') == '') or (val.get('file', '') == ''): return False

        # чтобы избежать "socket is already closed"
        while True:
            try:
                filename = os.path.split(val['file'])                   # ('path', 'nnn.txt')
                with open(val['file'], 'rb') as f:
                    ret_api = self.client.api_call(
                        'files.upload',
                        channels        = val['channel'],
                        title           = val['text'],
                        file            = io.BytesIO(f.read()),
                        filename        = val.get('filename', filename[1]),
                        initial_comment = val.get('initial_comment', ''),
                    )
                ret = ret_api.get('ok', False)
                break
            except websocket.WebSocketConnectionClosedException as e:
                logger.error('Caught websocket disconnect, reconnecting...')
                time.sleep(10)
                self.ioConnect()            # auto_reconnect=True
                if not isWait: break
            except Exception as e:
                logError(e)
                if not isWait: break
        return ret


    #####################################################
    # ИНТЕРФЕЙС: ОТПРАВИТЬ
    #####################################################
    # val.channel     - id канала
    # val.text
    # val.ts          - thread_ts - для реплики на сообщение
    # [val.text2]     - дополнительный текст (text - заголовок)
    # [val.important] - важность [0 ... 3]
    #####################################################
    def ioSend(self, val, isWait=False):
        IMPORTANT_TO_COLOR = {
            '0': '#1E90FF',  # blue
            '1': '#7CFC00',  # green
            '2': '#FFD700',  # yellow
            '3': '#dd2e4e',  # red
        }

        if (val.get('channel', '') == '') or (val.get('text', '') == ''): return
        if val.get('text2', '') != '':
            val['text']        = '*'+val['text']+'*'
            val['attachments'] = [
                {
                    'attachment_type' : 'default',
                    'color'           : BOT_TYPE.IMPORTANT_TO_COLOR.get(val.get('important', '0'), BOT_TYPE.IMPORTANT_TO_COLOR['0'])[0],
                    #'pretext'        : 'pretext',
                    'text'            : val['text2'],
                }
            ]

        if val.get('text2',     None) != None: del val['text2']
        if val.get('important', None) != None: del val['important']

        options = {
            'channel'      : val['channel'],
            'text'         : val['text'],
            'as_user'      : True,
            'unfurl_links' : val.get('unfurl_links', False),                                        # дополнять ссылку контентом
            'unfurl_media' : val.get('unfurl_media', False),
        }
        if not val.get('ts',          None) is None: options['thread_ts'  ] = val['ts']             # str(tsNow())+'.000000'),
        if not val.get('attachments', None) is None: options['attachments'] = val['attachments']
        ret = self.ioAPICall(method='chat.postMessage', options=options, isWait=isWait)
        if not ret.get('ok', True): logger.error(str(ret.get('error', ret))+'\n'+str(val))
        return ret.get('ts', '')

        '''
        'ok': True,
        'channel': 'CJL8MU56G',
        'ts': '1557822127.025400',
        'message': {'type': 'message', 'subtype': 'bot_message', 'text': 'Hello world!', 'ts': '1557822127.025400', 'username': 'bot', 'bot_id': 'B6YU4CCKX'},
        'warning': 'missing_charset',
        'response_metadata': {'warnings': ['missing_charset']}
        '''

    #####################################################
    # ИНТЕРФЕЙС: ОТПРАВИТЬ REACTION
    #####################################################
    def ioSendReaction(self, channel, name, ts, isWait=False):
        ret = self.ioAPICall(method='reactions.add', options={'channel':channel, 'name':name, 'timestamp':ts}, isWait=isWait)
        if not ret.get('ok', True): logger.error(str(ret.get('error', ret))+'\n'+str(val))



    #####################################################
    # ИНТЕРФЕЙС: ПОЛУЧИТЬ
    #####################################################
    # return: [{channel, message, user, ...}, ... ]
    #####################################################
    # MESSAGE
    # 'channel': 'G73A76YH4',
    # 'user': 'U29URMFA9',                       <-- MY
    # 'text': 'главное сообщение',
    # 'type': 'message',
    # 'ts': '1542705930.007700',
    # 'team': 'T29V0TPS6',
    # 'event_ts': '1542705930.007700',
    # 'client_msg_id': 'bf6ef012-9cd8-4265-b776-ec38a1ad614a'
    #####################################################
    # REACTION
    # 'type': 'reaction_added',
    # 'user': 'U29URMFA9',
    # 'item': {'type': 'message', 'channel': 'G73A76YH4', 'ts': '1562909476.217800'},
    # 'reaction': 'exclamation',
    # 'item_user': 'U6YMUGFBM',
    # 'event_ts': '1562914326.220900',
    # 'ts': '1562914326.220900'
    #####################################################
    def ioGet(self, isWait=False):
        ret = []
        val = self.ioAPI(fun=lambda: self.client.rtm_read(), isWait=isWait)
        if len(val) == 0: return ret
        for item in val:
            # message: есть текст, автор - не этот бот, сообщение
            if item \
                and 'text' in item \
                and 'user' in item and self.varID not in item['user'] \
                and 'type' in item and 'message'  in     item['type']:
                rec = {
                    self.KEY_CHANNEL: item['channel'],
                    self.KEY_USER:    item['user'],
                    self.KEY_TEXT:    item['text'].strip(),
                    self.KEY_TS:      item['ts'],
                }

                # добавить родителя реплики (если есть)
                if 'thread_ts' in item:
                    rec_parent = self.ioGetParent(channel=item['channel'], thread_ts=item['thread_ts'], isWait=isWait)
                    if len(rec_parent) > 0: rec.update(rec_parent)
                ret.append(rec)

            # reaction: есть текст, автор - не этот бот, сообщение или реакция
            elif item \
                and 'user' in item and self.varID not in item['user'] \
                and 'item' in item and 'channel' in item['item'] and 'type' in item['item'] and 'message' in item['item']['type'] \
                and 'type' in item and 'reaction_added' in item['type']:
                rec = {
                    self.KEY_CHANNEL: item['item']['channel'],
                    self.KEY_USER:    item['user'],
                    self.KEY_REACTION:item['reaction'],
                    self.KEY_TEXT:    self.ioGetReactionText(channel=item['item']['channel'], user=item['user'], ts=item['item']['ts']),
                    self.KEY_TS:      item['item']['ts'],
                }
                ret.append(rec)
        return ret


    #####################################################
    # ИНТЕРФЕЙС: ПОЛУЧИТЬ ОТМЕЧЕННЫЙ ТЕКСТ
    #####################################################
    # 'ok': True,
    # 'items': [{
    #   'type': 'message',
    #   'channel': 'G73A76YH4',
    #   'message': {
    #       'bot_id': 'B6YU4CCKX',
    #       'type': 'message',
    #       'text': ' ',
    #       'user': 'U6YMUGFBM',
    #       'ts': '1562911669.218700',
    #       'team': 'T29V0TPS6',
    #       'permalink': ' ',
    #       'reactions': [
    #           {'name': 'exclamation', 'users': ['U29URMFA9'], 'count': 1},
    #           {'name': 'question', 'users': ['U29URMFA9'], 'count': 1}]}}, ...
    #####################################################
    def ioGetReactionText(self, channel, user, ts, isWait=False):
        ret = ''
        val = self.ioAPICall(method='reactions.list', options={'channel':channel, 'user':user, 'limit':3}, isWait=isWait)
        for item in val.get('items', []):
            message = item.get('message', {})
            if message.get('ts', '')!=ts: continue
            text = message.get('text', '')
            if text=='': continue
            ret = text
            break
        return ret


    #####################################################
    # ИНТЕРФЕЙС: ПОЛУЧИТЬ РОДИТЕЛЬСКИЙ THREAD
    #####################################################
    # 'ok': True,
    # 'headers': {'X-XSS-Protection': '0', ...
    # 'messages': [
    #     {
    #         'unread_count': 1,
    #         'ts': '1542706919.000300',
    #         'text': 'гл сообщ 1',
    #         'subscribed': False,
    #         'type': 'message',
    #         'reply_count': 1,
    #         'replies': [{'ts': '1542715641.003200', 'user': 'U29URMFA9'}],
    #         'client_msg_id': 'f41cb957-c1d6-4cdd-9fbf-6080b3e35ffb',
    #         'thread_ts': '1542706919.000300',
    #         'user': 'U29URMFA9'
    #     }, {
    #         'ts': '1542715641.003200',
    #         'text': 'rrrr1',
    #         'type': 'message',
    #         'parent_user_id': 'U29URMFA9',
    #         'client_msg_id': '7bcb260b-3269-4d60-9a80-5e6bce61c9c4',
    #         'thread_ts': '1542706919.000300',
    #         'user': 'U29URMFA9'
    #     }
    # ],
    # 'has_more': False
    #####################################################
    def ioGetParent(self, channel, thread_ts, isWait=False):
        ret = {}
        val = self.ioAPICall(method='conversations.replies', options={'channel':channel, 'ts':thread_ts}, isWait=isWait)

        messages = val.get('messages', [])
        if len(messages) == 0: return ret

        ret[self.KEY_PARENT_TS]   = messages[0].get('ts',   '')
        ret[self.KEY_PARENT_TEXT] = messages[0].get('text', '')
        ret[self.KEY_PARENT_USER] = messages[0].get('user', '')
        if (ret[self.KEY_PARENT_TS]  =='') or \
           (ret[self.KEY_PARENT_TEXT]=='') or \
           (ret[self.KEY_PARENT_USER]==''): ret = {}

        return ret




    #####################################################
    # ИНТЕРФЕЙС: УДАЛИТЬ
    #####################################################
    def ioDel(self, channel, ts, isWait=False):
        ret_api = self.ioAPICall(method='chat.delete', options={'channel':channel, 'ts':ts}, isWait=isWait)
        ret = ret_api.get('ok', False)
        if not ret: logger.error(ret_api.get('error', 'err'))
        return ret




    #####################################################
    # ИНТЕРФЕЙС: API
    #####################################################
    ioAPICall = lambda self, method, options, isWait=False: self.ioAPI(fun=lambda: self.client.api_call(method, **options), isWait=isWait)
    def ioAPI(self, fun, isWait=False):
        ret = {}
        # чтобы избежать "socket is already closed"
        while True:
            try:
                ret = fun()
                break
            # except websocket.WebSocketConnectionClosedException as e:
            #     logger.error('Caught websocket disconnect, reconnecting...')
            #     time.sleep(10)
            #     self.ioConnect()                                  # auto_reconnect=True
            #     if not isWait: break
            except Exception as e:
                logger.error(str(e))
                time.sleep(10)
                self.ioConnect()                                    # auto_reconnect=True
                if not isWait: break
        return ret


'''
    # https://api.slack.com/docs/interactive-message-field-guide
    # https://api.slack.com/docs/message-buttons
    # https://api.slack.com/docs/message-attachments
    slack = Slacker(DAEMON_INI.SLACK.TOKEN)
    slack.chat.post_message(
            channel     = '#monitor',
            text        = 'Проверка *запуска* бота',
            as_user     = True,
            icon_emoji  = ':ninja:',
            attachments = [
                {'attachment_type' : 'default',
                 'color'    : '#dd2e4e',
                 'pretext'  : 'pretext',
                 'text'     : 'text',
                 'actions'  : [
                    {
                        'type'  : 'button',
                        'text'  : 'Да',
                        'name'  : 'yes',
                        'value' : 'yes',
                        'style' : 'primary',
                        'confirm' : {
                            'title'        : 'Вы уверены?',
                            'text'         : 'Вы предпочитаете Да?',
                            'ok_text'      : 'Да',
                            'dismiss_text' : 'Нет',
                        },
                    },
                    {
                        'type'  : 'button',
                        'text'  : 'Нет',
                        'name'  : 'no',
                        'value' : 'no',
                        'style' : 'danger',
                        'url'   : 'http://tut.by',
                    },
                 ]
                 }]
    )
'''
