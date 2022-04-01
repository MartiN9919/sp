# -*- coding: utf-8 -*-

#####################################################
# http://lxml.de/installation.html
# pip install lxml
# ver 3.7.3
#####################################################
# http://lxml.de/cssselect.html
# pip install cssselect
# ver 1.0.3
#####################################################

import time
import requests
import lxml.html
from   fun.funSys      import logger


#####################################################
# чтение текста в парсер
#####################################################
# addSpaces - добавлять пробелы в начале тела тегов
# alternativeDecode - альтернативное декодирование страницы
# return - {ParserURL.TEXT: текст, ParserURL.URL: ссылка после возможной переадресации}
# return - None - ошибка
#####################################################
class ParserURL:
      TEXT = 'text'
      URL  = 'url'

def parserGet(url, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
                            "Accept":"application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"}):
    return requests.get(url, headers=headers)


def parserURLDetail(url, isWait=True, addSpaces=False, alternativeDecode = False):
    iErr = 0
    while True:
        try:
            # запись страницы в файл для изучения
            #tt = requests.get(url, headers=headers).text
            #f = open("file.txt", "w")
            #f.write(url+'\n\n'+str(tt))
            #f.close()

            dat = parserGet(url)
            txt = dat.text if alternativeDecode else dat.content # пишут, что вместо .content нужно использовать .text, но nn.by так не работает, а bsblog.info - наоборот http://docs.python-requests.org/en/master/user/quickstart/

            ret = lxml.html.fromstring(txt)
            if addSpaces: parserErrSpaces(ret)

            ret = {ParserURL.TEXT: ret, ParserURL.URL: dat.url}
            break
        except Exception as e:
            ret = None
            if isWait:
                time.sleep(10)
                iErr += 1
            if (not isWait) or (iErr >= 10):
                logger.warning(str(e)+": "+url)
                iErr = 0
        if not isWait: break
    return ret


def parserURL(url, isWait=True, addSpaces=False, alternativeDecode = False):
    ret = parserURLDetail(url, isWait=True, addSpaces=False, alternativeDecode = False)
    return ret[ParserURL.TEXT] if ret!=None else None



#####################################################
# устранить ошибку парсинга: нет пробелов между блоками
#####################################################
def parserErrSpaces(parser):
    for el in parser.findall(".//div"):               # ".//*"
        if el.text: el.text = el.text + "\n"



#####################################################
# чтение текста из ПЕРВОГО подходящего блока
#####################################################
def parserGetTextFirst(block, selector, valEmpty=''):
    try:
        # у массива взять первый элемент
        if isinstance(block, list): _block_ = block[0]
        else:                       _block_ = block
        # селектор
        _block_ = _block_.cssselect(selector)
        # текст
        ret = _block_[0].text_content()
        if ret == '': ret = valEmpty
    except Exception as e:
        ret = valEmpty
    return ret



#####################################################
# чтение текста из ВСЕХ подходящих блоков
#####################################################
def parserGetTextAll(block, selector, separator='', valEmpty=''):
    try:
        # у массива взять первый элемент
        if isinstance(block, list): _block_ = block[0]
        else:                       _block_ = block
        # ищем текст
        arr = []
        #selector2 = 'html'
        #print(selector2, _block_.cssselect(selector2))
        for item in _block_.cssselect(selector):
            s = item.text_content().strip()
            if s != '': arr.append(s)
        ret = separator.join(arr)
        if ret == '': ret = valEmpty
    except Exception as e:
        ret = valEmpty
    return ret



#####################################################
# чтение текста из блока за пределами тэгов
#####################################################
def parserGetTextWithoutTag(block, selector, valEmpty=''):
    try:
        # у массива взять первый элемент
        if isinstance(block, list): _block_ = block[0]
        else:                       _block_ = block
        # селектор
        _block_ = _block_.cssselect(selector)[0]
        # нужный текст находится вне тегов ==> убрать тэги
        for item in _block_.cssselect('*'): item.drop_tree()
        # взять оставшийся текст
        ret = _block_.text_content()
        if ret == '': ret = valEmpty
    except Exception as e:
        ret = valEmpty
    return ret



#####################################################
# чтение значения атрибута
#####################################################
def parserGetAttr(block, selector, attr, valEmpty=''):
    try:
        # у массива взять первый элемент
        if isinstance(block, list): _block_ = block[0]
        else:                       _block_ = block
        # селектор
        _block_ = _block_.cssselect(selector)
        ret = _block_[0].get(attr)               # _block_[0].attrib[attr]
        if ret == '': ret = valEmpty
    except Exception as e:
        ret = valEmpty
    return ret



#####################################################
# удаление ПЕРВОГО подходящего блока
#####################################################
def parserDelFirst(block, selector):
    try:
        if isinstance(block, list): _block_ = block[0]              # у массива взять первый элемент
        else:                       _block_ = block
        _block_ = _block_.cssselect(selector)                       # селектор
        _block_[0].drop_tree()                                      # удаление
    except Exception as e:
        pass



#####################################################
# удаление ВСЕХ подходящих блоков
#####################################################
def parserDelAll(block, selector):
    #try:
    if isinstance(block, list): _block_ = block[0]              # у массива взять первый элемент
    else:                       _block_ = block
    for item in _block_.cssselect(selector):
        item.drop_tree()                                        # удаление
    #except Exception as e:
    #    pass



#####################################################
# СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ DOM-ЭЛЕМЕНТА (КАК В HTML)
#####################################################
def DOMToText(DOM_Element):
    return str(lxml.html.tostring(DOM_Element)) if not (DOM_Element is None) else ''
