import hashlib
from src.server import config
from src.server.network.ClientAction import ClientAction
from src.server.client_actions.utils import valid_email


class ClientSignUp(ClientAction):
    def act(self, data, send):
        list_data = data.split(config.CLIENT_DELIMITER)
        username, password, email = list_data[1], list_data[2], list_data[3]
        if valid_email(email):
            new_user = self.__db.get_user(username)
            if new_user is None:
                password = hashlib.sha224(password).hexdigest()
                self.__db.add_user([username, "Online", 0, 0, 0, email, password, False, 0])
                print("sending Username Accepted")
                send(self.__aes_cipher.encrypt("Username Accepted") + config.CLIENT_DELIMITER)
                self.__ui_file_writer.write("SignUp" + "," + username + "," + email)
            else:
                print("sending Username Exist")
                send(self.__aes_cipher.encrypt("Username Exist") + config.CLIENT_DELIMITER)
        else:
            print("Sending Invalid Email")
            send(self.__aes_cipher.encrypt("Invalid Email") + config.CLIENT_DELIMITER)
