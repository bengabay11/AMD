import hashlib

from src.server import config
from src.server.network.ClientAction import ClientAction


class ClientChangeTemporaryPassword(ClientAction):
    def act(self, data, send):
        new_password = data
        self.__db.update_user(self.username, 'PASSWORD', hashlib.sha224(new_password).hexdigest())
        self.__db.update_user(self.username, 'FORGOT_PASSWORD', False)
        print("sending Password Accepted")
        send(self.__aes_cipher.encrypt('Password Accepted') + config.CLIENT_DELIMITER)

