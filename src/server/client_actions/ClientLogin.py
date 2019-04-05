import hashlib
from src.server import config
from src.server.ClientAction import ClientAction


class ClientLogin(ClientAction):
    def act(self, data, send):
        list_data = data.split(config.CLIENT_DELIMITER)
        check_username, check_password = list_data[1], list_data[2]
        user = self.__db.get_user(check_username)
        if user is None:
            print("Sending Incorrect Username")
            send(self.__aes_cipher.encrypt("Incorrect Username") + config.CLIENT_DELIMITER)
        else:
            username, password, forgot_password = user[0], user[6], user[7]
            check_password = hashlib.sha224(check_password).hexdigest()
            if username == check_username and password == check_password:
                self.__db.update_user(username, "STATUS", "Online")
                self.__ui_file_writer.write("Login" + "," + username)
                if forgot_password == 0:
                    print("Sending to " + username + ": Login Complete")
                    send(self.__aes_cipher.encrypt("Login Complete") + config.CLIENT_DELIMITER)
                elif forgot_password == 1:
                    print("Sending to " + username + ": Login Complete, need to change password")
                    send(self.__aes_cipher.encrypt("Login Complete, need to change password") + config.CLIENT_DELIMITER)
            else:
                print("sending: Incorrect Password")
                send(self.__aes_cipher.encrypt("Incorrect Password") + config.CLIENT_DELIMITER)



