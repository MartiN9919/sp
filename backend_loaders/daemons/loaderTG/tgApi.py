# -*- coding: utf-8 -*-

# pip3 install PySocks     https://github.com/Anorov/PySocks#installation
# ver 1.6.8
# pip3 install telethon или pip3 install --upgrade telethon
# ver 0.19.1.6
# pip3 install cryptg           # для быстрых операций с файлами
# cryptg ver 0.1.0.7
# rsa ver 3.4.2
# pyaes ver 1.6.1
# pyasn1 ver 0.4.2
# for python 3.4: pip3 install typing
# https://github.com/zalando-stups/senza/issues/287
#
# https://github.com/LonamiWebs/Telethon/blob/master/telethon/telegram_client.py
# https://github.com/LonamiWebs/Telethon/blob/master/telethon/utils.py

# import telethon.version
# print(telethon.version.__version__)


# !!!!!!!! УСТАНОВКА НА СЕРВЕРЕ
# запустить с терминала, получить код, ввести код, записать код в БД
# перенести файл username.session в корневой каталог
# запустить в режиме демона


import os, time, random #, socks

from   telethon                       import TelegramClient, sync, utils
from   telethon.tl.functions.channels import GetParticipantsRequest, JoinChannelRequest, LeaveChannelRequest
from   telethon.tl.functions.users    import GetFullUserRequest
from   telethon.tl.functions.contacts import ImportContactsRequest
from   telethon.tl.custom.dialog      import Dialog
from   telethon.tl.functions.messages import ImportChatInviteRequest
from   telethon.tl.types              import (
    Channel, ChannelParticipantsSearch, PeerChannel, InputPeerChannel,
    User, PeerUser, UserProfilePhoto, UserStatusOffline, UserStatusOnline, InputUser, InputPeerUser,
    ChatPhoto, Document, Photo,
    Message, MessageMediaDocument, MessageMediaPhoto,
    #FileLocation,
    InputPhoneContact
)
from   daemonIni         import DAEMON_INI
from   lib.funConst      import HOST_SHORT
from   lib.funSys        import logger, logError, sqlDateTime, datetimeNow, datetimeCutSecond
from   lib.funBD         import varGetRandom
from   lib.funText       import textToJSON, textNormal
from   lib.funFile       import filePathShort, iconFile



#####################################################
# ПОДКЛЮЧЕНИЕ ЧЕРЕЗ СЛУЧАЙНЫЙ АККАУНТ
#####################################################
# owner  - 'loaderTG'
#####################################################
def TGRandom(owner='loaderTG', worker='', varName='connect'):
    s = varGetRandom(owner, worker, varName, valEmpty=None)
    if s == None: return None
    param = textToJSON(s)
    return TG(param)


#####################################################
# РАБОТА С ТЕЛЕГРАМ
#####################################################
# !!! for telethon 0.19.1.6 !!!
#####################################################
# param:
#    username = 'username'
#    api_id   = 114386
#    api_hash = '2e91b30aafd0db3d51e7db558259ac08'
#    phone    = '+375259529767'
#    code     = 58486
#    host     = '192.168.30.100'    ## не обязательно
#    port     = 3128                ## не обязательно
#####################################################
class TG_BD:
    TABLE      = 'entities'
    ID         = 'id'
    HASH       = 'hash'
    USERNAME   = 'username'
    PHONE      = 'phone'
    NAME       = 'name'

class TG():
    recMaxCount  = 50                       # сколько читать с канала сообщений, 100
    delayRequest = 2                        # максимальная задержка между запросами, сек
    fileIcon     = iconFile(HOST_SHORT.TG)  # файл иконки

    #####################################################
    # КОНСТРУКТОР
    #####################################################
    def __init__(self, param):
        self.client = TelegramClient(
            DAEMON_INI.PATH_DAEMON+param.get('username', 'username'),
            api_id   = param['api_id'],
            api_hash = param['api_hash'],
            proxy    = ((socks.HTTP, param['host'], param['port']) if (param.get('host', '') != '') and (param.get('port', '') != '') else None) # socks.SOCKS5 блокируется шлюзом
            # update_workers=1, timeout=timedelta(seconds=30)
        )
        logger.info('connect for api_id: '+str(param['api_id']))
        self.client.connect()
        if not self.client.is_user_authorized():
            logger.info('authorize for phone: '+param['phone'])
            try:
                self.client.send_code_request(param['phone'])
                param['code'] = input('Enter code ['+param['phone']+'] (and change BD): ')
                self.client.sign_in(param['phone'], param['code'])
                print('Change [BD.var/loaderTG/connect/code] and restart app')
            except BaseException as e:
                logger.error(str(e))
            finally:
                raise


    #####################################################
    # ПСЕВДО-ДЕСТРУКТОР
    #####################################################
    def free(self):
        pass
        #self.disconnect() # отключил, так как выдает ошибку



    #####################################################
    # СОЕДИНЕНИЕ
    #####################################################
    def reconnect(self, wait=True):
        self.disconnect()
        self.sleep()
        self.connect(wait=wait)

    def connect(self, wait=True):
        logger.debug('connect')
        iErr = 0
        while True:
            try:
                self.client.connect()
                isOk = True
            except BaseException as e:
                isOk = not wait
                if (iErr < 10) and wait:
                    iErr += 1                                           # ошибка + 1
                else:
                    logger.warning(str(e)+"\n"+sql[:200])               # вывести сообщение если 10 и более ошибок
                    iErr = 0                                            # обнулить счетчик ошибок
            if isOk: break
            time.sleep(5.0)

    def disconnect(self):
        if 'disconnect' in dir(self.client):
            logger.debug('disconnect')
            try:
                self.client.disconnect()
            except BaseException as e:
                logger.error(str(e))




    #####################################################
    # LOCAL: ЧИТАТЬ TG_BD
    #####################################################
    def getLocaFromID(self, entity_id):
        try:    ret = self.client.session._execute("SELECT "+TG_BD.HASH+", "+TG_BD.USERNAME+", "+TG_BD.NAME+" FROM "+TG_BD.TABLE+" WHERE id="+str(entity_id))
        except: ret = (None, None, None)
        return {
            TG_BD.ID:       self.corrLocalID      (entity_id),
            TG_BD.HASH:     self.corrLocalHash    (ret[0]),
            TG_BD.USERNAME: self.corrLocalUserName(ret[1]),
            TG_BD.NAME:     self.corrLocalName    (ret[2]),
        }

    def getLocalFromUserName(self, entity_username):
        try:    ret = self.client.session._execute("SELECT "+TG_BD.ID+", "+TG_BD.HASH+", "+TG_BD.NAME+" FROM "+TG_BD.TABLE+" WHERE "+TG_BD.USERNAME+"='"+str(entity_username)+"'")
        except: ret = (None, None, None)
        return {
            TG_BD.ID:       self.corrLocalID      (ret[0]),
            TG_BD.HASH:     self.corrLocalHash    (ret[1]),
            TG_BD.USERNAME: self.corrLocalUserName(entity_username),
            TG_BD.NAME:     self.corrLocalName    (ret[2]),
        }




    #####################################################
    # LOCAL: КОРРЕКТИРОВКА ПОЛЯ TG_BD.NAME
    #####################################################
    corrLocalID       = lambda self, val:  0 if val is None else val
    corrLocalHash     = lambda self, val:  0 if val is None else val
    corrLocalUserName = lambda self, val: '' if val is None else val
    corrLocalName     = lambda self, val: '' if val is None else textNormal(val)




    #####################################################
    # ЧИТАТЬ ПОЛЬЗОВАТЕЛЯ ПО ЕГО НОМЕРУ ТЕЛЕФОНА
    #####################################################
    # phone = '+xxxxxxxxxx'
    #####################################################
    def getUserFormPhone(self, phone):
        contact = InputPhoneContact(client_id = 0, phone = phone, first_name='custom_first_name', last_name='custom_last_name')
        try:     val  = self.client(ImportContactsRequest(contacts=[contact])).users
        finally: self.sleep()
        return val[0] if len(val)>0 else None



    #####################################################
    # ЧИТАТЬ КАНАЛ / ПОЛЬЗОВАТЕЛЯ ПО ЕГО ID (!!! если раньше не парсился - не сработает !!!)
    #####################################################
    #def getChannel(self, id): return self.getGlobalEntity(PeerChannel(int(id)))
    #def getUser   (self, id): return self.getGlobalEntity(PeerUser   (int(id)))




    #####################################################
    # ЧИТАТЬ ОБЪЕКТ ИЗ API
    #####################################################
    # entity - id | 'name' | 't.me/name' | 'https://telegram.org/name' | '+34xxxxxxxxx' | 'telegram.me/joinchat/AAAAAEkk2WdoDrB4-Q8-gg'
    # return - Channel, User
    #####################################################
    def getGlobalEntity(self, entity):
        try:     obj = self.client.get_entity(entity)
        except:  obj = None
        finally:
            for _ in range(3, 8): self.sleep()                                      # увеличенная задержка из-за бана
        return   obj

    #####################################################
    # entity - id | 'name' | 't.me/name' | 'https://telegram.org/name'
    # return - InputPeerChannel, InputPeerUser
    #####################################################
    def getLocalEntity(self, entity):
        try:    obj = self.client.get_input_entity(entity)
        except: obj = None
        return  obj





    #####################################################
    # ID ПОЛЬЗОВАТЕЛЯ / КАНАЛА (НЕИЗМЕННО)
    #####################################################
    def getGlobalID(self, entity):
        ret = 0

        id_local = self.getLocalID(entity)
        if id_local!=0:
            try: ret = utils.resolve_id(id_local)[0]
            except: pass

        if isinstance(entity, (str, int)) and (ret==0):
            logger.warning('Not optimization work for: ['+str(entity)+']')
            entity_global = self.getGlobalEntity(entity)
            if not(entity_global is None): entity = entity_global
        if isinstance(entity, (User, Channel)) and (ret==0):
            ret = entity.id

        return ret


    def getLocalID(self, entity):
        ret = 0

        if isinstance(entity, str):
            try:    ret = self.client.session._execute("SELECT "+TG_BD.ID+" FROM "+TG_BD.TABLE+" WHERE "+TG_BD.USERNAME+"='"+entity+"'")[0]
            except: pass
        if isinstance(entity, (str, int)) and (ret==0):
            entity_local = self.getLocalEntity(entity)                                   # на всякий случай также пытаемся найти стандартными средствами
            if not(entity_local is None): entity = entity_local
        if isinstance(entity, (InputPeerUser, InputPeerChannel)) and (ret==0):
            try:    ret = utils.get_peer_id(entity)
            except: pass
        if isinstance(entity, int) and (ret==0):
            ret = entity

        return self.corrLocalID(ret)




    #####################################################
    # USERNAME ПОЛЬЗОВАТЕЛЯ / КАНАЛА (МОЖЕТ МЕНЯТЬСЯ)
    #####################################################
    def getUsername(self, entity):
        ret = ''

        if isinstance(entity, (InputPeerUser, InputPeerChannel)):
            try:
                id_local = utils.get_peer_id(entity)
                ret = self.client.session._execute("SELECT "+TG_BD.USERNAME+" FROM "+TG_BD.TABLE+" WHERE "+TG_BD.ID+"="+str(id_local))[0]
                if ret is None: ret = ''
            except: pass
        if isinstance(entity, int) and (ret==''):
            try:
                ret = self.client.session._execute("SELECT "+TG_BD.USERNAME+" FROM "+TG_BD.TABLE+" WHERE "+TG_BD.ID+"="+str(entity))[0]
                if ret is None: ret = ''
            except: pass
        if isinstance(entity, (str, int)) and (ret==''):
            entity_global = self.getGlobalID(entity)
            if not(entity_global is None): entity = entity_global
        if isinstance(entity, (User, Channel)) and (ret==''):
            try: ret = entity.username
            except: pass
        if isinstance(entity, InputPeerChannel) and (ret==''):              # предполагаем, что канал private (no username for public не тестировалось)
            ret = 'c/'+str(entity.channel_id)

        return self.corrLocalUserName(ret)





    #####################################################
    # ОТОБРАЖАЕМОЕ ИМЯ ПОЛЬЗОВАТЕЛЯ / КАНАЛА (МОЖЕТ МЕНЯТЬСЯ)
    #####################################################
    def getName(self, entity):
        ret = self.getLocalName(entity)
        if ret == '': ret = self.getGlobalName(entity)
        return ret


    def getGlobalName(self, entity):
        ret = ''

        if isinstance(entity, (str, int)):
            logger.warning('Not optimization work for: ['+str(entity)+']')
            entity_global = self.getGlobalEntity(entity)
            if not(entity_global is None): entity = entity_global
        if isinstance(entity, (User, Channel)):
            try:    ret = utils.get_display_name(entity)
            except: pass

        return  textNormal(ret)


    def getLocalName(self, entity):
        ret = ''

        if isinstance(entity, str):
            try:    ret = self.client.session._execute("SELECT "+TG_BD.NAME+" FROM "+TG_BD.TABLE+" WHERE "+TG_BD.USERNAME+"='"+entity+"'")[0]
            except: pass
        if isinstance(entity, int) and (ret==''):
            try:    ret = self.client.session._execute("SELECT "+TG_BD.NAME+" FROM "+TG_BD.TABLE+" WHERE "+TG_BD.ID+"="+str(entity ))[0]
            except: pass
        if isinstance(entity, (str, int)) and (ret==''):
            entity_local = self.getLocalEntity(entity)                                        # на всякий случай также пытаемся найти стандартными средствами
            if not(entity_local is None): entity = entity_local
        if isinstance(entity, (InputPeerUser, InputPeerChannel)) and (ret==''):
            try:
                id_local = utils.get_peer_id(entity)
                ret = self.client.session._execute("SELECT "+TG_BD.NAME+" FROM "+TG_BD.TABLE+" WHERE "+TG_BD.ID+"="+str(id_local))[0]
            except: pass

        return self.corrLocalName(ret)




    #####################################################
    # ЧИТАТЬ УЧАСТНИКОВ КАНАЛА
    #####################################################
    # entity_all - username, Channel, InputPeerChannel
    # return     - [User, User, ...]; если показ заблокирован или ошибка - вернет []
    #####################################################
    def getMembers(self, entity_all):
        try:
            ret = self.client.get_participants(entity_all, None, aggressive=True)
        except Exception as e:
            ret = []
            logger.debug('No read members: '+str(entity_all))                                                        # logError(e) - так хуже
        finally: self.sleep()
        return ret


    #####################################################
    # УСТАНОВИТЬ ЧЛЕНСТВО В ПУБЛИЧНОМ КАНАЛЕ
    #####################################################
    # entity_all - username, Channel, InputPeerChannel
    # LeaveChannelRequest выдает ошибку если уже не член
    #####################################################
    def setMember(self, entity_all, isMember=True):
        try:
            if isMember != self.isMember(channelID=self.getGlobalID(entity_all)):
                if isMember: self.client(JoinChannelRequest (entity_all))
                else:        self.client(LeaveChannelRequest(entity_all))
                logger.info('Join channel' if isMember else 'Leave channel')
            ret = True
        except Exception as e:
            ret = False
            logError(e)
        finally: self.sleep()
        return ret


    #####################################################
    # УСТАНОВИТЬ ЧЛЕНСТВО В ПРИВАТНОМ КАНАЛЕ
    #####################################################
    # https://t.me/joinchat/key_invite
    #####################################################
    def setMemberPrivate(self, key_invite):
        try:
            self.client(ImportChatInviteRequest(key_invite))
            ret = True
        except Exception as e:
            ret = False
            logError(e)
        finally: self.sleep()
        return ret



    #####################################################
    # ПРОВЕРИТЬ ЧЛЕНСТВО В КАНАЛЕ
    #####################################################
    # задавать или channelID или username
    # GetDialogsRequest ?
    #####################################################
    def isMember(self, channelID=None, username=None):
        try:
            ret = False
            for itemDialog in self.client.get_dialogs():
                if not isinstance(itemDialog, Dialog): continue
                if not isinstance(itemDialog.entity, Channel): continue
                if ((itemDialog.entity.id == channelID) and (channelID != None)) or ((itemDialog.entity.username == username) and (username != None)):
                    ret = True
                    break
        except Exception as e:
            ret = None
            logError(e)
        finally: self.sleep()
        return ret



    #####################################################
    # ЧИТАТЬ СООБЩЕНИЯ КАНАЛА ( ПОЛЬЗОВАТЕЛЯ? )
    #####################################################
    def getMessages(self, entity):
        # deprecated try:     messages = self.client.get_message_history(entity, limit=self.recMaxCount)
        try:     messages = self.client.get_messages(entity, limit=self.recMaxCount)                                # читать по recMaxCount сообщений с канала
        finally: self.sleep()
        return messages



    #####################################################
    # ЗАГРУЗИТЬ ФОТО ПОЛЬЗОВАТЕЛЯ
    #####################################################
    # api_obj = User(...) | Channel(...)
    # return  - FileBig, FileSmall (tg/xx/xx/xxxxxx.jpg); '', '' - если ошибка
    #####################################################
    # User.photo=UserProfilePhoto(
    #   photo_big  =FileLocation(secret=-2235609098130881287, local_id=121702, dc_id=1, volume_id=803115276),
    #   photo_small=FileLocation(secret=9159805154486843342,  local_id=121700, dc_id=1, volume_id=803115276),
    #   photo_id=288420785393084382
    # )
    # Имя файла = 'obj_'+photo_id+'_'+local_id.jpg
    #####################################################
    # Channel.photo=ChatPhoto(
    # photo_big  =FileLocation(dc_id=2, secret=-8153148005583349211, local_id=58696, volume_id=235915920),
    # photo_small=FileLocation(dc_id=2, secret=-3687284038183352932, local_id=58694, volume_id=235915920)
    #)
    # Имя файла = 'obj_'+local_id.jpg
    #####################################################
    def getPhoto(self, author_id, api_obj):
        funCalback = lambda file: self.client.download_profile_photo(entity=api_obj, file=file)
        # funCalbackBig   = lambda file: self.client.download_profile_photo(entity=api_obj, file=file, download_big=True )
        # funCalbackSmall = lambda file: self.client.download_profile_photo(entity=api_obj, file=file, download_big=False)

        retNone = '' #, ''                                                                                            # инициализация
        if isinstance(api_obj, User):
            if not isinstance(api_obj.photo, UserProfilePhoto): return retNone
        elif isinstance(api_obj, Channel):
            if not isinstance(api_obj.photo, ChatPhoto): return retNone
        else: return retNone

        print(api_obj.photo)
        fFile = 'obj_'+str(api_obj.photo.photo_id)
        fPath = self.getPathShort(author_id, fFile+'.jpg')
        if not self.downloadFile(fPath=DAEMON_INI.FILE_BASE+fPath, fun=funCalback): return retNone
        print('+')
        return fPath

        # fFile      = 'obj_'+str(api_obj.photo.photo_big.local_id)                                                   # загрузить большое фото
        # fPathBig   = self.getPathShort(author_id, fFile+'.jpg')
        # if not self.downloadFile(fPath=DAEMON_INI.FILE_BASE+fPathBig, fun=funCalbackBig): return retNone

        # fFile      = 'obj_'+str(api_obj.photo.photo_small.local_id)                                                 # загрузить малое фото
        # fPathSmall = self.getPathShort(author_id, fFile+'.jpg')
        # if not self.downloadFile(fPath=DAEMON_INI.FILE_BASE+fPathSmall, fun=funCalbackSmall): return retNone

        # fPathSmall2 = self.getPathShort(author_id, self.fileIcon)
        # os.rename(DAEMON_INI.FILE_BASE+fPathSmall, DAEMON_INI.FILE_BASE+fPathSmall2)                                # фото на иконку

        # return fPathBig, fPathSmall2



    #####################################################
    # ЗАГРУЗИТЬ ФАЙЛ MEDIA
    #####################################################
    # author_id - id автора, str
    # api_media - MessageMediaPhoto | MessageMediaDocument
    # max_size  - максимальный размер файла, байт; 0-не установлен - for only document
    # return    - относительный путь закачанного файла (tg/xx/xx/xxxxxx.jpg), '' - если ошибка
    #####################################################
    # Message.media=MessageMediaPhoto(
    #   photo=Photo(
    #       has_stickers=False,
    #       id=5251482076920785058,
    #       date=datetime.fromtimestamp(1511781204.0),
    #       sizes=[
    #           PhotoCachedSize(
    #               w=90,
    #               bytes=b'\xff\xd8\xff\xe0\x00\ ...
    #               h=43,
    #               location=FileLocation(volume_id=238228300, dc_id=2, secret=-3766663937072106418, local_id=63396), type='s'),
    #               PhotoSize(w=319, h=153, location=FileLocation(volume_id=238228300, dc_id=2, secret=7682553958629216800, local_id=63395),
    #               type='x',
    #               size=12904
    #           )
    #       ],
    #       access_hash=-4741914692102327473
    #   ),
    # caption=None,
    # ttl_seconds=None
    # )
    #####################################################
    # Message.media=MessageMediaDocument(
    #   document=Document(
    #       access_hash=-6596365731581613700,
    #       version=0,
    #       mime_type='video/mp4',
    #       date=datetime.fromtimestamp(1511758651.0),
    #       attributes=[DocumentAttributeVideo(h=288, round_message=False, duration=1897, w=512), DocumentAttributeFilename(file_name='1.mp4')],
    #       id=5251260542051418365,
    #       size=126655134,
    #       thumb=PhotoSize(
    #           type='s',
    #           h=50,
    #           size=1832,
    #           location=FileLocation(local_id=39808, volume_id=238216574, secret=2658794311354958535, dc_id=2),
    #           w=90
    #       ),
    #       dc_id=2
    #   )
    # )
    #####################################################
    def getMedia(self, author_id, api_media, max_size=0):
        funCalback = lambda file: self.client.download_media(message=api_media, file=file)

        retNone = ''
        if isinstance(api_media, MessageMediaPhoto):
            if not isinstance(api_media.photo, Photo): return retNone
            fName = str(api_media.photo.id)                                                                         # файл: имя
        elif isinstance(api_media, MessageMediaDocument):
            if not isinstance(api_media.document, Document): return retNone
            if (max_size > 0) and (max_size < api_media.document.size): return retNone                              # превышение размера
            fName = str(api_media.document.id)                                                                      # файл: имя
        else: return retNone

        fExt = utils.get_extension(api_media)                                                                       # файл: расширение
        if fExt == '': return retNone
        fExt = fExt[1:]
        fPathShort = self.getPathShort(author_id, fName+'.'+fExt)                                                   # файл: путь относительный
        fPathFull  =  DAEMON_INI.FILE_BASE+fPathShort                                                               # файл: путь полный

        return fPathShort if self.downloadFile(fPath=fPathFull, fun=funCalback) else retNone



    #####################################################
    # ЗАГРУЗИТЬ ФАЙЛ
    #####################################################
    # return - True | False
    #####################################################
    def downloadFile(self, fPath, fun):
        ret = False
        try:
            os.makedirs(os.path.dirname(fPath), exist_ok=True)                                                      # создать каталог
            if not os.path.exists(fPath):                                                                           # файла нет
                try:
                    ret = fun(file=open(fPath, "wb"))                                                               # скачать файл
                    if not ret: os.remove(fPath)                                                                    # удалить файл при ошибке
                finally:
                    self.sleep()                                                                                    # задержка между запросами
            else: ret = True                                                                                        # файл есть
        #except (SystemExit, KeyboardInterrupt):
        #    os.remove(fPath)
        #    raise
        except BaseException as e:
            logError(e)
            os.remove(fPath)
            raise
        finally:
            return ret



    #####################################################
    # CAPTION ИЗ ВЛОЖЕНИЙ MEDIA
    #####################################################
    def getMediaCaption(self, api_message):
        ret = ''
        if isinstance(api_message, Message):
            if isinstance(api_message.media, (MessageMediaPhoto, MessageMediaDocument)):
                ret = getattr(api_message.media, 'caption', '')
                #if api_message.media.caption!=None: ret = api_message.media.caption  # !!!! не работает, так как в telethon/utils.py.get_input_media убрано .caption
        return ret


    #####################################################
    # ПОЛЬЗОВАТЕЛЬ: БОЛЕЕ ПОЛНАЯ ИНФО: UserFull ???
    #####################################################
    def getUserInfo(self, api_user):
        ret = None
        if isinstance(api_user, User):
            try:     ret = self.client(GetFullUserRequest(InputUser(api_user.id, api_user.access_hash)))
            finally: self.sleep()
        return ret


    #####################################################
    # ПОЛЬЗОВАТЕЛЬ: ПОСЛЕДНИЙ ВИЗИТ
    #####################################################
    # return - дата/время в формате SQL, None - ошибка
    # https://telegram.org/blog/privacy-revolution
    #####################################################
    def getUserLastVisit(self, api_user):
        last_visit = None
        if isinstance(api_user, User):
            if isinstance(api_user.status, UserStatusOffline): last_visit = api_user.status.was_online
            if isinstance(api_user.status, UserStatusOnline):  last_visit = datetimeNow()
            if last_visit != None: last_visit = sqlDateTime(datetimeCutSecond(last_visit).timestamp())
        return last_visit



    getPathShort       = lambda self, author_id, file: filePathShort(HOST_SHORT.TG, author_id, file)
    getSource          = lambda self, entity:  'https://t.me/'+self.getUsername(entity)+'/'
    isUser             = lambda self, entity:  isinstance(entity, User)
    isChannel          = lambda self, entity:  isinstance(entity, Channel)
    isPeerChannel      = lambda self, entity:  isinstance(entity, PeerChannel)
    isInputPeerChannel = lambda self, entity:  isinstance(entity, InputPeerChannel)
    isMessage          = lambda self, entity:  isinstance(entity, Message)
    idToUser           = lambda self, id:      self.getGlobalEntity(PeerUser(id))
    sleep              = lambda self, count=1: time.sleep(random.uniform(self.delayRequest*count/1.5, self.delayRequest*count*1.5))
    #def sleep(self, count=1):
    #    print(count)
    #    time.sleep(random.uniform(self.delayRequest*count/2, self.delayRequest*count))
    #    print('+')