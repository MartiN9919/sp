# -*- coding: utf-8 -*-

import pytz, time, datetime, hashlib, logging, logging.handlers, copy, subprocess
from   dateutil.parser import parse

import fun.funBD

DAY_OF_WEEK_NAME = [
    ['понедельник', 'пнд'],
    ['вторник',     'втр'],
    ['среда',       'срд'],
    ['четверг',     'чтв'],
    ['пятница',     'птн'],
    ['суббота',     'сбт'],
    ['воскресенье', 'вск']
    ]


#==================================================================================
#======   ЛОГИ   ==================================================================
#==================================================================================
def setLogger(logFilePath, logName=None):
    logger = logging.getLogger(logName)
    logger.setLevel(logging.INFO)
    filehandler = logging.handlers.TimedRotatingFileHandler(logFilePath, when='midnight', interval=1, backupCount=10)
    filehandler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(filehandler)
    return logger

logger = logging.getLogger(__name__)
def logError(e, msg=''):
    logging.exception(e)
    msgStr = str(msg)[:1000]
    if msg != '': logger.error(msgStr)

def logInfo(msg):
    logger.info(msg)
    print(msg)



#==================================================================================
#======   SWITCH - CASE   =========================================================
#==================================================================================
# arr = {'key1': val1, 'keyN': valN}
# mCase = valN
# return = keyN
def mSwitch(arr, mCase):
    if mCase in arr: ret = arr[mCase]
    else: ret = ''
    return ret



###################################################################################
# ПРЕОБРАЗОВАТЬ В ОДНОМЕРНЫЙ СПИСОК
###################################################################################
lstDim1 = lambda data: [data] if not isinstance(data, list) else data


###################################################################################
# ПРЕОБРАЗОВАТЬ В ДВУХМЕРНЫЙ СПИСОК
###################################################################################
def lstDim2(data):
    ret = data
    if not isinstance(ret,    list): ret = [[ret]]    # одиночное значение в двумерный массив
    if len(ret) == 0:                ret = [[]]       # [] --> [[]]
    if not isinstance(ret[0], list): ret = [ret]      # одномерный массив в двумерный
    return ret


###################################################################################
# БЕЗ ОШИБОК ПРОЧИТАТЬ ПЕРВЫЙ ЭЛЕМЕНТ ОДНОМЕРНОГО МАССИВА, ПРИ ОШИБКЕ - None
###################################################################################
# def lstValFirst(lst):
#     if not isinstance(lst, list): return None
#     if len(lst) == 0: return None
#     return lst[0]


###################################################################################
# MAP ДЛЯ МНОГОМЕРНОГО СЛОЖНОГО СПИСКА
###################################################################################
def lstMap(arr, fun):
    if isinstance(arr, list):
        for ind in range(0, len(arr)): arr[ind] = lstMap(arr[ind], fun)
    else:
        arr = fun(arr)
    return arr


###################################################################################
# УСТАНОВЛЕН ЛИ ПАКЕТ
###################################################################################
# import pip
# if pip.__version__ >= "10.0.0": from pip._internal.utils.misc import get_installed_distributions
# else:                           from pip                      import get_installed_distributions
# def packageValid(nam):
#     list_packages = get_installed_distributions()
#     flat_packages = [item.project_name for item in list_packages]
#     return (nam in flat_packages)


#==================================================================================
#======   УДАЛЕНИЕ ДУБЛИКАТОВ В МАССИВЕ   =========================================
#==================================================================================
def lstUnique(lst):
    seen = set()
    return list(zip(*[(x, seen.add(x)) for x in lst if x not in seen]))[0]

#==================================================================================
#======   УДАЛЕНИЕ ЭЛЕМЕНТА В КОПИИ СПИСКА   ======================================
#==================================================================================
def dictRemoveKey(dic, key):
    dictNew = dict(dic)
    del dictNew[key]
    return dictNew

#==================================================================================
#======    ДАТА/ВРЕМЯ В TS   ======================================================
#==================================================================================
datetimeToTs      = lambda dat: datetime.datetime.timestamp(dat)

#==================================================================================
#======   УДАЛИТЬ СЕКУНДЫ   =======================================================
#==================================================================================
datetimeCutSecond = lambda dat: datetime.datetime(dat.year, dat.month, dat.day, dat.hour, dat.minute, 0)

#==================================================================================
#======   СТРОКУ В ДАТА/ВРЕМЯ   ===================================================
#==================================================================================
strToDatetime     = lambda val: datetime.datetime.strptime(val, '%Y-%m-%d %H:%M')
strAllToDatetime  = lambda val: parse(val)

#==================================================================================
#======    ДАТА/ВРЕМЯ В СТРОКУ   ==================================================
#==================================================================================
datetimeToStr     = lambda dat: sqlDateTime(datetimeToTs(dat))

#==================================================================================
#======   ДАТА ДЛЯ ПОЛЯ SQL DATETIME: '2016-12-16 9:21'   =========================
#==================================================================================
sqlDateTime       = lambda timestamp: datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

#==================================================================================
#======   ДАТА ДЛЯ ПОЛЯ SQL DATETIME: '2016-12-16'   ==============================
#==================================================================================
sqlDate          = lambda timestamp: datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

#==================================================================================
#======   ДАТА ДЛЯ ПОЛЯ SQL DATETIME: '9:21'   ====================================
#==================================================================================
sqlTime          = lambda timestamp: datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M')

#==================================================================================
#======   YYYYMMDD (INT) TO TIMESTAMP+UTC (INT)  ==================================
#==================================================================================
def yyyymmddToTs(val):
    s   = str(val)
    dat = datetime.datetime(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    return int(dat.timestamp())


#==================================================================================
#======   ТЕКУЩИЙ TIMESTAMP ДЛЯ (GMT+UTC)   =======================================
#==================================================================================
def tsNowUTC():
    now_time = datetime.datetime.now().replace(tzinfo=pytz.utc)
    return int(datetime.datetime.timestamp(now_time))


#==================================================================================
#======   ТЕКУЩИЙ TIMESTAMP ДЛЯ GMT         =======================================
#==================================================================================
def tsNow():
    now_time = datetime.datetime.now()
    return int(datetime.datetime.timestamp(now_time))


#==================================================================================
#======   ДАТА В ФОРМАТЕ SQL В TIMESTAMP   ========================================
#==================================================================================
def tsDate(sqlDateTime):
    dat = datetime.datetime(int(sqlDateTime[0:4]), int(sqlDateTime[5:7]), int(sqlDateTime[8:10]))
    return int(dat.timestamp())
def tsDateTime(sqlDateTime):
    ln  = len(sqlDateTime)
    dat = datetime.datetime(
        int(sqlDateTime[0:4]),
        int(sqlDateTime[5:7]),
        int(sqlDateTime[8:10]),
        int(sqlDateTime[11:13] if ln>=13 else 0),
        int(sqlDateTime[14:16] if ln>=16 else 0)
    )
    return int(dat.timestamp())


#==================================================================================
#======   TIMESTAMP В ДНИ, ЧАСЫ, МИНУТЫ   =========================================
#==================================================================================
tsToMonth   = lambda timestamp: datetime.datetime.fromtimestamp(timestamp).strftime('%m')
tsToDays    = lambda timestamp: datetime.datetime.fromtimestamp(timestamp).strftime('%d')
tsToHours   = lambda timestamp: datetime.datetime.fromtimestamp(timestamp).strftime('%H')
tsToMinutes = lambda timestamp: datetime.datetime.fromtimestamp(timestamp).strftime('%M')


#==================================================================================
#======   TIMESTAMP НА НАЧАЛО ДНЯ, МЕСЯЦА, ГОДА   =================================
#==================================================================================
tsStartDay   = lambda timestamp: int(datetime.datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=0, hour=0).timestamp())
tsStartMonth = lambda timestamp: int(datetime.datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=0, hour=0, day=1).timestamp())
tsStartYear  = lambda timestamp: int(datetime.datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=0, hour=0, day=1, month=1).timestamp())


#==================================================================================
#======   TIMESTAMP ЗАМЕНИТЬ ВРЕМЯ   ==============================================
#==================================================================================
tsSetTime    = lambda timestamp, hour=0, minute=0: int(datetime.datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=minute, hour=hour).timestamp())


#==================================================================================
#======   АНАЛИЗАТОР РАСПИСАНИЯ-ТАЙМИНГА   ========================================
#==================================================================================
# mask = '*/2' - каждый второй
# valNow, valMax - str или int
#==================================================================================
def cmpTiming(mask, valNow, valMax):
    TIMING_ALL = '*'
    if mask==TIMING_ALL: return True                                    # mask = '*'
    maskLst = mask.replace(' ', '').split('/')                          # maskLst = ['*', '2']
    if str(maskLst[0]).isdigit() and str(valNow).isdigit():
        if int(maskLst[0])==int(valNow): return True                    # mask = val
    if (maskLst[0]==TIMING_ALL) and (len(maskLst)==2):                  # mask = '*/2'

        # переменные в числа
        if isinstance(maskLst[1], str) and (not str(maskLst[1]).isdigit()): raise Exception('maskLst[1] не число: "'+maskLst[1]+'"')
        if isinstance(valNow,     str) and (not str(valNow    ).isdigit()): raise Exception('valNow не число: "'+valNow+'"')
        if isinstance(valMax,     str) and (not str(valMax    ).isdigit()): raise Exception('valMax не число: "'+valMax+'"')
        maskLst[1] = int(maskLst[1])
        valNow     = int(valNow)
        valMax     = int(valMax)

        # проверка допустимых значений
        ret = False
        val = 0 if (valMax in [23, 59]) else 1
        while (val<valMax) and (not ret):
            ret = (val==valNow)
            val += maskLst[1]
        return ret

    else:
        return False


#==================================================================================
#======   ТЕКУЩEE ВРЕМЯ    ========================================================
#==================================================================================
sqlDateTimeNow = lambda: sqlDateTime(tsNow())
datetimeNow    = lambda: datetime.datetime.now()
strUnique      = lambda: datetime.datetime.now().strftime('%y%m%d%H%M%S%f')


#==================================================================================
#======   UTC В СЕКУНДАХ    =======================================================
#==================================================================================
getUTC         = lambda: -time.timezone if (time.localtime().tm_isdst == 0) else -time.altzone




#==================================================================================
#======   RUN SCRYPT    ===========================================================
#==================================================================================
def scryptExec(cmd):
    try:
        logger.debug('Скрипт: '+cmd)
        ret = False
        val = ''
        val = subprocess.check_output(cmd, shell=True).strip().decode('utf-8')
        ret = True
    except subprocess.CalledProcessError as e: val = 'Проблема выполнения '+str(e)
    except Exception as e:                     val = str(e)
    finally:
        if val!='': logger.info(val)
        return ret, val



#==================================================================================
#======   ХЭШ MD5 (128-bit, 16-byte, 32-char) =====================================
#==================================================================================
#======   1% вероятности 1 коллизии при 2.6х10**18 записях  =======================
#==================================================================================
def getMD5(text):
    m = hashlib.md5()
    m.update(bytes(text, "UTF-8"))
    return m.hexdigest()


#==================================================================================
#======   ХЭШ SHA512 (256-bit, 32-byte, 64-char) ==================================
#==================================================================================
#======   1% вероятности 1 коллизии при 4.8х10**37 записях  =======================
#==================================================================================
def getSHA256(text):
    m = hashlib.sha256()
    m.update(bytes(text, "UTF-8"))
    return m.hexdigest()


#==================================================================================
#   КОНТРОЛЬ ПЕРИОДОВ
#==================================================================================
#    [возвращаемое значение], [[даты возврата значения], [часы возврата значения]]
#    arrIni = [[[1440,  False], [[-1], [-1]]],                              # сутки
#              [[1440,  True ], [[-1], [1]]],                               # сутки
#              [[4320,  False], [[-1], [5, 13, 20]]],                       # 3 суток
#              [[43200, True ], [[4, 7, 10, 13, 19, 22, 25, 28], [1]]],     # 30 суток
#              [[86400, True ], [[1, 16], [1]]]]                            # 60 суток
#==================================================================================
class Periods:
    def __init__(self, arrIni, valEmpty):
        self.clearDay = -1            # день, в котором проведена последняя очистка
        self.arr      = {}            # "day.hour" = [val, False]   "-1.-1" = [[1440, False], False]
        for item in arrIni:
            for itemDay in item[1][0]:
                for itemHour in item[1][1]:
                    self.arr[self.key(itemDay, itemHour)] = [item[0], False]

    def __del__(self):
        self.arr = None

    key = lambda self, day, hour: str(day)+'.'+str(hour)

    def getVal(self):
        def _get_(day, hour):
            ret = self.arr.get(self.key(day, hour), None)
            if ret != None:
                if self.arr[self.key(day, hour)][1]: ret = None    # если признак установлен, значение не читаем
                else:
                    self.arr[self.key(day, hour)][1] = True        # иначе устанавливаем признак и возвращаем значение
                    ret = ret[0]
            return ret

        now = datetime.datetime.now()

        # очистка признаков использования
        if now.day != self.clearDay:
            self.clearDay = now.day
            for item in self.arr: self.arr[item][1] = False

        # чтение значения
        val = _get_(now.day, now.hour)
        if val == None: val = _get_(-1, now.hour)
        if val == None:
            val = self.arr.get(self.key(-1, -1), None)
            if val != None: val = val[0]
        return val if val != None else valEmpty



#==================================================================================
#   ОЧЕРЕДЬ
#==================================================================================
class Queue:
    def __init__(self, maxSize):
        self.items   = []      # очередь
        self.maxSize = maxSize # максимальное количество записей в очереди

    def __del__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def isFull(self):
        return self.size() >= self.maxSize

    def push(self, item):
        self.items.insert(0, copy.deepcopy(item))

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
