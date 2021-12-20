# -*- coding: utf-8 -*-

from   daemonIni     import DAEMON_INI
from   fun.funSys    import logger, logError
from   fun.funBDMon  import monTypeControlAdd, monTypeControlDel, monTypeControlVerify
from   fun.funBDBot  import botTypeControlAdd


#####################################################
# МОНИТОРИНГ: ДОБАВИТЬ
#####################################################
def handlerMonAdd(channelID, args):
    if len(args) == 0: return {'text': '*Неверная команда: нет аргументов!*'}

    val = ' '.join(args).replace('"', "'")
    nam = val.split('|')
    nam = nam[0].replace("'", '').replace('(', '').replace(')', '').replace('~', '')
    try:
        if monTypeControlVerify(nam):
            ret = DAEMON_INI.ICO_ERROR+' Контроль ['+nam+'] уже существует!'
        else:
            monIDTitle, monIDContent = monTypeControlAdd(nam, val, 'Создано в Slack')                                  # создать MON_TYPE
            botIDTitle, botIDContent = botTypeControlAdd(channelID, monIDTitle, monIDContent, nam, 'Создано в Slack')  # создать BOT_TYPE
            logger.info( \
                'Контроль: ['+nam+'] в канал '+channelID+'. '+ \
                'MON_TYPE: '+monIDTitle+', '+monIDContent+' '+ \
                'BOT_TYPE: '+botIDTitle+', '+botIDContent
            )
            ret = DAEMON_INI.ICO_OK+' Контроль ['+nam+'] установлен'
    except Exception as e:
        logger.error(str(e))
        ret = DAEMON_INI.ICO_ERROR+' Ошибка постановки на контроль ['+nam+']'
    finally:
        return {'text': '*'+ret+'*'}



#####################################################
# МОНИТОРИНГ: УДАЛИТЬ
#####################################################
def handlerMonDel(channelID, args):
    if len(args) != 1: return {'text': '*Неверная команда: должен быть один аргумент!*'}

    val = ' '.join(args).replace('"', "'")
    nam = val.split('|')
    nam = nam[0].replace("'", '').replace('(', '').replace(')', '').replace('~', '')
    try:
        if not monTypeControlVerify(nam):
            ret = DAEMON_INI.ICO_ERROR+' Контроль ['+nam+'] не существует!'
        else:
            monTypeControlDel(nam)
            if not monTypeControlVerify(nam): ret = DAEMON_INI.ICO_OK    + ' Контроль ['+nam+'] удален'
            else:                             ret = DAEMON_INI.ICO_ERROR + ' Ошибка удаления с контроля ['+nam+']'
    except Exception as e:
        logger.error(str(e))
        ret = DAEMON_INI.ICO_ERROR+' Ошибка удаления с контроля ['+nam+']'
    finally:
        return {'text': '*'+ret+'*'}
