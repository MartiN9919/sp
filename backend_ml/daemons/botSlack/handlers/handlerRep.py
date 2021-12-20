# -*- coding: utf-8 -*-

from   daemonIni     import DAEMON_INI
from   fun.funConst  import REP_TYPE
from   fun.funSys    import logger, logError
from   fun.funBDRep  import getRepType, setRepTypeStartOnce


#####################################################
# ОТЧЕТ: СОЗДАТЬ
#####################################################
def handlerRepCreate(channelID, args):
    if len(args) != 1: return {'text': '*Неверная команда: должен быть ОДИН аргумент!*'}

    try:
        key = args[0]
        if key == '?':
            ret = ''
            for item in getRepType(worker=DAEMON_INI.WORKER):
                ret += (item[REP_TYPE.ID]+' - _'+item[REP_TYPE.DESCRIPT]+'_\n')
            if ret != '': ret = '*Доступные отчеты:*\n'+ret+'\n'
            else:         ret = '*Доступных отчетов НЕ ОБНАРУЖЕНО!*\n'

        elif key.isdigit():
            nam = ''
            for item in getRepType(worker=DAEMON_INI.WORKER):
                if key == item[REP_TYPE.ID]:
                    nam = item[REP_TYPE.DESCRIPT]
                    break

            if nam != '':
                setRepTypeStartOnce(id=key, flag=True)
                logger.info('OK! Отчет ['+key+']')
                ret = DAEMON_INI.ICO_OK+' *Запрос на отчет ['+key+' - _'+nam+'_] отправлен. Ждите его подготовки.*'
            else:
                ret = DAEMON_INI.ICO_ERROR+' *Отчет ['+key+'] не найден!*'

        else:
            ret = '*Неверная команда: аргумент должен быть числом или знаком "?"*'

    except Exception as e:
        logger.error(str(e))
        ret = DAEMON_INI.ICO_ERROR+' *Ошибка отчета ['+key+']*'
    finally:
        return {'text': ret}
