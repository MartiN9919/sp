# -*- coding: utf-8 -*-

import time
from fun.funConst import PHONE_LIST, PHONE_ACCOUNT
from fun.funSys   import logger, sqlDateTime, tsNow
from fun.funBD    import bdConnect, bdDisconnect, bdSQL



#####################################################
# РАБОТА С ТАБЛИЦАМИ PHONE_... (НЕ ФОНОВО)
#####################################################
class PhoneWriter():

    #####################################################
    # КОНСТРУКТОР
    #####################################################
    def __init__(self):
        self.db = bdConnect()


    #####################################################
    # ПСЕВДО-ДЕСТРУКТОР
    #####################################################
    def free(self):
        bdDisconnect(self.db)



    #####################################################
    # ПОЛУЧИТЬ СПИСОК ТЕЛЕФОНОВ
    #####################################################
    def getPhoneList(self, host):
        sql = \
            "SELECT "+PHONE_LIST.PHONE+" "+ \
            "FROM "  +PHONE_LIST.TABLE+" "+ \
            "WHERE " +PHONE_LIST.ENABLED_HOST[host]+"=1;"
        return bdSQL(sql, True, True, self.db)



    #####################################################
    # УСТАНОВИТЬ ДОСТУПНОСТЬ ТЕЛЕФОНА
    #####################################################
    # phone = '+xxxxxxxxxx'
    #####################################################
    def setPhoneEnabled(self, host, phone, enabled=0):
        sql = \
            "UPDATE IGNORE "+PHONE_LIST.TABLE+" "+ \
            "SET "   + PHONE_LIST.ENABLED_HOST[host]+"="+str(enabled)+" "+ \
            "WHERE " + PHONE_LIST.PHONE+"='"+phone+"';"
        bdSQL(sql, True, False, self.db)



    #####################################################
    # ДОБАВИТЬ/ОБНОВИТЬ АККАУНТ
    #####################################################
    # phone = '+xxxxxxxxxx'
    #####################################################
    def addPhoneAccount(self, host, id, phone, name, name_visible, url):
        refresh = sqlDateTime(tsNow())
        sql = \
            "UPDATE IGNORE "+PHONE_ACCOUNT.TABLE+" "+ \
            "SET "+ \
                PHONE_ACCOUNT.NAME         + "='"+name        +"', "+ \
                PHONE_ACCOUNT.NAME_VISIBLE + "='"+name_visible+"', "+ \
                PHONE_ACCOUNT.URL          + "='"+url         +"', "+ \
                PHONE_ACCOUNT.REFRESH      + "='"+refresh     +"' " + \
            "WHERE " + \
                "("+PHONE_ACCOUNT.HOST     + "='"+host   +"') AND "+ \
                "("+PHONE_ACCOUNT.ID       + "='"+str(id)+"') AND "+ \
                "("+PHONE_ACCOUNT.PHONE    + "='"+phone  +"'); "+\
            "INSERT IGNORE INTO " + \
                PHONE_ACCOUNT.TABLE        + " (" + \
                PHONE_ACCOUNT.HOST         + ", " + \
                PHONE_ACCOUNT.ID           + ", " + \
                PHONE_ACCOUNT.PHONE        + ", " + \
                PHONE_ACCOUNT.NAME         + ", " + \
                PHONE_ACCOUNT.NAME_VISIBLE + ", " + \
                PHONE_ACCOUNT.URL          + ", " + \
                PHONE_ACCOUNT.REFRESH      + ") " + \
            "VALUES ("+ \
                "'"+host         + "', "+ \
                "'"+str(id)      + "', "+ \
                "'"+phone        + "', "+ \
                "'"+name         + "', "+ \
                "'"+name_visible +"', "+ \
                "'"+url          + "', "+ \
                "'"+refresh      + "');"
        bdSQL(sql, True, False, self.db)
