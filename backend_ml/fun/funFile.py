# -*- coding: utf-8 -*-

import os, csv, pickle, shutil

from   fun.funConst import HOST, HOST_SHORT, HOST2HOST_SHORT, FILE_UNIT_ICON
from   fun.funSys   import strUnique #, packageValid
from   fun.funText  import textDigitsLast


###################################################################################
#  ЧИТАЕТ ФАЙЛ ПО СТРОКАМ (ГЕНЕРАТОР)
###################################################################################
class FileReadLines(object):
    def __init__(self, path, encoding='utf-8'): # cp1251
        self.path     = path
        self.encoding = encoding

    def __iter__(self):
        try:
            f = None
            with open(self.path, "r", encoding=self.encoding) as f:
                for line in f: yield line
        finally:
            if f != None: f.close


###################################################################################
# УДАЛИТЬ ПУСТЫЕ ДИРЕКТОРИИ
###################################################################################
def dirDelEmpty(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            dirDelEmpty(a)
            if not os.listdir(a): os.rmdir(a)


###################################################################################
# УДАЛИТЬ НЕ ПУСТЫЕ ДИРЕКТОРИИ
###################################################################################
def dirDel(path):
    shutil.rmtree(path)


###################################################################################
# ДОБАВИТЬ К ИМЕНИ ФАЙЛА ПОСТФИКС
###################################################################################
# path/filename+postfix.ext
###################################################################################
def filePostfixAdd(file, postfix):
    filePath = os.path.dirname(file)
    fileName = os.path.splitext(os.path.basename(file))
    return os.path.join(filePath, fileName[0]+postfix+fileName[1])


###################################################################################
# НАИБОЛЬШАЯ ЦИФРОВАЯ ЧАСТЬ ПОСТФИКСА (INT)                      -1 - нет постфикса
###################################################################################
def filePosfixMax(path, postfixBegin):
    files = os.listdir(path)
    prefs = list(map(lambda x: filePostfixGet(file=x, postfixBegin=postfixBegin), files))  # [-1, 2, 5, ...]
    return max(prefs)


###################################################################################
# ЦИФРОВАЯ ЧАСТЬ ПОСТФИКСА = -1 - нет постфикса   file - имя файла (можно с путем)
###################################################################################
filePostfixGet = lambda file, postfixBegin: int(textDigitsLast(text=os.path.splitext(os.path.basename(file))[0], pref=postfixBegin, valEmpty='-1'))


###################################################################################
# УНИКАЛЬНОЕ ИМЯ ФАЙЛА
###################################################################################
# file - имя файла (можно с путем)
###################################################################################
fileUnique = lambda file: filePostfixAdd(file, '_'+strUnique())


###################################################################################
# ПРОВЕРИТЬ РАСШИРЕНИЕ ФАЙЛА
###################################################################################
# path - [полный путь] + файл
# ext  - проверяемое расширение С ТОЧКОЙ ИЛИ БЕЗ, регистр не важен
###################################################################################
def extValidate(path, ext):
    ext2 = ('.'+ext) if ext[0]!='.' else ext
    return path.lower().endswith(ext2.lower())


###################################################################################
# УСТАНОВИТЬ/ЗАМЕНИТЬ РАСШИРЕНИЕ ФАЙЛА
###################################################################################
# path - [полный путь] + файл
# ext  - проверяемое расширение С ТОЧКОЙ ИЛИ БЕЗ
###################################################################################
def extSet(path, ext):
    return os.path.splitext(path)[0]+(('.'+ext) if ext[0]!='.' else ext)


###################################################################################
# КРАТКИЙ ПУТЬ К ФАЙЛУ В БАЗЕ
###################################################################################
# host = HOST. ... или HOST_SHORT. ...
# id   = '' иконка хоста
###################################################################################
def filePathShort(host, id, file):
    return filePrefAdd(hostShort(host)+'/'+str(id)+'/'+file) if id != '' else (hostShort(host)+'/'+iconFile(host))


###################################################################################
# КРАТКИЙ ПУТЬ К ИКОНКЕ В БАЗЕ
###################################################################################
# host = HOST. ... или HOST_SHORT. ...
###################################################################################
def iconPathShort(host, id):
    host2 = hostShort(host)
    return filePathShort(host2, id, iconFile(host2))


###################################################################################
# ФАЙЛ ИКОНКИ - АВАТАРКИ
###################################################################################
# host = HOST. ... или HOST_SHORT. ...
###################################################################################
def iconFile(host):
    return FILE_UNIT_ICON.get(host, '')

def hostShort(host):
    return HOST2HOST_SHORT.get(host, host)



###################################################################################
# ПРЕФИКС - КАТАЛОГ
###################################################################################
# vk/n/-12345/nnn.txt <--> vk/n/-1/23/45/-12345/nnn.txt
# vk/n/1234/nnn.txt   <--> vk/n/12/34/0/1234/nnn.txt
# vk/n/1/nnn.txt      <--> vk/n/1/0/0/1/nnn.txt
###################################################################################
def filePrefAdd(path):
    s   = os.path.split(path)  # ('vk/n/-12345', 'nnn.txt')
    arr = s[0].split('/')
    s1  = arr[-1][0:2]
    s2  = arr[-1][2:4]
    s3  = arr[-1][4:6]
    if s2 == '': s2 = '0'
    if s3 == '': s3 = '0'
    arr.insert(-1, s1)
    arr.insert(-1, s2)
    arr.insert(-1, s3)
    return '/'.join(arr)+'/'+s[1]

def filePrefDel(path):
    s   = os.path.split(path) # ('vk/n/-1/23/45/-12345', 'nnn.txt')
    arr = s[0].split('/')
    arr.pop(-2)
    arr.pop(-2)
    arr.pop(-2)
    return '/'.join(arr)+'/'+s[1]


# if packageValid('Django'):
#     from django.conf import settings
#     def filePrefGet(host, id, count=500):
#         ret = []
#         iCount = 0
#         try:
#             pathLocal = filePrefAdd(os.path.splitext(host)[0]+'/'+str(id)+'/')
#             pathFull  = settings.FILES_DB_DIR+'/'+pathLocal
#             for fileName in os.listdir(pathFull):
#                 if os.path.isfile(os.path.join(pathFull, fileName)):
#                     ret.append('/files/db/'+pathLocal+fileName)
#                     iCount+=1
#                     if iCount >= count: break
#         except:
#             pass
#         return ret


def listSaveCSV(my_list, file):
    with open(file, "w") as f:
        writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in my_list: writer.writerow(item)
    f.close()

def listLoadCSV(file):
    ret = []
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter=' ', quotechar='|')
        for row in reader:
            row = list(map(lambda x: int(x), row))
            ret.append(row)
    f.close()
    return ret


#####################################################
# ОБЪЕКТ: ЧТЕНИЕ / ЗАПИСЬ (LIST, DICT etc.)
#####################################################
def objSave(obj, file):
    with open(file, "wb") as f: pickle.dump(obj, f)
    f.close()

def objLoad(file):
    with open(file, "rb") as f: ret = pickle.load(f)
    f.close()
    return ret



# #####################################################
# # КОЛЛЕКЦИЯ: СОХРАНИТЬ / ЗАГРУЗИТЬ
# #####################################################
# import collections
# def collectionSave(collect, file):
#     with open(file, "w") as f:
#         writer = csv.writer(f)
#         for key, val in collect.items(): writer.writerow([key, val])
#     f.close()

# def collectionLoadInt(file):
#     ret = collections.defaultdict(int)
#     with open(file, "r") as f:
#         reader = csv.reader(f)
#         for row in reader:
#             ret[row[0]] = row[1]
#     f.close()
#     return ret
