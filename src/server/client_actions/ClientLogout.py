from src.server import config
from src.server.network.ClientAction import ClientAction


class ClientLogout(ClientAction):
    def act(self, data, send):
        self.__db.update_user(self.username, "STATUS", "Offline")
        self.__ui_file_writer.write("LogOut" + "," + self.username)
        print("Sending to " + self.username + ": Logout Successfully")
        send(self.__aes_cipher.encrypt("Logout Successfully") + config.CLIENT_DELIMITER)
        self.__db.close()
        # self.__socket.close()
