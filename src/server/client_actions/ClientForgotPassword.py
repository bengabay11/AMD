import hashlib
from src.server import config
from src.server.ClientAction import ClientAction
from src.server.client_actions.utils import get_random_string


class ClientForgotPassword(ClientAction):
    def __init__(self, db, aes_cipher, ui_file_writer, email_sender):
        ClientAction.__init__(self, db, aes_cipher, ui_file_writer)
        self.__email_sender = email_sender

    def act(self, data, send):
        list_data = data.split(config.CLIENT_DELIMITER)
        username_or_email = list_data[1]
        user = self.__db.get_user(username_or_email)
        if user is None:
            print("sending Username Does'nt Exist")
            send(self.__aes_cipher.encrypt("Username Does'nt Exist") + config.CLIENT_DELIMITER)
        else:
            temporary_password = get_random_string(6)
            username = user[0]
            to = user[5]
            subject = "AMD - Forgot Password"
            body = "Hello " + username + "," + '\n\n' + "We received a request that you forgot your password. " \
                                                        "Login with your temporary password and set your own new " \
                                                        "password to be logged in." + '\n\n' + \
                   "your temporary password is: " + temporary_password
            msg = self.__email_sender.create_message(to, body, subject)
            result = self.__email_sender.send_new_email(msg)
            if result == "Success":
                print("Sending Email Sent")
                send(self.__aes_cipher.encrypt("Email Sent") + config.CLIENT_DELIMITER)

                self.__db.update_user(username, 'PASSWORD', hashlib.sha224(temporary_password).hexdigest())
                self.__db.update_user(username, 'FORGOT_PASSWORD', True)
            elif result == "Fail":
                print("Fail Sending Email")
                send(self.__aes_cipher.encrypt("Fail Sending Email") + config.CLIENT_DELIMITER)
