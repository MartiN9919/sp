import socket
import json
from synonyms_manager.constant import SYNONYMS_CONSTANT


class Socket:
    def __init__(self, host, port):
        self.sock = socket.socket(
            socket.AF_INET,  # семейство протоколов 'Интернет' (INET)
            socket.SOCK_STREAM,  # тип передачи данных 'потоковый' (TCP)
            proto=0  # протокол 'по умолчанию' для TCP, т.е. IP
        )
        self.address = (host, port)

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, 'sock'):
            if self.sock:
                self.sock.close()
            self.sock = None

    def send_message(self, data, channel=None):
        try:
            msg = json.dumps(data, ensure_ascii=False).encode(
                "utf-8")  # ensure_ascii=False - не экранировать ASCII символы
            offset = 0
            if channel is None:
                channel = self.sock
            while offset < len(msg):
                channel.send(msg[offset:offset + SYNONYMS_CONSTANT.SIZE])
                offset += SYNONYMS_CONSTANT.SIZE
            channel.shutdown(socket.SHUT_WR)  # закрыть направление
            ret = True
        except socket.error as e:
            ret = False
        return ret

    def get_message(self, channel):
        msg = b''
        try:
            while True:
                msg_step = channel.recv(SYNONYMS_CONSTANT.SIZE)
                if not msg_step:
                    break
                msg += msg_step
            data = json.loads(msg.decode("utf-8")) if msg != b'' else None
        except socket.error as e:
            data = None
        return data


class SocketClient(Socket):
    def __init__(self, host, port=SYNONYMS_CONSTANT.PORT, timeout=30.0):
        super().__init__(host=host, port=port)
        self.sock.settimeout(timeout)

    def request(self, data):  # из-за channel.shutdown вызывать !!! только один раз !!!
        try:
            self.sock.connect(self.address)
            if self.send_message(data=data):
                ret = self.get_message(channel=self.sock)
            else:
                ret = None
        except Exception as e:
            ret = None
        return ret


def request(host, port, data_type, data=None, param=None):
    client = SocketClient(host=host, port=port, timeout=30.0)
    try:
        dat = {'type': data_type}
        if data:
            dat['data'] = data
        if param:
            dat['param'] = param
        result = client.request(dat)
    except Exception as e:
        result = None
        raise e
    client.close()
    return result