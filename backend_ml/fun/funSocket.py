# -*- coding: utf-8 -*-

import socket, json, threading
import pickle                                                                       # _pickle  as pickle
from   fun.funSys      import logger, logError


class VAR:
    HOST = ''                                                                       # хост по умолчанию
    PORT = 5000                                                                     # порт по умолчанию
    SIZE = 1024                                                                     # рамер передаваемого блока

#####################################################
# в finally: объект = None
#####################################################
class Socket():
    def __init__(self, host=VAR.HOST, port=VAR.PORT):
        self.sock = socket.socket(
            socket.AF_INET,                                                         # семейство протоколов 'Интернет' (INET)
            socket.SOCK_STREAM,                                                     # тип передачи данных 'потоковый' (TCP)
            proto=0                                                                 # протокол 'по умолчанию' для TCP, т.е. IP
        )
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.addr = (host, port)

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, 'sock'):
            if self.sock != None: self.sock.close()
            self.sock = None


    #####################################################
    # ДАННЫЕ: ОТПРАВИТЬ
    #####################################################
    # channel - можно получить от self.get()
    #####################################################
    def send(self, data, channel=None):
        try:
            #msg = pickle.dumps(data)                                               # РАБОТАЕТ
            msg = json.dumps(data, ensure_ascii=False).encode("utf-8")              # ensure_ascii=False - не экранировать ASCII символы
            offset  = 0
            if channel is None: channel = self.sock
            while offset < len(msg):
                channel.send(msg[offset:offset+VAR.SIZE])
                offset += VAR.SIZE
            channel.shutdown(socket.SHUT_WR)                                        # закрыть направление
            ret = True
        except socket.error as e:
            logger.error(str(channel)+' '+str(e))
            ret = False
        return ret


    #####################################################
    # ДАННЫЕ: ПОЛУЧИТЬ
    #####################################################
    # ret = None - ошибка
    #####################################################
    def get(self, channel):
        msg = b''
        try:
            while True:
                msgStep = channel.recv(VAR.SIZE)
                if not msgStep: break
                msg += msgStep
            #data = pickle.loads(msg) if msg != b'' else None                        # РАБОТАЕТ
            data = json.loads(msg.decode("utf-8")) if msg != b'' else None
        except socket.error as e:
            logger.error(str(channel)+' '+str(e))
            data = None
        return data



#####################################################
# CLIENT
#####################################################
# в finally: объект = None
#####################################################
class SocketClient(Socket):
    def __init__(self, host=VAR.HOST, port=VAR.PORT, timeout=30.0):
        super().__init__(host=host, port=port)
        self.sock.settimeout(timeout)

    def request(self, data):                                                        # из-за channel.shutdown вызывать !!! только один раз !!!
        try:
            self.sock.connect(self.addr)
            if self.send(data=data): ret = self.get(channel=self.sock)
            else:                    ret = None
        except Exception as e:
            logger.error(str(self.sock)+' '+str(e))
            ret = None
        return ret



#####################################################
# SERVER
#####################################################
# в finally: объект = None
#####################################################
class SocketServer(Socket):
    def __init__(self, funHandler, host=VAR.HOST, port=VAR.PORT, maxClient=100):
        super().__init__(host=host, port=port)
        self.sock.bind(self.addr)
        self.sock.listen(maxClient)                                                 # размер очереди входящих подключений, т.н. backlog
        self.funHandler = funHandler

        while True:
            try:
                channel, _  = self.sock.accept()                                    # получить соединение из очереди - БЛОКИРУЮЩАЯ ОПЕРАЦИЯ
                self.thread = SocketServerThread(parent=self, channel=channel)      # исполнить в отдельном потоке
                self.thread.start()
            except Exception as e:
                logError(e)


class SocketServerThread(threading.Thread):
    def __init__(self, parent, channel):
        threading.Thread.__init__(self)
        self.parent  = parent
        self.channel = channel

    def run(self):
        try:
            data = self.parent.get(channel=self.channel)                            # None - ошибка
            logger.info((str(self.channel.getpeername())+': '+str(data))[:100])
            if data != None:
                data = self.parent.funHandler(data)
                self.parent.send(data=data, channel=self.channel)
        except Exception as e:
            logError(e)
        finally:
            if hasattr(self, 'channel'):
                if self.channel != None: self.channel.close()                       # закрывать соединение надо здесь
                self.channel = None
