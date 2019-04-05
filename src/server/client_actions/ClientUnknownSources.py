from src.server.network.ClientAction import ClientAction


class ClientUnknownSources(ClientAction):
    def act(self, data, send):
        if data == "Allowed":
            self.__ui_file_writer.write("Notification" + ",- " + self.username + ": Unknown Sources permission is "
                                                                                 "allowed" + ".\n")
            self.__ui_file_writer.write("UnknownSources," + self.username + "," + data)
            self.__db.update_user(self.username, "Unknown_Sources", data)
