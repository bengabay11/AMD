import socket


class Server:
    def __init__(self):
        self.__socket = socket.socket()

    def start(self, ip, port, num_clients):
        self.__socket.bind((ip, port))
        self.__socket.listen(num_clients)
        print("Listening on port %d" % port + '...')

    def accept(self):
        return self.__socket.accept()
