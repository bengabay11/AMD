from src.server import config
from src.server.ClientAction import ClientAction
from src.server.client_actions.utils import valid_email


class ClientChangeEmail(ClientAction):
    def act(self, data, send):
        new_email = data
        if valid_email(new_email):
            print("check: " + str(new_email.split("@")[1].split(".")))
            self.__db.update_user(self.username, 'EMAIL', new_email)
            self.__ui_file_writer.write("ChangeEmail" + "," + self.username + "," + new_email)
            print("sending Email Changed")
            send(self.__aes_cipher.encrypt('Email Changed') + config.CLIENT_DELIMITER)
        else:
            print("Sending Invalid Email")
            send(self.__aes_cipher.encrypt("Invalid Email") + config.CLIENT_DELIMITER)
