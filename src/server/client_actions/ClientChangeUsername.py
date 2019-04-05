from src.server import config
from src.server.network.ClientAction import ClientAction


class ClientChangeUsername(ClientAction):
    def act(self, data, send):
        new_username = data
        new_user = self.__db.get_user(new_username)
        if new_user is None:
            self.__db.update_user(self.username, 'USERNAME', new_username)
            self.__ui_file_writer.write("ChangeUsername" + "," + self.username + "," + new_username)
            print("sending Username Changed")
            send(self.__aes_cipher.encrypt('Username Changed') + config.CLIENT_DELIMITER)
        else:
            print("sending Username Exist")
            send(self.__aes_cipher.encrypt("Username Exist") + config.CLIENT_DELIMITER)
