import abc


class ClientAction(abc.ABC):
    def __init__(self, db, aes_cipher, ui_file_writer):
        self.__db = db
        self.__aes_cipher = aes_cipher
        self.__ui_file_writer = ui_file_writer

    @abc.abstractmethod
    def act(self, data, send):
        pass
