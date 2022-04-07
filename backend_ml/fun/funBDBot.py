# -*- coding: utf-8 -*-

from   fun.funConst     import BD, BOT_TYPE, BOT, MON_TYPE
from   fun.funSys       import tsNow, sqlDateTime
from   fun.funBD        import bdSQL



#===========================================================================================
# BOT_TYPE: получить список активных записей + поля из связанной таблицы MON_TYPE
#===========================================================================================
# fieldList - список возвращаемых полей [...] TABLE.FIELD
#===========================================================================================
def botTypeGet(worker, fieldList, bd=-1):
    ## при необходимости добавить названия таблиц
    for ind, item in enumerate(fieldList):
        if item.find(BD.DB+'.')==0: continue
        if item.find('.')!=-1: continue
        fieldList[ind]=BOT_TYPE.TABLE+'.'+fieldList[ind]

    sql = \
        "SELECT "+ ', '.join(fieldList) +" " \
        "FROM "  + BOT_TYPE.TABLE+" INNER JOIN "+MON_TYPE.TABLE+" "+ \
        "ON "+BOT_TYPE.TABLE+'.'+BOT_TYPE.MON_TYPE_ID+"="+MON_TYPE.TABLE+'.'+MON_TYPE.ID+" "+ \
        "WHERE " + \
            BOT_TYPE.TABLE+'.'+BOT_TYPE.WORKER +"='"+worker+"' AND "+ \
            BOT_TYPE.TABLE+'.'+BOT_TYPE.ENABLED+"=1 AND "+ \
            MON_TYPE.TABLE+'.'+MON_TYPE.ENABLED+"=1 "+ \
        "ORDER BY "+BOT_TYPE.TABLE+'.'+BOT_TYPE.SORT+" ASC"
    return bdSQL(sql, True, True, bd)


#===========================================================================================
# BOT_TYPE CONTROL: добавить запись-контроль
#===========================================================================================
def botTypeControlAdd(channelID, mon_type_id_title, mon_type_id_content, nam, descript=''):
    botTypeControlDescriptTitle   = lambda nam: 'Темы: КОНТРОЛЬ ['      +nam[:255]+']'
    botTypeControlDescriptContent = lambda nam: 'Публикации: КОНТРОЛЬ ['+nam[:255]+']'
    setSQL = lambda dat: \
        "INSERT IGNORE INTO " + \
            BOT_TYPE.TABLE             + " (" + \
                BOT_TYPE.MON_TYPE_ID   + ", " + \
                BOT_TYPE.WORKER        + ", " + \
                BOT_TYPE.SORT          + ", " + \
                BOT_TYPE.CHANNEL_SLACK + ", " + \
                BOT_TYPE.TITLE_VAL     + ", " + \
                BOT_TYPE.TITLE_NAM     + ", " + \
                BOT_TYPE.VAL_SORT      + ", " + \
                BOT_TYPE.VAL_MIN       + ", " + \
                BOT_TYPE.VAL_RISE      + ", " + \
                BOT_TYPE.VAL_FRESH     + ", " + \
                BOT_TYPE.VAL_TOP       + ", " + \
                BOT_TYPE.ENABLED       + ", " + \
                BOT_TYPE.DESCRIPT      + ", " + \
                BOT_TYPE.REFRESH       + ") " + \
        "VALUES ("          + \
                dat[BOT_TYPE.MON_TYPE_ID]   + ", "  + \
            "'"+dat[BOT_TYPE.WORKER]        + "', " + \
                dat[BOT_TYPE.SORT]          + ", "  + \
            "'"+dat[BOT_TYPE.CHANNEL_SLACK] + "', " + \
            "'"+dat[BOT_TYPE.TITLE_VAL]     + "', " + \
            "'"+dat[BOT_TYPE.TITLE_NAM]     + "', " + \
                dat[BOT_TYPE.VAL_SORT]      + ", "  + \
                dat[BOT_TYPE.VAL_MIN]       + ", "  + \
                dat[BOT_TYPE.VAL_RISE]      + ", "  + \
                dat[BOT_TYPE.VAL_FRESH]     + ", "  + \
                dat[BOT_TYPE.VAL_TOP]       + ", "  + \
                dat[BOT_TYPE.ENABLED]       + ", "  + \
            "'"+dat[BOT_TYPE.DESCRIPT]      + "', " + \
            "'"+dat[BOT_TYPE.REFRESH]       + "' "  + \
        ")"

    # добавить BOT_TYPE title_name
    dat = {
        BOT_TYPE.MON_TYPE_ID:   mon_type_id_title,
        BOT_TYPE.WORKER:        BOT_TYPE.WORKER_STANDART,
        BOT_TYPE.SORT:          BOT_TYPE.SORT_AUTO,
        BOT_TYPE.CHANNEL_SLACK: channelID,
        BOT_TYPE.TITLE_VAL:     nam,
        BOT_TYPE.TITLE_NAM:     '[title]',
        BOT_TYPE.VAL_SORT:      '0',
        BOT_TYPE.VAL_MIN:       '0',
        BOT_TYPE.VAL_RISE:      '0',
        BOT_TYPE.VAL_FRESH:     '0',
        BOT_TYPE.VAL_TOP:       '0',
        BOT_TYPE.ENABLED:       '1',
        BOT_TYPE.DESCRIPT:      botTypeControlDescriptTitle(nam)+' '+descript,
        BOT_TYPE.REFRESH:       sqlDateTime(tsNow()),
    }
    retTitle = botTypeControlGetID(dat[BOT_TYPE.TITLE_VAL], dat[BOT_TYPE.TITLE_NAM])
    if retTitle == '-1':
        bdSQL(setSQL(dat), True, False)
        retTitle = botTypeControlGetID(dat[BOT_TYPE.TITLE_VAL], dat[BOT_TYPE.TITLE_NAM])

    # добавить BOT_TYPE content
    dat[BOT_TYPE.MON_TYPE_ID] = mon_type_id_content
    dat[BOT_TYPE.TITLE_NAM]   = '[content]'
    dat[BOT_TYPE.DESCRIPT]    = botTypeControlDescriptContent(nam)+' '+descript
    retContent = botTypeControlGetID(dat[BOT_TYPE.TITLE_VAL], dat[BOT_TYPE.TITLE_NAM])
    if retContent == '-1':
        bdSQL(setSQL(dat), True, False)
        retContent = botTypeControlGetID(dat[BOT_TYPE.TITLE_VAL], dat[BOT_TYPE.TITLE_NAM])

    return retTitle, retContent



#===========================================================================================
# BOT_TYPE CONTROL: получить id записи-контроля
#===========================================================================================
def botTypeControlGetID(title_val, title_nam):
    sql = \
        "SELECT " + BOT_TYPE.ID    + " " + \
        "FROM "   + BOT_TYPE.TABLE + " " + \
        "WHERE "  + \
            BOT_TYPE.TITLE_VAL   + "='"  + title_val + "' AND " + \
            BOT_TYPE.TITLE_NAM   + "='"  + title_nam + "' AND " + \
            BOT_TYPE.ENABLED + "=1 " + \
        "LIMIT 1"
    rec = bdSQL(sql, True, True)
    return str(rec[0][0] if len(rec) > 0 else -1)


# НЕ НУЖНО, ТАК КАК ТАБЛИЦЫ СВЯЗАННЫЕ: def botTypeControlVerify(val, nam):





#===========================================================================================
# BOT SLACK: получить записи, связанные с bot_type_id
#===========================================================================================
# fieldList - список имен возвращаемых полей [...]
#===========================================================================================
def botSlackGet(bot_type_id, fieldList, bd=-1):
    sql = \
        "SELECT "+ ', '.join(fieldList) +" " \
        "FROM "  + BOT.TABLE+" " + \
        "WHERE " + \
            BOT.BOT_TYPE_ID + "="   + str(bot_type_id) + " AND " + \
            BOT.SHOW_SLACK  + "=0 " + \
        "ORDER BY "+BOT.REFRESH +" ASC"
    return bdSQL(sql, True, True, bd)


#===========================================================================================
# BOT SLACK: отметить запись отображенная
#===========================================================================================
def botSlackMark(bot_id, bot_ts='', bd=-1):
    sql = \
        "UPDATE IGNORE "+ BOT.TABLE+" "+ \
        "SET "+ \
            BOT.SHOW_SLACK + "=1, " + \
            BOT.SLACK_TS   + "=\'"+str(bot_ts).replace("\'", "\"")+"\' "+ \
        "WHERE "+BOT.ID+"="+str(bot_id)
    bdSQL(sql, True, False, bd)




#===========================================================================================
# BOT: добавить запись
#===========================================================================================
def botAdd(rec):
    dat = {
        BOT.BOT_TYPE_ID: rec[BOT.BOT_TYPE_ID],
        BOT.HOST:        rec[BOT.HOST][:32],
        BOT.MSG_VAL:     rec[BOT.MSG_VAL][:255],
        BOT.MSG_NAM:     rec[BOT.MSG_NAM][:255],
        BOT.URL:         rec[BOT.URL][:255],
        BOT.DATE:        str(rec[BOT.DATE]),
        BOT.REFRESH:     str(tsNow()),
    }

    sql = \
        "INSERT IGNORE INTO " + \
            BOT.TABLE           + " (" + \
                BOT.BOT_TYPE_ID + ", " + \
                BOT.HOST        + ", " + \
                BOT.MSG_VAL     + ", " + \
                BOT.MSG_NAM     + ", " + \
                BOT.URL         + ", " + \
                BOT.DATE        + ", " + \
                BOT.REFRESH     + ") " + \
        "VALUES ("          + \
            dat[BOT.BOT_TYPE_ID] + ", "  + \
            "'"+dat[BOT.HOST]        + "', " + \
            "'"+dat[BOT.MSG_VAL]     + "', " + \
            "'"+dat[BOT.MSG_NAM]     + "', " + \
            "'"+dat[BOT.URL]         + "', " + \
                dat[BOT.DATE]        + ", "  + \
                dat[BOT.REFRESH]     + \
        ")"
    bdSQL(sql, True, False)

    # работает, но отсутствует необходимость + вопрос с BOT.REFRESH
    #sql = \
    #    "UPDATE IGNORE "  + BOT.TABLE   + " " + \
    #    "SET "            + BOT.REFRESH + "=" + str(tsNow()) + " "  + \
    #    "WHERE "+ \
    #        BOT.BOT_TYPE_ID + "="  + dat[BOT.BOT_TYPE_ID] + " AND "   + \
    #        BOT.HOST        + "='" + dat[BOT.HOST]        + "' AND " + \
    #        BOT.MSG_VAL     + "='" + dat[BOT.MSG_VAL]     + "' AND "  + \
    #        BOT.MSG_NAM     + "='" + dat[BOT.MSG_NAM]     + "' AND "  + \
    #        BOT.URL         + "='" + dat[BOT.URL]         + "' AND " + \
    #        BOT.DATE        + "="  + dat[BOT.DATE]        + " AND "  + \
    #        BOT.REFRESH     + "="  + dat[BOT.REFRESH]     + ";"
    #bdSQL(sql, True, False)



#===========================================================================================
# BOT: удалить старые записи
#===========================================================================================
# remember - время запоминания опубликованных сообщений, сек.
#===========================================================================================
def botDel(remember):
    sql = \
        "DELETE "+ \
        "FROM " + BOT.TABLE   + " " + \
        "WHERE "+ BOT.REFRESH + "<" + str(tsNow()-remember) + ";"
    bdSQL(sql, True, False)
