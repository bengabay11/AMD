from threading import Thread
import wx
from src.server.network import client_handler
from src.server import config
from src.server.network.Server import Server
from src.server.ui.UiFileWriter import UiFileWriter
from src.server.client_actions.ClientCameraOn import ClientCameraOn
from src.server.client_actions.ClientChangeEmail import ClientChangeEmail
from src.server.client_actions.ClientChangePassword import ClientChangePassword
from src.server.client_actions.ClientChangeTemporaryPassword import ClientChangeTemporaryPassword
from src.server.client_actions.ClientChangeUsername import ClientChangeUsername
from src.server.client_actions.ClientCheckApps import ClientCheckApps
from src.server.client_actions.ClientCheckSmishing import ClientCheckSmishing
from src.server.client_actions.ClientCheckVersion import ClientCheckVersion
from src.server.client_actions.ClientDeleteUser import ClientDeleteUser
from src.server.client_actions.ClientForgotPassword import ClientForgotPassword
from src.server.client_actions.ClientLogin import ClientLogin
from src.server.client_actions.ClientProcessesSmishing import ClientCheckProcesses
from src.server.client_actions.ClientSignUp import ClientSignUp
from src.server.client_actions.ClientUnknownSources import ClientUnknownSources
from src.server.client_actions.utils import get_random_string
from src.server.db.database import DataBase
from src.server.ui.MainFrame import MainFrame


def start_server():
    db = DataBase()
    ui_file_writer = UiFileWriter()
    email = EmailSender(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
    aes_key = get_random_string(10)
    client_actions = {"Login": ClientLogin(db, aes_key, ui_file_writer), "SignUp": ClientSignUp(db),
                      "ForgotPassword": ClientForgotPassword(db),
                      "ChangeTemporaryPassword": ClientChangeTemporaryPassword(db),
                      "CheckVersion": ClientCheckVersion(db), "CheckApps": ClientCheckApps(db),
                      "CheckProcesses": ClientCheckProcesses(db), "CheckSmishing": ClientCheckSmishing(db),
                      "CameraOn": ClientCameraOn(db), "UnknownSources": ClientUnknownSources(db),
                      "ChangeUsername": ClientChangeUsername(db), "ChangePassword": ClientChangePassword(db),
                      "ChangeEmail": ClientChangeEmail(db), "DeleteUser": ClientDeleteUser(db)}

    server_socket = Server()
    server_socket.start(config.SERVER_IP, config.SERVER_PORT, config.NUM_CLIENTS)
    while True:
        (client_socket, client_address) = server_socket.accept()
        clh = client_handler.ClientHandler(client_socket, client_actions, aes_key)
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
