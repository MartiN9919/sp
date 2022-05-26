# -*- coding: utf-8 -*-
from   daemonIni import DAEMON_INI, runPointer
import sys, os, time, atexit
from   signal import SIGTERM
import logging, logging.handlers

logger = logging.getLogger()
logger.setLevel(logging.INFO)
filehandler = logging.handlers.TimedRotatingFileHandler(DAEMON_INI.FILE_LOG, when='midnight', interval=1, backupCount=10)
filehandler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(filehandler)



############################################################
# Subclass Daemon class and override the run() method
############################################################
class Daemon(object):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr="/dev/null"):
        self.stdin   = stdin
        self.stdout  = stdout
        self.stderr  = stderr
        self.pidfile = pidfile



    ############################################################
    # Deamonize
    ############################################################
    def daemonize(self):
        # Первое ветвление (first fork)
        try:
            pid = os.fork()
            if pid > 0: sys.exit(0)  # если родитель - выход
        except OSError as e:
            message = "Fork #1 failed: {}\n".format(e)
            sys.stderr.write(message)
            sys.exit(1)

        # Отвязка от родительской среды
        os.chdir("/")   # рабочий каталог
        os.setsid()     # новый сеанс
        os.umask(0)

        # Второе ветвление (second fork)
        try:
            pid = os.fork()
            if pid > 0: sys.exit(0)
        except OSError as e:
            message = "Fork #2 failed: {}\n".format(e)
            sys.stderr.write(message)
            sys.exit(1)

        message = 'Демон (PID: {}) запущен'.format(os.getpid())
        logger.info(message)
        print(message)

        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # Запись PID-файла
        pid = str(os.getpid())
        open(self.pidfile,'w+').write("{}\n".format(pid))

        # Register a function to clean up
        atexit.register(self.delpid)

    def delpid(self):
        os.remove(self.pidfile)


    ############################################################
    #   DAEMON: START
    ############################################################
    def start(self):
        # Проверка PID-aайла чтобы узнать запущен ли ранее процесс
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "Файл {} существует. Демон уже запущен?\n".format(self.pidfile)
            sys.stderr.write(message)
            sys.exit(1)

        # Start daemon
        self.daemonize()
        self.run()


    ############################################################
    #   DAEMON: STATUS
    ############################################################
    def status(self):
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            message = "Нет PID-файла. Демон не запущен?\n"
            sys.stderr.write(message)
            sys.exit(1)

        try:
            procfile = open("/proc/{}/status".format(pid), 'r')
            procfile.close()
            message = "Процесс с PID {}\n".format(pid)
            sys.stdout.write(message)
        except IOError:
            message = "Нет процесса с PID {}\n".format(self.pidfile)
            sys.stdout.write(message)



    ############################################################
    #   DAEMON: STOP
    ############################################################
    def stop(self):
        # Получение PID из файла
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError as e:
            message = str(e) + "\nДемон не запущен?\n"
            sys.stderr.write(message)
            sys.exit(1)

        # Удаление демона
        try:
            os.kill(pid, SIGTERM)
            time.sleep(1)
        except OSError as e:
            print(str(e))
            sys.exit(1)

        try:
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)

                message = 'Демон (PID: {}) удален'.format(pid)
                logger.info(message)
                print(message)

        except IOError as e:
            message = str(e) + "\nНевозможно удалить pid-файл {}".format(self.pidfile)
            sys.stderr.write(message)
            sys.exit(1)


    ############################################################
    #   DAEMON: RESTART
    ############################################################
    def restart(self):
        self.stop()
        time.sleep(1)
        self.start()



    ############################################################
    #   DAEMON: RUN
    ############################################################
    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been daemonized by start() or restart().

        Example:

        class MyDaemon(Daemon):
            def run(self):
                while True:
                    time.sleep(1)
        """

class MyDaemon(Daemon):
    def run(self):
        runPointer()
        #while True:
        #    time.sleep(1)


############################################################
#   ЗАПУСК
############################################################
if __name__ == "__main__":
    daemon = MyDaemon(DAEMON_INI.FILE_PID)

    message = ''
    for s0 in sys.argv: message += ' '+s0
    logger.info('{}'.format(message.strip()))

    if len(sys.argv) == 2:
        if   'start'   == sys.argv[1]: daemon.start()
        elif 'stop'    == sys.argv[1]: daemon.stop()
        elif 'restart' == sys.argv[1]: daemon.restart()
        elif 'status'  == sys.argv[1]: daemon.status()
        else:
            message = "Неизвестная команда"
            print (message)
            logger.warning(message)

            sys.exit(2)
        sys.exit(0)
    else:
        message = "Неизвестная команда"
        print (message)
        logger.warning(message)

        print ("Использование: {} start|stop|restart".format(sys.argv[0]))
        sys.exit(2)

