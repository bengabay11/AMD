from threading import Thread
from src.server import config
from src.server.DTOs.ClientData import ClientData
from src.server.encryptions.AESCipher import AESCipher


class ClientHandler(Thread):
    def __init__(self, socket, client_actions, aes_key):
        Thread.__init__(self)
        self.__socket = socket
        self.__client_actions = client_actions
        self.aes_key = aes_key
        self.aes_cipher = None

    def run(self):
        self.aes_cipher = AESCipher(self.aes_key)
        self.__socket.send("AESKey," + self.aes_key)
        client_action_type = None
        while client_action_type != "Logout" or client_action_type != "DeleteUser":
            encrypted_data = self.__socket.recv(config.DATA_LENGTH)
            plain_data = self.aes_cipher.decrypt(encrypted_data)
            client_data = ClientData("", "")  # deserialize to client data object
            client_action_type = client_data.action_type
            self.__client_actions[client_action_type].act(client_data.data, self.__socket.send)

    def close(self):
        pass
