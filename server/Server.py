import socket


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
