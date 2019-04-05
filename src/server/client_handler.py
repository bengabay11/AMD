from threading import Thread
import hashlib
from src.server import config
from src.server.client_actions.utils import get_random_string
from src.server.db.database import DataBase
from src.server.encryptions.AESCipher import AESCipher


FINISH = False
FORGOT_PASSWORD = False


class ClientHandler(Thread):
    def __init__(self, socket, client_actions, aes_key):
        Thread.__init__(self)
        self.__socket = socket
        self.__client_actions = client_actions
        self.aes_key = aes_key
        self.aes_cipher = None

    def run(self):
        """The function is ran when starting the thread."""
        # send to the client the AES key
        self.aes_cipher = AESCipher(self.aes_key)
        self.__socket.send("AESKey," + self.aes_key)

        global FINISH
        FINISH = False
        while FINISH is False:
            encrypted_data = self.__socket.recv(config.DATA_LENGTH)
            plain_data = self.aes_cipher.decrypt(encrypted_data)
            client_data = ""  # deserialize to client data object
            self.__client_actions[client_data.type].act(client_data.data, self.__socket.send)

    def close(self):
        pass

            #         elif request == 'ForgotPassword':
            #             username_or_email = list_data[1]
            #             self.forgot_password(username_or_email)
            #
            #         elif request == "ChangeTemporaryPassword":x
            #             new_password = list_data[1]
            #             self.change_temporary_password(new_password)
            #
            #         elif request == 'CheckVersion':
            #             version = list_data[1]
            #             version_quality = int(version.split('.')[0])
            #             check_version_thread = Thread(target=self.check_version, args=(version, version_quality))
            #             check_version_thread.start()
            #
            #         elif request == "CheckSmishingData":
            #             self.check_smishing_data += list_data[1]
            #
            #         elif request == "CheckSmishing":
            #             check_smishing_data = self.check_smishing_data
            #             self.check_smishing_data = ""
            #             check_smishing_thread = Thread(target=self.check_smishing, args=(check_smishing_data,))
            #             check_smishing_thread.start()
            #
            #         elif request == "CheckProcessesData":
            #             self.__socket.send(self.aes_cipher.encrypt("CheckProcesses part accepted") +
            #                                config.CLIENT_DELIMITER)
            #             self.check_processes_data += list_data[1]
            #
            #         elif request == "CheckProcesses":
            #             print("CheckProcesses Length: " + str(len(self.check_processes_data)))
            #             output = self.check_processes_data
            #             self.check_processes_data = ""
            #             check_processes_thread = Thread(target=self.check_processes, args=(output,))
            #             check_processes_thread.start()
            #
            #         elif request == "CameraOn":
            #             current_time = list_data[1]
            #             self.camera_on(current_time)
            #
            #         elif request == "UnknownSources":
            #             allowed = list_data[1]
            #             if allowed == "Allowed":
            #                 self.write_to_file("Notification" + ",- " + self.username +
            #                                    ": Unknown Sources permission is allowed" + ".\n")
            #             self.write_to_file("UnknownSources," + self.username + "," + allowed)
            #             self.db.update_user(self.username, "Unknown_Sources", allowed)
            #
            #         elif request == 'ChangeUsername':
            #             new_username = list_data[1]
            #             self.change_username(new_username)
            #
            #         elif request == 'ChangePassword':
            #             old_password, new_password = list_data[1], list_data[2]
            #             self.change_password(old_password, new_password)
            #
            #         elif request == 'ChangeEmail':
            #             new_email = list_data[1]
            #             self.change_email(new_email)
            #
            #         elif request == 'DeleteUser':
            #             self.delete_user()
            #             FINISH = True
            #             break

            # elif request == 'LogOut' or data_from_client == '':
            #     self.logout()
            #     FINISH = True
            #     break


    def check_apps_review(self):
        """The function check the review of the apps on play store."""
        app_url = "https://play.google.com/store/apps/details?id="
        for app_name, app_package, app_installer, list_permissions in self.list_applications:
            # Check if the app installed from play store.
            if FINISH:
                break
            if app_installer == config.GOOGLE_PLAY_APP:
                # Check app review on play store
                app_details = get_app_details(app_url + app_package)
                if app_details is not None:
                    print("Review for " + app_name + ": downloads: " + str(app_details['downloads']) + ", rating: " + \
                          str(app_details['rating']))
                    if app_details['rating'] < 3 or app_details['downloads'] < 100:
                        self.write_to_file("Notification, - " + self.username + ": Bad review on play store for " +
                                           app_name + " - maybe malware.\n")
                        print("Sending Notification,Bad review on play store for " + app_name + " - maybe malware.")
                        self.__socket.send(self.aes_cipher.encrypt("Notification,Bad review on play store for " +
                                                                   app_name + " - maybe malware.") +
                                           config.CLIENT_DELIMITER)

    def check_apps(self):
        """The function runs on the apps list and check if there is a suspicious apps."""
        print("\n\n\n" + str(self.list_applications) + "\n\n\n")
        for app_name, app_package, app_installer, list_permissions in self.list_applications:
            # app installer check
            if app_installer != config.GOOGLE_PLAY_APP and app_installer != config.SYSTEM_APP:
                if app_installer == config.SAMSUNG_APP_STORE_APP:
                    self.write_to_file("Notification, - " + self.username + ": " + app_name + " installed from"
                                                                                              " Samsung App Store.\n")
                    print("Sending Notification," + app_name + " installed from Samsung App Store.")
                    self.__socket.send(
                        self.aes_cipher.encrypt("Notification," + app_name + " installed from Samsung App Store.") +
                        config.CLIENT_DELIMITER)
                    suspicious_app = True
                elif app_installer == config.AMAZON_APP:
                    self.write_to_file("Notification, - " + self.username + ": " + app_name + " installed from"
                                                                                              " Amazon.\n")
                    print("Sending Notification," + app_name + " installed from Amazon.")
                    self.__socket.send(self.aes_cipher.encrypt("Notification," + app_name +
                                                               " installed from Amazon.") +
                                       config.CLIENT_DELIMITER)
                    suspicious_app = True
                elif app_installer.startswith(config.FACEBOOK_APP):
                    self.write_to_file("Notification, - " + self.username + ": " + app_name + " installed from"
                                                                                              " Facebook.\n")
                    print("Sending Notification," + app_name + " installed from Facebook.")
                    self.__socket.send(self.aes_cipher.encrypt("Notification," + app_name +
                                                               " installed from Facebook.") +
                                       config.CLIENT_DELIMITER)
                    suspicious_app = True
                else:
                    self.write_to_file("Notification, - " + self.username + ": Unknown installer for " + app_name +
                                       " - " + app_installer + ".\n")
                    print("Sending Notification,Unknown installer for " + app_name + " - " + app_installer)
                    self.__socket.send(self.aes_cipher.encrypt("Notification,Unknown installer for " + app_name +
                                                               " - " + app_installer) + config.CLIENT_DELIMITER)
                    suspicious_app = True

                    # check permissions of unknown app
                    for suspicious_permission in config.UNKNOWN_APPS_BLACK_LIST_PERMISSIONS:
                        if suspicious_permission in list_permissions:
                            suspicious_app = True
                            self.write_to_file("Notification, - " + self.username + ": Suspicious permission in " +
                                               app_name + " - " + suspicious_permission + ".\n")
                            print("Sending Notification,Suspicious permission in " + app_name + \
                                  " - " + suspicious_permission + ".")
                            self.__socket.send(self.aes_cipher.encrypt("Notification,Suspicious permission in " +
                                                                       app_name + " - " + suspicious_permission + ".") +
                                               config.CLIENT_DELIMITER)
                if suspicious_app:
                    db2 = DataBase()
                    user = db2.get_user(self.username)
                    suspicious_app_count = user[2] + 1
                    db2.update_user(self.username, "SUSPICIOUS_APPS", suspicious_app_count)
                    self.write_to_file("IncreaseSuspiciousApps," + self.username)

    @staticmethod
    def check_smishing(check_smishing_data):
        list_inbox = []
        list_sms = check_smishing_data.split("&*(")
        for i in range(len(list_sms)):
            sms_info = list_sms[i]
            address = sms_info.split("#^%")[0]
            body = sms_info.split("&*(")[1]
            list_inbox.append((address, body))

        print(list_inbox)

    def check_processes(self, output):
        """The function checks all the processes that the client sent, and detect malwares."""
        list_processes = output.split("\n")[1:len(output.split("\n")) - 1]
        final_list_processes = []
        for process in list_processes:
            process_info = process.split(" ")
            process_info = filter(None, process_info)
            final_process_info = {"USER": process_info[0], "PID": process_info[1], "PPID": process_info[2],
                                  "WCHAN": process_info[5]}
            try:
                final_process_info["NAME"] = process_info[8]
            except:
                final_process_info["NAME"] = process_info[7]
            final_list_processes.append(final_process_info)

        suspicious_process = False
        suspicious_processes_data = ""
        for process_info in final_list_processes:
            process_name = process_info["NAME"]
            process_user = process_info["USER"]

            if process_name in config.BLACK_LIST_PROCESSES_NAMES:
                self.write_to_file("Notification, - " + self.username + ": Suspicious process: " + process_name + ".\n")
                print("Sending Notification,Suspicious process: " + process_name + ".")
                self.__socket.send(self.aes_cipher.encrypt("Notification,Suspicious process: " + process_name) +
                                   config.CLIENT_DELIMITER)
                suspicious_process = True

            if process_user not in config.WHITE_LIST_PROCESSES_USERS and process_user.startswith(
                    config.NORMAL_USER_PROCESS) is False:
                self.write_to_file(
                    "Notification, - " + self.username + ": The process: " + process_name + " was started by"
                                                                                            " suspicious user: " +
                    process_user + ".\n")
                print("Sending Notification,The process: " + process_name + " was started by suspicious user: " + \
                      process_user + ".")
                self.__socket.send(
                    self.aes_cipher.encrypt("Notification,The process: " + process_name + " was started by"
                                                                                          " suspicious user: " +
                                            process_user) + config.CLIENT_DELIMITER)
                suspicious_process = True

            if suspicious_process:
                suspicious_processes_data += (process_name + chr(20) + process_user + chr(20) + process_info["PID"] +
                                              chr(20) + process_info["PPID"] + chr(20) + process_info["WCHAN"] + chr(
                            25))
                suspicious_process = False
                db2 = DataBase()
                user = db2.get_user(self.username)
                suspicious_process_count = user[8] + 1
                db2.update_user(self.username, "Check_Processes", suspicious_process_count)
                self.write_to_file("IncreaseCheckProcesses," + self.username)

        if suspicious_processes_data != "":
            self.write_to_file("SuspiciousProcessesUpdate," + self.username + "," + suspicious_processes_data)

    def camera_on(self, current_time):
        """The function inform the db, the file, and the client."""
        user = self.db.get_user(self.username)
        camera_on_count = user[4] + 1
        self.db.update_user(self.username, "CAMERA_ON", camera_on_count)
        self.write_to_file("Notification, - " + self.username + ": has camera open at " + current_time + ".\n")
        self.write_to_file("IncreaseCameraOn," + self.username)

    def forgot_password(self, username_or_email):
        """The function check if there is a user with that has the username or the email that the client send. if there
        is, the server send the password of the user to his email and if not, he send an error message to the client."""
        user = self.db.get_user(username_or_email)
        if user is None:
            print("sending Username Does'nt Exist")
            self.__socket.send(self.aes_cipher.encrypt("Username Does'nt Exist") + config.CLIENT_DELIMITER)
        else:
            temporary_password = get_random_string(6)
            username = user[0]
            to = user[5]
            subject = "AMD - Forgot Password"
            body = "Hello " + username + "," + '\n\n' + "We received a request that you forgot your password. " \
                                                        "Login with your temporary password and set your own new " \
                                                        "password to be logged in." + '\n\n' + \
                   "your temporary password is: " + temporary_password
            msg = self.email.create_message(to, body, subject)
            result = self.email.send_new_email(msg)
            if result == "Success":
                print("Sending Email Sent")
                self.__socket.send(self.aes_cipher.encrypt("Email Sent") + config.CLIENT_DELIMITER)

                self.db.update_user(username, 'PASSWORD', hashlib.sha224(temporary_password).hexdigest())
                self.db.update_user(username, 'FORGOT_PASSWORD', True)
            elif result == "Fail":
                print("Fail Sending Email")
                self.__socket.send(self.aes_cipher.encrypt("Fail Sending Email") + config.CLIENT_DELIMITER)

    def change_temporary_password(self, new_password):
        """The function change the password of the client to a new one."""
        self.db.update_user(self.username, 'PASSWORD', hashlib.sha224(new_password).hexdigest())
        self.db.update_user(self.username, 'FORGOT_PASSWORD', False)
        print("sending Password Accepted")
        self.__socket.send(self.aes_cipher.encrypt('Password Accepted') + config.CLIENT_DELIMITER)

    def change_username(self, new_username):
        """The function gets a request from the client to change his username. the server change the username if there
         is no other username that already has this username."""
        new_user = self.db.get_user(new_username)
        if new_user is None:
            self.db.update_user(self.username, 'USERNAME', new_username)
            self.write_to_file("ChangeUsername" + "," + self.username + "," + new_username)
            self.username = new_username
            print("sending Username Changed")
            self.__socket.send(self.aes_cipher.encrypt('Username Changed') + config.CLIENT_DELIMITER)
        else:
            print("sending Username Exist")
            self.__socket.send(self.aes_cipher.encrypt("Username Exist") + config.CLIENT_DELIMITER)

    def change_email(self, new_email):
        """The function gets a request from the client to change his email. the server change the email if there
            the new email is valid."""
        if valid_email(new_email):
            print("check: " + str(new_email.split("@")[1].split(".")))
            self.db.update_user(self.username, 'EMAIL', new_email)
            self.write_to_file("ChangeEmail" + "," + self.username + "," + new_email)
            print("sending Email Changed")
            self.__socket.send(self.aes_cipher.encrypt('Email Changed') + config.CLIENT_DELIMITER)
        else:
            print("Sending Invalid Email")
            self.__socket.send(self.aes_cipher.encrypt("Invalid Email") + config.CLIENT_DELIMITER)

    def change_password(self, old_password, new_password):
        """The function gets a request from the client to change his password. the server change the password with
         no tests."""
        user = self.db.get_user(self.username)
        old_password = hashlib.sha224(old_password).hexdigest()
        if user[6] == old_password:
            self.db.update_user(self.username, 'PASSWORD', hashlib.sha224(new_password).hexdigest())
            print("sending Password Changed")
            self.__socket.send(self.aes_cipher.encrypt('Password Changed') + config.CLIENT_DELIMITER)
        else:
            print("Sending Incorrect Password")
            self.__socket.send(self.aes_cipher.encrypt('Incorrect Password') + config.CLIENT_DELIMITER)

    def check_version(self, version, version_quality):
        """The functions gets a an android version, and checks if its old."""
        if version_quality < 5:
            print("Sending You have an old version[" + version + "]. you must update for hotfixes")
            self.write_to_file("Notification, - " + self.username + ": old version[" + version + "] - must update his"
                                                                                                 " version." + "\n")
            print("Sending Notification," + "old version[" + version + "] - must update version.")
            self.__socket.send(self.aes_cipher.encrypt("Notification," + "old version[" + version +
                                                       "] - must update version.") + config.CLIENT_DELIMITER)
        elif 5 < version_quality < 8:
            self.write_to_file("Notification, - " + self.username +
                               ": old version[" + version + "] -  recommended to update his"
                                                            " version but still supported.\n")
            print("Sending Notification,old version[" + version + "] - recommended to update" \
                                                                  " version but still supported.")
            self.__socket.send(self.aes_cipher.encrypt("Notification,old version[" + version +
                                                       "] - recommended to update version but still supported.") +
                               config.CLIENT_DELIMITER)

    def delete_user(self):
        """The function deletes the user from the database and the ui."""
        self.db.delete_user(self.username)
        self.write_to_file("Delete" + "," + self.username)
        print("Sending to " + self.username + ": Delete Complete")
        self.__socket.send(self.aes_cipher.encrypt("Delete Complete") + config.CLIENT_DELIMITER)
        self.db.close()
        self.__socket.close()

    def logout(self):
        """The function logout from the current user account, and update it in the database and the ui."""
        self.db.update_user(self.username, "STATUS", "Offline")
        self.write_to_file("LogOut" + "," + self.username)
        print("Sending to " + self.username + ": Logout Successfully")
        self.__socket.send(self.aes_cipher.encrypt("Logout Successfully") + config.CLIENT_DELIMITER)
        self.db.close()
        self.__socket.close()
