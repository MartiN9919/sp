# -*- coding: utf-8 -*-

from fun.funConst  import IARC, EMO
from fun.funBD     import bdSQL
from fun.funSphinx import sphinxSQL


# из atlas.emo
try:                   LEMO_ = bdSQL('SELECT '+EMO.LEX+', '+EMO.WEIGHT+' FROM '+EMO.TABLE+';', True, True)
except Exception as e: LEMO_ = []
LEMO = {}
for item in LEMO_: LEMO[item[0]] = item[1]
if len(LEMO) == 0: print("Нет данных для определения эмоций")


#####################################################
# EMO: эмоции текста
#####################################################
def emo(text):
    # список нормализованных слов
    LNORM = sphinxSQL("CALL KEYWORDS('"+text+"', '"+IARC.TABLE_MAIN+"')", True)
    LNORM = list(map(lambda x: x[2], LNORM))

    # сумма весов
    ip = im = 0
    for norm in LNORM:
        i = LEMO.get(norm, 0)
        if i == -1: continue
        if i > 0: ip += i
        else:     im -= i

    # соотношение
    ret = 0
    if im == 0:
        if ip > 2: ret = 1
    else:
        d = ip / im
        if d > 1.3:  ret =  1
        if d < 0.01: ret = -1

    return ret
