from threading import Thread
import wx
from src.server import client_handler
from src.server import config
from src.server.Server import Server
from src.server.UI.MainFrame import MainFrame


def start_server():
    server_socket = Server()
    server_socket.start(config.SERVER_IP, config.SERVER_PORT, config.NUM_CLIENTS)
    while True:
        (client_socket, client_address) = server_socket.accept()
        clh = client_handler.ClientHandler(client_socket, client_address)
        clh.start()


def main():
    server_thread = Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    app = wx.App(False)
    main_frame = MainFrame()
    main_frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
