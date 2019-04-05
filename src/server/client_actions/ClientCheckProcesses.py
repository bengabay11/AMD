from src.server import config
from src.server.network.ClientAction import ClientAction


class ClientCheckProcesses(ClientAction):
    def act(self, data, send):
        list_processes = data.split("\n")[1:len(data.split("\n")) - 1]
        final_list_processes = []
        for process in list_processes:
            process_info = process.split()
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
                self.__ui_file_writer.write(
                    "Notification, - " + self.username + ": Suspicious process: " + process_name + ".\n")
                print("Sending Notification,Suspicious process: " + process_name + ".")
                send(self.__aes_cipher.encrypt("Notification,Suspicious process: " + process_name) +
                     config.CLIENT_DELIMITER)
                suspicious_process = True

            if process_user not in config.WHITE_LIST_PROCESSES_USERS and process_user.startswith(
                    config.NORMAL_USER_PROCESS) is False:
                self.__ui_file_writer.write(
                    "Notification, - " + self.username + ": The process: " + process_name + " was started by"
                                                                                            " suspicious user: " +
                    process_user + ".\n")
                print("Sending Notification,The process: " + process_name + " was started by suspicious user: " + \
                      process_user + ".").send(self.__aes_cipher.encrypt("Notification,The process: " + process_name +
                                                                         " was started by suspicious user: " +
                                                                         process_user) + config.CLIENT_DELIMITER)
                suspicious_process = True

            if suspicious_process:
                suspicious_processes_data += (process_name + chr(20) + process_user + chr(20) + process_info["PID"] +
                                              chr(20) + process_info["PPID"] + chr(20) + process_info["WCHAN"] + chr(
                            25))
                suspicious_process = False
                user = self.__db.get_user(self.username)
                suspicious_process_count = user[8] + 1
                self.__db.update_user(self.username, "Check_Processes", suspicious_process_count)
                self.__ui_file_writer.write("IncreaseCheckProcesses," + self.username)

        if suspicious_processes_data != "":
            self.__ui_file_writer.write("SuspiciousProcessesUpdate," + self.username + "," + suspicious_processes_data)
