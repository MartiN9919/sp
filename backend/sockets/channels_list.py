from data_base_driver.connect.base_conection import SingletonMeta


class ChannelsList(metaclass=SingletonMeta):
    """
    Класс для инкапсуляции канала с пользователем
    """

    def __init__(self):
        self.channels_dict = {}

    def add_channel(self, channel, user_id):
        """
        Функция для добавления нового канала в список
        @param channel: объект класса канала
        @param user_id: идентификационный номер пользователя
        """
        self.channels_dict[user_id] = channel

    def get_channel_by_user(self, user_id):
        """
        Функция для получения канала по идентификатору пользователя
        @param user_id: идентификационный номер пользователя
        @return: объект класса канала принадлежащий данному пользователю
        """
        return self.channels_dict.get(user_id, None)

    def remove_channel(self, user_id):
        """
        Функция для удаления канада из списка
        @param user_id: идентификационный номер пользователя
        @return: удаляемый объект класса канала, если такой имеется
        """
        return self.channels_dict.pop(user_id, None)
