# -*- coding: utf-8 -*-

import re, html, json
from   lib.funConst import CHR, MSG


# re Look-ahead & Look-behind https://habr.com/ru/post/159483/   ТОЛЬКО ОДИНАРНЫЕ *: r'(?<!\*)(\*)(?!\*)'



################################################################################
# наличие в arr[][ind] = val
################################################################################
def findInArr(arr, ind, val):
    ret = False
    for rec in arr:
        if rec[ind] == val:
            ret = True
            break
    return ret


################################################################################
# поиск по формату
################################################################################
# findInBrackets - искать в скобках ...()..., иначе полное совпадение
################################################################################
def findStr(myStr, reg, valEmpty='', findInBrackets=True):
    val = re.search(reg, myStr)
    ind = 1 if findInBrackets else 0
    return val.group(ind) if val != None else valEmpty

# возрат списка найденных совпадений
def findStrAll(myStr, reg, valEmpty=[]):
    val = re.findall(reg, myStr)
    return val if val != None else valEmpty


################################################################################
# замена по формату
################################################################################
def replStr(myStr, newBlock, reg):
    return re.sub(reg, newBlock, myStr)


################################################################################
# преобразовать к нормальному виду прочитанную из БД JSON структуру
################################################################################
def JSONNormal(text):
    return json.loads(textJSONNormal(text.replace('\r', '')), strict=False) if text!=None else {}


################################################################################
# нормальная строка для парсинга в JSON
################################################################################
def textJSONNormal(text):
    ret = replStr(text+'\n', ' ', r'(\#\#.*\n)')                    # удалить комментарии: ## ...
    ret = replStr(ret,  ' ', r'([\t])')                             # символ табуляции
    ret = textStrip(ret)                                            # только один пробел и удаляем по сторонам, удаляет chr(10), chr(13)
    return ret


################################################################################
# текстовую строку в JSON (JSON без крайних скобок)
################################################################################
def textToJSON(text):
    return json.loads('{'+textJSONNormal(text)+'}', strict=False)


################################################################################
# только один пробел и удаляем по сторонам, удаляет chr(10), chr(13)
################################################################################
def textStrip(text):
    return ' '.join(text.split()).strip()


################################################################################
# нормальный текст
################################################################################
def textNormal(text, isNewStr=False):
    if text is None: return ''
    lst  = [['\\',     ' '],
            [chr(9),   ' '], # tab на пробел
            [chr(39),  '"'], # кавычки одиночные на двойные
            [chr(160), ' '], # неразрывный пробел на обычный ТОЛЬКО С АПРЕЛЯ 2018
            ['−',      '-'], # длинная черта на минус ТОЛЬКО С АПРЕЛЯ 2018
            ['—',      '-'], # еще какая-то черта на минус ТОЛЬКО С ИЮЛЯ 2018
            ['–',      '-'], # это также надо, хоть и внешне похож на предыдущий ТОЛЬКО С ИЮЛЯ 2018
            ['`',      '"'], # С СЕНТЯБРЯ 2018
            ['«',      '"'],
            ['»',      '"'],
            ['“',      '"'],
            ['”',      '"'],
            ['ё',      'е'], # С СЕНТЯБРЯ 2018
            ['Ё',      'Е'], # С СЕНТЯБРЯ 2018
            ['&quot;', '"'], # " html.unescape их меняет также
            ['&amp;',  '"'], # &
            ['&apos;', '"'], # апостроф
            ['&nbsp;', ' ']] # неразрывный пробел на обычный
    if isNewStr:
        lst.append([chr(10), '<chr(10)>'])
        lst.append([chr(13), '<chr(13)>'])
    for item in lst: text = html.unescape(text.replace(item[0], item[1]))           # html.unescape с АПРЕЛЯ 2018
    text = replStr(text,  '', r'\w*@\w*\.\w+')                                      # del email
    text = ''.join([i if CHR.ALL.find(i) > -1 else '' for i in text])               # допустимые символы, убирает @
    #text = text.replace(".", ". ").replace("!", "! ").replace("?", "? ")           # устраняет ошибку html-парсинга text_content() когда блоки объединяются без пробелов, НО ПОРТИТ ВРЕМЯ 00. 00 И ТЕКСТ В КАВЫЧКАХ: "ААА! " А ЭТО УСТРАНЯТЬ ЗАТРАТНО
    text = replStr(text,  '', r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*')  # del url
    text = replStr(text,  '', r'www\.[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*')      # del url: www.bsuir.unibel.by
    text = ' '.join(text.split()).strip()                                           # только один пробел и удаляем по сторонам, удаляет chr(10), chr(13)
    if isNewStr:
        text = text.replace('<chr(10)>', chr(10))
        text = text.replace('<chr(13)>', chr(13))

    # разделяем русскую и английскую части пробелом
    # ИНАЧЕ ПАДАЕТ SPHINX FOR WINDOWS
    #for ind in range(len(text)-2, -1, -1):
    #    if CHR.ENG.find(text[ind])   == -1: continue
    #    if CHR.RUS.find(text[ind+1]) == -1: continue
    #    text = text[:ind+1]+' '+text[ind+1:]

    return text


################################################################################
# текст без объектов типа <ФАЙЛ: ...> (arc.title_name, arc.content)
################################################################################
def textWithoutObj(text):
    #ret = replStr(ret, '', r'\[\/QUOTE.+\]')
    ret = replStr(text, '', r'\<.+:.+\>')                                           # r'\<.+\>' группы темы: '<...>' - оставить, собъекты: '<ФОТО:...>' - удалить
    ret = replStr(ret,  '', r'[А-Я]+[:\d_-]+\s')                                    # ЛОЖНОЕ СРАБАТЫВАНИЕ: 'ТОП-8 ...'
    ret = replStr(ret,  '', r'\<ССЫЛКА\s')
    ret = replStr(ret,  '', r'\<')
    ret = replStr(ret,  '', r'\>')
    #ret = replStr(ret,  '', r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*')    # del url - УДАЛИТЬ - уже есть в textNormal()
    ret = ret.strip()
    if len(ret)>0:
        if ret[-1] in ['.', ',', ':']: ret = ret[:-1]
    if ret == '': ret = MSG.NO_TEXT
    return ret


################################################################################
#    обрезать текст с добавлением многоточия
################################################################################
def textCutDots(text, max_length):
    ret = text
    if len(ret) > max_length: ret = text[:max_length-3]+'...'
    return ret


################################################################################
#    удалить из текста цифры
################################################################################
def textDigitsDel(word):
    return ''.join([char for char in word if not char.isdigit()])


################################################################################
#    цифры в конце текста
################################################################################
def textDigitsLast(text, pref='', valEmpty=''):
    val = re.match('.*?'+pref+'([0-9]+)$', text)
    return val.group(1) if not val is None else valEmpty


################################################################################
#    содержит ли текст хоть одну цифру
################################################################################
def textConsistDigits(word):
    ret = False
    for char in word:
        if char.isdigit():
            ret = True
            break
    return ret


################################################################################
#   URL
################################################################################
def isURL(url):
    _url_ = str(url)
    if len(_url_) < 6: return False
    return (_url_[:4] == 'http')

def strURL(url):
    return url if isURL(url) else ''

def urlCut(text):
    val = re.search("(?P<url>https?://[^\s^|]+)", text)
    url = '' if val is None else val.group("url")
    txt = text.replace(url, '')
    return url.strip(), txt.strip()

# def urlGet(text, before='', after=''):
#     val = re.search(before+"(?P<url>https?://[^\s^|]+)"+after, text)
#     url = '' if val is None else val.group("url")
#     return url.strip()

def urlsGet(text):
    return re.findall("https?://[^\s^|^>]+", text)

def urlToHost(url):
    s = url.replace("http://", "")
    s = s.replace("https://", "")
    s = s.replace("www.", "")
    s = s.split('/')
    s = s[0] if len(s)>0 else ''
    s = s.split('.')
    return (s[-2]+'.'+s[-1]) if len(s)>1 else ''

def urlCutParam(text):
    return replStr(text, '', r'\?.*')

# парсить в массив URL AJAX--запроса
# '/aj/dat/mm/ss' -> [mm', 'ss'] (skipFirst=2)
def urlAjaxParse(urlAjax, skipFirst=0):
    ret   = []
    count = -1
    for item in urlAjax.split('/'):
        if item=='': continue
        count += 1
        if count < skipFirst: continue
        ret.append(item)
    return ret
