from src.server import config
from src.server.ClientAction import ClientAction


class ClientCheckVersion(ClientAction):
    def act(self, data, send):
        version = data
        version_quality = int(version.split('.')[0])
        if version_quality < 5:
            print("Sending You have an old version[" + version + "]. you must update for hotfixes")
            self.__ui_file_writer.write("Notification, - " + self.username + ": old version[" +
                                        version + "] - must update his version." + "\n")
            print("Sending Notification," + "old version[" + version + "] - must update version.")
            send(self.__aes_cipher.encrypt("Notification," + "old version[" + version +
                                           "] - must update version.") + config.CLIENT_DELIMITER)
        elif 5 < version_quality < 8:
            self.__ui_file_writer.write("Notification, - " + self.username +
                                        ": old version[" + version + "] -  recommended to update his"
                                                                     " version but still supported.\n")
            print("Sending Notification,old version[" + version + "] - recommended to update" \
                                                                  " version but still supported.")
            send(self.__aes_cipher.encrypt("Notification,old version[" +
                                           version + "] - recommended to update version but still supported.")
                 + config.CLIENT_DELIMITER)
