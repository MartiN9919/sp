# -*- coding: utf-8 -*-

import gc, html, json, time, datetime, feedparser
from   fun.funConst      import ARC
from   fun.funSys        import logger, logError, sqlDateTime, getUTC, tsNow, getMD5
from   fun.funText       import replStr, findStr, textNormal, textJSONNormal
from   fun.funLoader     import GetNodSite, loaderUrlVerify, loaderUrlAdd, loaderUrlClear
from   fun.funParser     import ParserURL, parserURLDetail, parserGetTextFirst, parserGetTextAll, parserDelAll, DOMToText


#####################################################
# парсинг BD.LOADER_NOD.rec
#####################################################
# bios          - классы ввода/вывода
# rec           - запись BD.LOADER_NOD
# min_timestamp - дата/время, минимум до которой читать, 0 - читать всё
# return        - количество помещенных в очередь записей
#####################################################
def parserSiteRSS(bios, rec, min_timestamp):
    JSON_EXCEPT        = 'except'                                                                   # маски (в т.ч. регулярки) исключаемых из обработки url, проверка до и после выкачки
    JSON_DECODE        = 'decode'                                                                   # при загрузке в парсер вместо content использовать text
    JSON_PARSE         = 'parse'

    JSON_FIELD         = 'field'
    JSON_WARNING       = 'warning'
    JSON_OPERATION     = 'operation'
    JSON_OPERATION_SUM = 'sum'
    JSON_DOM_DEL       = 'dom_del'
    JSON_TEXT          = 'text'
    JSON_TEXT_DEL      = 'text_del'
    JSON_TEXT_REPLACE  = 'text_replace'

    #####################################################
    def isExcept(url):
        ret = False
        for except_item in JSONExcept:
            if findStr(myStr=url, reg=except_item, findInBrackets=False) != '':
                ret = True
                break
        return ret


    #####################################################
    ret = 0
    logger.info('Start: '+rec[GetNodSite.HOST])

    try:
        feed = feedparser.parse(rec[GetNodSite.URL])
    except Exception as e:
        logError(e)
        return ret

    loaderUrlClear()
    for item in feed.entries:
        try:
            published = item.published_parsed if hasattr(item, 'published_parsed') else None        # дата публикации
            ts = (time.mktime(item.published_parsed)+getUTC()+rec[GetNodSite.TS_CORRECT]*60*60) if (published != None) else tsNow()
            if ts < min_timestamp: continue

            source = item.get('link', '').strip()
            if loaderUrlVerify(source): continue                                                    # если недавно читали - пропустить
            param  = json.loads(textJSONNormal(rec[GetNodSite.PARAM]), strict=False)                # JSON-структура: читать
            if isinstance(param, list): param = {JSON_PARSE: param}                                 # JSON-структура: расшифровка сокращенной записи

            JSONDecode = param.get(JSON_DECODE, False)                                              # альтернативный вариант декодирования
            JSONExcept = param.get(JSON_EXCEPT, [])                                                 # исключения для source
            if not isinstance(JSONExcept, list): JSONExcept = [JSONExcept]                          # расшифровка сокращенной записи

            if isExcept(source): continue                                                           # пропустить исключения: первый шаг - до выкачки как в source

            arcRec                  = bios["wArc"].recIni()
            arcRec[ARC.TYPE]        = ARC.TYPE_RSS
            arcRec[ARC.HOST]        = rec[GetNodSite.HOST]
            arcRec[ARC.COUNTRY]     = rec[GetNodSite.COUNTRY]
            arcRec[ARC.SOURCE]      = source
            arcRec[ARC.TITLE_NAME]  = item.get('title', '')
            arcRec[ARC.DATE]        = sqlDateTime(ts)
            arcRec[ARC.AUTHOR_NAME] = item.get('author', '')

            val = item.get('tags', [])
            if len(val) > 0: arcRec[ARC.GROUP_ID] = val[0].get('term', '')                          # например: 'Общество', 'Аналитика' и т.д.

            arcRec[ARC.GROUP_ID]    = textNormal(arcRec[ARC.GROUP_ID   ])
            arcRec[ARC.TITLE_NAME]  = textNormal(arcRec[ARC.TITLE_NAME ])
            arcRec[ARC.TITLE_ID]    = getMD5(arcRec[ARC.TITLE_NAME     ])
            arcRec[ARC.AUTHOR_NAME] = textNormal(arcRec[ARC.AUTHOR_NAME])

            parserDetail = parserURLDetail(url=arcRec[ARC.SOURCE], addSpaces=True, alternativeDecode=JSONDecode, isWait=False) # читать сайт
            if parserDetail == None: break                                                          # при ошибке чтения прервать (continue)
            parser = parserDetail[ParserURL.TEXT]
            if isExcept(parserDetail[ParserURL.URL]): continue                                      # пропустить исключения: второй шаг - после выкачки учитываем возможную переадресацию

            # не испытывал
            # лечит 'utf-8' codec can't decode byte 0xd0 in position 92: invalid continuation byte
            #.get_content_charset() определить кодировку (iso-8859-1)
            #doc = html.document_fromstring(page.read().decode('iso-8859-1'))

            parserDelAll(parser, 'script')                                                          # выбросить не нужное
            parserDelAll(parser, 'figure')
            parserDelAll(parser, 'style')
            parserDelAll(parser, 'img')

            for item in param.get(JSON_PARSE, []):                                                  # JSON-структура: просмотреть
                if not isinstance(item, dict): continue                                             # JSON-элемент - словарь?

                JSONField       = item.get(JSON_FIELD,        '')                                   # заполняемое поле
                JSONWarning     = item.get(JSON_WARNING,      True)                                 # предупреждение в лог о пустом поле
                JSONOperation   = item.get(JSON_OPERATION,    '')                                   # тип операции
                JSONDomDel      = item.get(JSON_DOM_DEL,      [])                                   # DOM-блоки для удаления
                JSONText        = item.get(JSON_TEXT,         '')                                   # получить текст
                JSONTextReplace = item.get(JSON_TEXT_REPLACE, [])                                   # текст для замены
                JSONTextDel     = item.get(JSON_TEXT_DEL,     [])                                   # текст для удаления

                if not isinstance(JSONDomDel,      list): JSONDomDel      = [JSONDomDel]            # расшифровка сокращенной записи
                if not isinstance(JSONText,        list): JSONText        = [[JSONText, ""]]
                if not isinstance(JSONTextReplace, list): JSONTextReplace = [JSONTextReplace]
                if not isinstance(JSONTextDel,     list): JSONTextDel     = [JSONTextDel]

                for data_item in JSONDomDel:                                                        # удалить ненужные DOM-блоки
                    parserDelAll(parser, data_item)

                if JSONOperation == '':                                                             # операция: ЧИТАТЬ
                    result = ''
                    for data_item in JSONText:
                        txt = parseText(parser, data_item[0])
                        if data_item[1] != '': txt = findStr(txt, data_item[1])
                        result += ' '+txt
                    result = result.strip()
                    if result != '': arcRec[JSONField] = result
                    else:
                        if JSONWarning: logger.warning('не прочитано [' + JSONField + ']: ' + arcRec[ARC.SOURCE])

                if JSONOperation == JSON_OPERATION_SUM:                                             # операция: СУММА
                    result = 0
                    for data_item in JSONText:
                        txt = parser.cssselect(data_item[0])                                        # читать содержимое элемента
                        if isinstance(txt, list):
                            if len(txt) > 0: txt = txt[0]
                            else:            txt = None
                        txt = DOMToText(txt)
                        if data_item[1] != '': txt = findStr(txt, data_item[1])                     # найти в нем нужный текст
                        if txt.isdigit(): result += int(txt)
                    arcRec[JSONField] = str(result)

                for data_item in JSONTextReplace:                                                   # заменить текст
                    arcRec[JSONField] = arcRec[JSONField].replace(data_item[0], data_item[1])
                for data_item in JSONTextDel:                                                       # удалить ненужный текст
                    arcRec[JSONField] = arcRec[JSONField].replace(data_item, '')
                arcRec[JSONField] = arcRec[JSONField].strip()


            if  (arcRec[ARC.TITLE_NAME] == '') or \
                (arcRec[ARC.SOURCE]     == '') or \
                (arcRec[ARC.CONTENT]    == ''):                                                      # нет полей
                s = ((ARC.TITLE_NAME+' ') if arcRec[ARC.TITLE_NAME] == '' else '') + \
                    ((ARC.SOURCE+' ')     if arcRec[ARC.SOURCE]     == '' else '') + \
                    ((ARC.CONTENT+' ')    if arcRec[ARC.CONTENT]    == '' else '')
                logger.warning('пустое поле [' + s.strip() + ']: ' + arcRec[ARC.SOURCE])
                continue
            if (arcRec[ARC.CONTENT]    == ''): continue
            if arcRec[ARC.VIEW_ALL] == '': arcRec[ARC.VIEW_ALL] = '0'
            if arcRec[ARC.LIKE_YES] == '': arcRec[ARC.LIKE_YES] = '0'
            if arcRec[ARC.LIKE_NO]  == '': arcRec[ARC.LIKE_NO]  = '0'
            if arcRec[ARC.REPOST]   == '': arcRec[ARC.REPOST]   = '0'

            #print(arcRec[ARC.SOURCE], '\n', arcRec[ARC.LIKE_YES]+' '+arcRec[ARC.REPOST]+' '+arcRec[ARC.VIEW_ALL], '\n', arcRec[ARC.CONTENT], '\n')
            #print(arcRec)
            bios["wArc"].recAdd(arcRec)
            loaderUrlAdd(source)                                                                    # запомнить url чтобы не повторять
            ret += 1

        except Exception as e:
            logError(e, str(item))
        finally:
            arcRec = None

    # сборщик мусора
    gc.collect()

    logger.debug('Leave: '+rec[GetNodSite.HOST]+' '+str(ret))
    return ret


def parseText(parser, selector): return textNormal(parserGetTextAll(parser, selector.strip(), ' '))



# ss.attrib['data-content'])   ss.text    .encode('utf-8')
