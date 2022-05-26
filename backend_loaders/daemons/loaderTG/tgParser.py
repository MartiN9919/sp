# -*- coding: utf-8 -*-

import gc, os
from   lib.funConst  import ARC, REL, UNIT, HOST
from   lib.funSys    import logger, logError, sqlDateTime, datetimeCutSecond, strToDatetime
from   lib.funText   import textNormal, textCutDots
from   lib.funFile   import filePrefDel
from   lib.funBDArc  import ArcWriter, arcMarkDel
from   lib.funBDUnit import UnitWriter
from   lib.funBDRel  import RelWriter
from   lib.funBDFile import FileWriter
from   lib.funLoader import getLoaderSync, GetLoaderSync


class TGParser():
    mediaMaxSize = 10000000      # максимальный размер загружаемого файла - 10M
    bios         = None
    tg           = None          # api telegram
    myTimeOffset = 0             # смещение между временем на сайте и на сервере, сек.
    isError      = False         # признак ошибки


    #####################################################
    # КОНСТРУКТОР
    #####################################################
    def __init__(self, tg):
        self.tg                = tg
        self.bios              = {}
        self.bios["wArc"]      = ArcWriter  (10000, 1000, True, True, True)
        self.bios["wUnit"]     = UnitWriter (10000, 1000, True, True, True)
        self.bios["wRel"]      = RelWriter  (25000, 25000)
        self.bios["wFile"]     = FileWriter (25000, 25000)
        ret, self.myTimeOffset = self.getTimeSync()
        self.isError = (not ret) or self.isError


    #####################################################
    # ПСЕВДО-ДЕСТРУКТОР
    #####################################################
    def free(self):
        self.bios["wArc"] .stop(True)
        self.bios["wUnit"].stop(True)
        self.bios["wRel"] .stop(True)
        self.bios["wFile"].stop(True)
        self.bios = None
        gc.collect()


    #####################################################
    # ПАРСИТЬ КАНАЛ (СООБЩЕНИЯ, ФОТО, МЕДИА)
    #####################################################
    # entityLocal   - InputPeerChannel
    # min_timestamp - дата/время, минимум до которой читать, 0 - читать всё
    # advanced      - полная выкачка: parseMembers, parseUser, loadFiles, иначе ТОЛЬКО сообщения
    # return        - количество помещенных в очередь сообщений+связей
    #####################################################
    def parseChannel(self, entityLocal, min_timestamp, advanced):
        obj_name = lambda name: ('_'+textCutDots(name, 253)+'_') if name != None else ''

        retMsg = retRel = retFile = 0
        if self.tg.isInputPeerChannel(entityLocal):
            if advanced: self.parseMembers(entityLocal)                                                             # парсить участников канала
            title_id   = str(self.tg.getGlobalID(entityLocal))
            title_name = obj_name(self.tg.getName(entityLocal))                                                     # отображаемое имя
            source     = self.tg.getSource(entityLocal)
            for msg in self.tg.getMessages(entityLocal):                                                            # читать сообщения с канала
                if not self.tg.isMessage(msg): continue                                                             # обработка только сообщений (напр., Action не обрабатываются)
                if ((msg.date.timestamp()+self.myTimeOffset) < min_timestamp): break                                # старые сообщения не обрабатывать

                if msg.from_id != None:                                                                             # для user
                    obj         = self.tg.idToUser(msg.from_id)
                    if obj is None: continue
                    author_id   = str(obj.id)
                    author_name = self.tg.getName(obj)
                    if advanced: self.parseUser(obj)                                                                # парсить данные о пользователях

                elif (msg.from_id == None) and self.tg.isPeerChannel(msg.to_id):                                    # для channel
                    if advanced:
                        obj     = self.tg.getGlobalEntity(msg.to_id)
                        if obj is None: continue
                    author_id   = title_id
                    author_name = title_name

                else: continue
                if author_name=='': author_name = 'id'+str(author_id)

                url = source+str(msg.id)

                content = (textNormal(self.tg.getMediaCaption(msg))+' '+textNormal(msg.message)).strip()            # текст сообщения
                if (content == ''): continue
                if (msg.fwd_from != None):
                    content = 'Репост: '+content
                    if msg.fwd_from != None:
                        if msg.fwd_from.from_id != None:
                            val = msg.fwd_from.from_id.channel_id
                            if val != None:
                                author_id   = str(val)
                                author_name = obj_name(self.tg.getName(val))

                # запись в rel
                relRec = {
                    REL.TO_HOST:   HOST.TG,
                    REL.TO_ID:     title_id,
                    REL.FROM_HOST: HOST.TG,
                    REL.FROM_ID:   author_id,
                    REL.TYPE:      REL.TYPE_ARC,
                    REL.HOST:      HOST.TG,
                    REL.OBJECT:    title_id+' '+str(msg.id),
                    REL.SOURCE:    url,
                }
                self.bios["wRel"].recAdd(relRec)
                retRel += 1

                # запись в arc
                arcRec                  = self.bios["wArc"].recIni()
                arcRec[ARC.CRC_REL]     = relRec[REL.CRC]
                arcRec[ARC.CRC_REL]     = relRec[REL.CRC]
                arcRec[ARC.TYPE]        = ARC.TYPE_SOCIAL
                arcRec[ARC.DATE]        = sqlDateTime(datetimeCutSecond(msg.date).timestamp()+self.myTimeOffset)
                arcRec[ARC.HOST]        = HOST.TG
                arcRec[ARC.SOURCE]      = url
                arcRec[ARC.GROUP_ID]    = title_id
                arcRec[ARC.TITLE_ID]    = title_id
                arcRec[ARC.TITLE_NAME]  = title_name
                arcRec[ARC.CONTENT]     = content
                arcRec[ARC.AUTHOR_ID]   = author_id
                arcRec[ARC.AUTHOR_NAME] = author_name
                arcRec[ARC.VIEW_ALL]    = str(msg.views) if msg.views != None else '0'
                self.bios["wArc"].recAdd(arcRec)
                retMsg += 1

                # скачать файлы
                if advanced:
                    fPhoto = self.tg.getPhoto(author_id=author_id, api_obj  =obj)                                      # скачать фото пользователя/группы
                    # fPhotoBig, fPhotoSmall = self.tg.getPhoto(author_id=author_id, api_obj  =obj)                                      # скачать фото пользователя/группы
                    fMedia = self.tg.getMedia(author_id=author_id, api_media=msg.media, max_size=self.mediaMaxSize)    # скачать медиа-файл

                    # запись в file (только регистрация), поэтому source не указывать !!!
                    if fPhoto != '': self.bios["wFile"].recAdd(host=HOST.TG, path=filePrefDel(fPhoto), arc_crc='', unit_id=arcRec[ARC.AUTHOR_ID])
                    # if fPhotoBig   != '': self.bios["wFile"].recAdd(host=HOST.TG, path=filePrefDel(fPhotoBig),   arc_crc='',              unit_id=arcRec[ARC.AUTHOR_ID])
                    # if fPhotoSmall != '': self.bios["wFile"].recAdd(host=HOST.TG, path=filePrefDel(fPhotoSmall), arc_crc='',              unit_id=arcRec[ARC.AUTHOR_ID])
                    if fMedia      != '': self.bios["wFile"].recAdd(host=HOST.TG, path=filePrefDel(fMedia),      arc_crc=arcRec[ARC.CRC], unit_id=arcRec[ARC.AUTHOR_ID])
                    retFile += ((1 if fPhoto!='' else 0)+(1 if fMedia!='' else 0))
                    # retFile += ((1 if fPhotoBig!='' else 0)+(1 if fPhotoSmall!='' else 0)+(1 if fMedia!='' else 0))

        gc.collect()
        logger.debug('Channel messages: '+str(retMsg)+'/'+str(retRel)+'/'+str(retFile))
        return retMsg+retRel+retFile



    #####################################################
    # ПАРСИТЬ УЧАСТНИКОВ КАНАЛА
    #####################################################
    # entity - Channel, InputPeerChannel и т.д.
    # return - количество участников
    #####################################################
    def parseMembers(self, entity):
        #if not (self.tg.isChannel(entity) or self.tg.isInputPeerChannel(entity)): return 0
        ret    = 0
        users  = self.tg.getMembers(entity)
        if len(users)==0: return ret

        to_id  = str(self.tg.getGlobalID(entity))
        source = self.tg.getSource(entity)
        for user in users:
            self.parseUser(user)
            rec                = {}
            rec[REL.TO_HOST]   = HOST.TG
            rec[REL.TO_ID]     = to_id
            rec[REL.FROM_HOST] = HOST.TG
            rec[REL.FROM_ID]   = str(user.id)
            rec[REL.TYPE]      = REL.TYPE_GROUP
            rec[REL.HOST]      = HOST.TG
            rec[REL.OBJECT]    = ''
            rec[REL.SOURCE]    = source
            self.bios["wRel"].recAdd(rec)
            ret += 1
        logger.debug('Channel members: '+str(ret))
        return ret



    #####################################################
    # ПАРСИТЬ USER
    #####################################################
    # entity - User
    #####################################################
    def parseUser(self, entity):
        if not self.tg.isUser(entity): return
        last_visit = self.tg.getUserLastVisit(entity)
        if last_visit == None: last_visit = '1800-01-01'

        rec = {}
        rec[UNIT.HOST]         = HOST.TG
        rec[UNIT.ID]           = str(entity.id)
        rec[UNIT.SOURCE]       = '' #self.tg.getSource(entity)
        rec[UNIT.NAME]         = self.tg.getName(entity)
        rec[UNIT.BDATE]        = '1800-01-01'
        rec[UNIT.RDATE]        = '1800-01-01'
        rec[UNIT.COUNTRY]      = ''
        rec[UNIT.CITY]         = ''
        rec[UNIT.INFO]         = ''
        rec[UNIT.DESCRIPT]     = ''
        rec[UNIT.VISIT_DATE]   = last_visit
        rec[UNIT.VISIT_DEVICE] = UNIT.VISIT_DEVICE_UNKNOW
        self.bios["wUnit"].recAdd(rec)


    def parseArcMarkDel(self, tsPeriodStart, tsScanStart):
        self.bios["wArc"].waitEmpty()                                                       # !!! перед вызовом очередь должна быть записана
        arcMarkDel(HOST.TG, tsPeriodStart, tsScanStart)                                     # tsPeriodStart один для воркера



    #####################################################
    # смещение между временем на сайте и на сервере, сек.
    #####################################################
    def getTimeSync(self):
        #return True, 10800
        try:
            # что должно быть
            dat = getLoaderSync(HOST.TG)
            if len(dat) != 1: raise ValueError('Sync: record not found')
            dat1 = strToDatetime(str(dat[0][GetLoaderSync.VAL])).timestamp()

            # что есть
            idUser = dat[0][GetLoaderSync.VAR1]
            if idUser.isdigit(): idUser = int(idUser)
            entity = self.tg.getLocalEntity(idUser)
            if entity == None: entity = self.tg.getGlobalEntity(idUser)
            if entity == None: raise ValueError('Sync: user entity not read')
            val    = self.tg.getMessages(entity)
            if len(val) == 0: raise ValueError('Sync: label not read')
            dat2 = datetimeCutSecond(val[-1].date).timestamp()

            # сравнение
            ret = int(dat1-dat2)
            logger.info('Sync: the host different time of syncronize is '+str(ret)+' s.')
            return True, ret

        except Exception as e:
            logError(e)
            return False, 0

