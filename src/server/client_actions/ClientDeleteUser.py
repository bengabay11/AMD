from src.server import config
from src.server.ClientAction import ClientAction


class ClientDeleteUser(ClientAction):
    def act(self, data, send):
        self.__db.delete_user(self.username)
        self.__ui_file_writer.write("Delete" + "," + self.username)
        print("Sending to " + self.username + ": Delete Complete")
        send(self.__aes_cipher.encrypt("Delete Complete") + config.CLIENT_DELIMITER)
        self.__db.close()
        # self.__socket.close()


