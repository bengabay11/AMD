import hashlib
from src.server import config
from src.server.ClientAction import ClientAction


class ClientChangePassword(ClientAction):
    def act(self, data, send):
        list_data = data.split(config.CLIENT_DELIMITER)
        old_password, new_password = list_data[1], list_data[2]
        user = self.__db.get_user(self.username)
        old_password = hashlib.sha224(old_password).hexdigest()
        if user[6] == old_password:
            self.__db.update_user(self.username, 'PASSWORD', hashlib.sha224(new_password).hexdigest())
            print("sending Password Changed")
            send(self.__aes_cipher.encrypt('Password Changed') + config.CLIENT_DELIMITER)
        else:
            print("Sending Incorrect Password")
            send(self.__aes_cipher.encrypt('Incorrect Password') + config.CLIENT_DELIMITER)
