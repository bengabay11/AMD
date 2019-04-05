from src.server import config


class ClientCheckApps:
    def __init__(self, __db, aes_cipher, ui_file_writer):
        self.__db = __db
        self.__aes_cipher = aes_cipher
        self.__ui_file_writer = ui_file_writer

    def act(self, data, send):
        list_applications = self.get_list_applications(data)
        print("\n\n\n" + str(list_applications) + "\n\n\n")
        for app_name, app_package, app_installer, list_permissions in list_applications:
            # app installer check
            if app_installer != config.GOOGLE_PLAY_APP and app_installer != config.SYSTEM_APP:
                if app_installer == config.SAMSUNG_APP_STORE_APP:
                    self.__ui_file_writer.write("Notification, - " + self.username + ": "
                                                + app_name + " installed from Samsung App Store.\n")
                    print("Sending Notification," + app_name + " installed from Samsung App Store.")
                    send(
                        self.__aes_cipher.encrypt("Notification," + app_name + " installed from Samsung App Store.") +
                        config.CLIENT_DELIMITER)
                    suspicious_app = True
                elif app_installer == config.AMAZON_APP:
                    self.__ui_file_writer.write("Notification, - " + self.username + ": " + app_name + " installed from"
                                                                                                       " Amazon.\n")
                    print("Sending Notification," + app_name + " installed from Amazon.")
                    send(self.__aes_cipher.encrypt("Notification," + app_name +
                                                   " installed from Amazon.") +
                         config.CLIENT_DELIMITER)
                    suspicious_app = True
                elif app_installer.startswith(config.FACEBOOK_APP):
                    self.__ui_file_writer.write("Notification, - " + self.username + ": " + app_name + " installed from"
                                                                                                       " Facebook.\n")
                    print("Sending Notification," + app_name + " installed from Facebook.")
                    send(self.__aes_cipher.encrypt("Notification," + app_name +
                                                   " installed from Facebook.") +
                         config.CLIENT_DELIMITER)
                    suspicious_app = True
                else:
                    self.__ui_file_writer.write(
                        "Notification, - " + self.username + ": Unknown installer for " + app_name +
                        " - " + app_installer + ".\n")
                    print("Sending Notification,Unknown installer for " + app_name + " - " + app_installer)
                    send(self.__aes_cipher.encrypt("Notification,Unknown installer for " + app_name +
                                                   " - " + app_installer) + config.CLIENT_DELIMITER)
                    suspicious_app = True

                    # check permissions of unknown app
                    for suspicious_permission in config.UNKNOWN_APPS_BLACK_LIST_PERMISSIONS:
                        if suspicious_permission in list_permissions:
                            suspicious_app = True
                            self.__ui_file_writer.write(
                                "Notification, - " + self.username + ": Suspicious permission in " +
                                app_name + " - " + suspicious_permission + ".\n")
                            print("Sending Notification,Suspicious permission in " + app_name + \
                                  " - " + suspicious_permission + ".")
                            send(self.__aes_cipher.encrypt("Notification,Suspicious permission in " +
                                                           app_name + " - " + suspicious_permission + ".") +
                                 config.CLIENT_DELIMITER)
                if suspicious_app:
                    user = self.__db.get_user(self.username)
                    suspicious_app_count = user[2] + 1
                    self.__db.update_user(self.username, "SUSPICIOUS_APPS", suspicious_app_count)
                    self.__ui_file_writer.write("IncreaseSuspiciousApps," + self.username)

    def get_list_applications(self, data):
        list_applications = []
        list_apps = data.split("&")
        for i in range(len(list_apps)):
            app_info = list_apps[i]
            app_name = app_info.split(":")[0]
            app_package = app_info.split(":")[1]
            app_installer = app_info.split(":")[2]
            list_permissions = app_info.split(":")[3].split("/")
            list_applications.append((app_name, app_package, app_installer, list_permissions))

        return list_applications
