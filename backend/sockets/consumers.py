import json

from channels.generic.websocket import WebsocketConsumer

from data_base_driver.sys_notifications.get_notifications_info import get_notifications_by_user
from sockets.channels_list import ChannelsList


def send_notification(to_user_id, data):
    """
    Функция для отправки сообщения пользователя по его каналу, при отсутствии канала с данным пользователем
    сообщения не будут отправлено
    @param to_user_id: идентификационный номер пользователя, которому следует отправить сообщение
    @param data: информация для отправки
    """
    channel_list = ChannelsList()
    channel = channel_list.get_channel_by_user(to_user_id)
    if channel != None:
        channel.send(json.dumps({'notifications': [data], 'to_remove': []}))


class Chanel(WebsocketConsumer):
    """
    Класс для инкапсуляции каналов веб сокета
    содержит ссылку на объект класса одиночки содержащего все другие каналы
    """
    channel_list = ChannelsList()

    def connect(self):
        """
        Функция обработки присоединения клиента, добавляет объект данного класса в общий список соединений
        """
        self.channel_list.add_channel(self, self.scope['user'].id)
        self.accept()

    def disconnect(self, close_code):
        """
        Функция обработки клиента от канала, удаляет объект из списка каналов
        @param close_code: причина закрытия соединения
        """
        self.channel_list.remove_channel(self.scope['user'].id)

    def send_notifications(self, previous_list):
        """
        Функция обработчик для сообщения с запросом списка оповещений
        @param previous_list: список идентификационных номеров уже прочитанных сообщений
        """
        self.send(json.dumps(get_notifications_by_user(self.scope['user'].id, previous_list)))

    def receive(self, text_data=None, bytes_data=None):
        """
        Функция обработчик для приема всех сообщений канала, перенаправляет сообщения соответствующим
        функциям обработки
        @param text_data: ссылка на текстовое содержание пришедшего сообщения
        @param bytes_data: ссылка на байтовое содержание пришедшего сообщения
        """
        message = json.loads(text_data)
        if message['type'] == 'alerts':
            self.send_notifications(message['message'])
