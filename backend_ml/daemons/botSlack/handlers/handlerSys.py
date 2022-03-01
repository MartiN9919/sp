# -*- coding: utf-8 -*-

import os.path, subprocess
from   daemonIni     import DAEMON_INI
from   fun.funSys    import scryptExec


#####################################################
# LOG
#####################################################
def handlerSysLog(channelID, args):
    valVerify = valContent = ''
    for fname in DAEMON_INI.VERIFY_FILES:
        if not os.path.exists(fname):
            (dirName, fileName) = os.path.split(fname)
            valVerify+='\n:exclamation:*'+fileName+'*: отсутствует'
    if valVerify != '': valVerify += '\n'

    count = (3 if len(args)==0 else int(args[0]))*(-1)

    for fname in DAEMON_INI.CONTENT_FILES:
        (dirName, fileName) = os.path.split(fname)
        val=' *'+fileName+'*:'
        if not os.path.exists(fname):
            valContent+='\n:exclamation:'+val+' отсутствует'
            continue

        with open(fname, 'r', encoding='utf8', errors='ignore') as f:
            f.seek (0, 2)                       # Seek @ EOF
            fsize = f.tell()                    # Get Size
            f.seek (max (fsize-1024, 0), 0)     # Set pos @ last n chars
            lines = f.readlines()               # Read to end
        linesEnd = lines[count:]                # Get last lines

        i=0
        for s in linesEnd:
            linesEnd[i] = '_'+s.rstrip()+'_\n'  # курсив   s.decode("utf-8").rstrip()
            i+=1

        valContent+='\n:gear:'+val+'\n'+''.join(linesEnd)

    ret = (valVerify + valContent).strip()
    return {'text': '*Состояние:*\n'+ret}



#####################################################
# EXEC
#####################################################
def handlerSysExecStart  (channelID, args): return handlerSysExec(['start'  ]+args)
def handlerSysExecStop   (channelID, args): return handlerSysExec(['stop'   ]+args)
def handlerSysExecRestart(channelID, args): return handlerSysExec(['restart']+args)
def handlerSysExecVerify (channelID, args): return handlerSysExec(['verify' ]+args)
def handlerSysExec(args):
    if len(args)>0:
        cmd = '/etc/init.d/atlas'
        if len(args)>=2:
            if args[1]=='mlServerText':
                cmd = '/etc/init.d/atlasML'
        _, msg = scryptExec(cmd+' '+args[0].lower()+((' '+args[1]) if len(args)>=2 else ''))
        return {'text': msg}
    else: return {'text': DAEMON_INI.ICO_ERROR+' Использование: *_exec start|stop|restart|verify loaderVK|..._*'}


