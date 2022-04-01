# -*- coding: utf-8 -*-

from   daemonIni     import DAEMON_INI

def handlerHelp(channelID, args):
    ret = \
        '*Формат сообщения:*\n'+ \
        '[Значение] > [Параметр]\n'+\
        '    значение = N - текущее значение параметра\n'+ \
        '    значение = N1..N2 изменение параметра ЗА ЧАС (если не указано иное)\n'+ \
        '    значение в некоторых случаях может отсутствовать\n\n'+ \
        '    параметр = содержимое публикациии, название темы, группы или иное сообщение\n'+ \
        '    (ссылки и нетекстовые элементы не отображаются)\n\n'+ \
        'Для получения детальной информации о сообщениях используйте закладку _"Мониторинг"_ на сайте системы\n\n'+ \
        '*Условные обозначения:*\n'
    for item in DAEMON_INI.ICO_LIST: ret+=DAEMON_INI.ICO_LIST[item][0]+'\t- '+DAEMON_INI.ICO_LIST[item][1]+'\n'
    ret+='\n*Контроль:*\n(контроль[+][-] или control[+][-]) название контроля-поисковая строка1|[поисковая строка N]\n'
    ret+='\n*Отчет:*\n(отчет или report) код отчета\n'
    ret+='\n*Информация:*\n(инфо или info)\n'
    ret+='\n*Логи работы системы:*\n(лог или log) [количество строк]\n'
    return {'text': ret}
