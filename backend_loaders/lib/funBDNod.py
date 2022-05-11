# -*- coding: utf-8 -*-

import time, lib.funBD
from lib.funConst import NOD



#==================================================================================
#   КЭШ ОБЪЕКТОВ ИНТРЕСА
#==================================================================================
#   refreshDelay - время хранения кэша, в секундах
#==================================================================================
class Nod:
    def __init__(self, refreshDelay = 60):
        self.refreshDelay = refreshDelay
        self.refreshTime  = time.time()-1
        self._refresh()

    def _refresh(self):
        if (self.refreshTime > time.time()): return
        self.nArr = lib.funBD.nodArrGet()
        self.nVal = lib.funBD.nodValGet()

        self.refreshTime = time.time()+self.refreshDelay

    def _get_arr(self):
        self._refresh()
        return self.nArr
    def _get_val(self):
        self._refresh()
        return self.nVal

    arr = property(_get_arr)
    val = property(_get_val)                            # все поисковые условия в одну строку

nodHash = Nod(60)



def getNodFields(sqlFields, sqlWhere=''):
    sql = "SELECT "+sqlFields+" "+ \
          "FROM "  +NOD.TABLE+" "+ \
          "WHERE ("+NOD.ENABLED+"=1) "+(("AND ("+sqlWhere+") ") if sqlWhere!="" else "") + \
          ";"
    return fun.funBD.bdSQL(sql, True, True)
