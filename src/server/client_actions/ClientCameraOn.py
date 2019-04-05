import os

from src.server.ClientAction import ClientAction


class ClientCameraOn(ClientAction):
    def act(self, data, send):
        time_opened = data
        user = self.__db.get_user(self.username)
        camera_on_count = user[4] + 1
        self.__db.update_user(self.username, "CAMERA_ON", camera_on_count)
        self.__ui_file_writer.write("Notification, - " + self.username + ": has camera open at " +
                                    time_opened + os.linesep)
        self.__ui_file_writer.write("IncreaseCameraOn," + self.username)


