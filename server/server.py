import socket
from server import config, client_handler


class Server:
    """Class of server socket."""
    def __init__(self):
        self.__socket = socket.socket()

    def start(self, ip, port, num_clients):
        """The function starts the listening of the server."""
        self.__socket.bind((ip, port))
        self.__socket.listen(num_clients)
        print("Listening on port %d" % port + '...')

    def accept(self):
        return self.__socket.accept()


def start():
    server_socket = Server()
    server_socket.start(config.SERVER_IP, config.SERVER_PORT, config.NUM_CLIENTS)
    while True:
        (client_socket, client_address) = server_socket.accept()
        clh = client_handler.ClientHandler(client_socket, client_address)
        clh.start()


if __name__ == '__main__':
    start()
