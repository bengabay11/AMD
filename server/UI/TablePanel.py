from threading import Thread
from wx import wx
from server import config
from server.UI.utils import show_user_info
from server.db.database import DataBase

ComputationDoneEvent, EVT_COMPUTATION_DONE = wx.lib.newevent.NewEvent()
LIST_NOTIFICATIONS = []
NOTIFICATION = ""
CONTINUE = True
START = False
FINISH = False


class TablePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.db = DataBase()
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(100, 7)
        for row in range(100):
            for col in range(7):
                self.grid.SetReadOnly(row, col, True)

        self.grid.SetColLabelValue(0, "Username")
        self.grid.SetColLabelValue(1, "Status")
        self.grid.SetColLabelValue(2, "Suspicious Apps")
        self.grid.SetColLabelValue(3, "Suspicious Processes")
        self.grid.SetColLabelValue(4, "Camera On")
        self.grid.SetColLabelValue(5, "Unknown Sources")
        self.grid.SetColLabelValue(6, "Email")
        self.grid.AutoSizeColumns(True)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 0, wx.EXPAND)
        self.SetSizer(sizer)

        cursor = self.db.get_all_users()
        for row in cursor:
            self.add_user(row[0], row[1], row[5], row[2], row[4], row[8], row[9])

        get_data_thread = Thread(target=self.get_data)
        get_data_thread.start()

        self.Bind(EVT_COMPUTATION_DONE, self.update_table)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.on_selected_cell)

    def get_data(self):
        """The function runs as a thread, and read in while loop from txt file, to get data changes in the UI.
         every time the function gets new data she inform the UI main thread by PostEvent."""
        global NOTIFICATION, CONTINUE
        file_name = "UI data.txt"
        f = open(file_name, "wb")
        f.close()
        position = -1
        current_notification = ""
        list_notifications = []
        while FINISH is False:
            if CONTINUE:
                file_object = open(file_name, "r+")
                string_file = file_object.read()
                file_object.close()

                if string_file.split(config.FILE_DELIMITER) != list_notifications:
                    list_notifications = string_file.split(config.FILE_DELIMITER)
                    try:
                        current_notification = list_notifications[position]
                    except IndexError:
                        pass
                    CONTINUE = False
                    NOTIFICATION = current_notification
                    evt = ComputationDoneEvent()
                    wx.PostEvent(self, evt)
                    position += 1

                    if len(list_notifications[position:]) > 1:
                        position += len(list_notifications[position:]) - 1

    def update_table(self, event):
        """The function analyzes the command to the UI, and calls a function accordingly."""
        global CONTINUE, NOTIFICATION, MALICIOUS_PROCESSES_DICT
        list_command = NOTIFICATION.split(",")
        request = list_command[0]
        if request == "Login":
            username = list_command[1]
            self.set_status(username, "Online")

        elif request == "LogOut":
            username = list_command[1]
            MALICIOUS_PROCESSES_DICT[username] = []
            self.set_status(username, "Offline")

        elif request == "SignUp":
            username, email = list_command[1], list_command[2]
            self.add_user(username, "Online", email)

        elif request == "Notification":
            notification = list_command[1]
            self.add_notification(notification)

        elif request == "ChangeUsername":
            old_username, new_username = list_command[1], list_command[2]
            self.change_cell(old_username, new_username, 0)

        elif request == "ChangeEmail":
            username, new_email = list_command[1], list_command[2]
            self.change_cell(username, new_email, 6)

        elif request == "Delete":
            username = list_command[1]
            self.delete_user(username)

        elif request == "UnknownSources":
            username, allowed = list_command[1], list_command[2]
            self.change_cell(username, allowed, 5)

        elif request == "Increase":
            column = -1
            name_column, username = list_command[1], list_command[2]
            if name_column == "CameraOn":
                column = 4
            if name_column == "SuspiciousApps":
                column = 2
            if name_column == "CheckProcesses":
                column = 3
            self.increase_cell(username, column)

        elif request == "SuspiciousProcessesUpdate":
            username = list_command[1]
            processes_list = list_command[2].split(chr(25))
            MALICIOUS_PROCESSES_DICT[username] = processes_list

        CONTINUE = True

    def add_user(self, username, status, email, suspicious_apps=0, camera_on=0,
                 check_processes=0, unknown_sources="null"):
        """The function get details of user and adds him to the table."""
        suspicious_apps = str(suspicious_apps)
        camera_on = str(camera_on)
        check_processes = str(check_processes)
        row = self.db.num_rows()
        for i in range(100):
            check_username = self.grid.GetCellValue(i, 0)
            if check_username == '':
                row = i
                break

        self.grid.SetCellValue(row, 0, username)
        self.grid.SetCellValue(row, 1, status)
        if status == "Online":
            self.grid.SetCellTextColour(row, 1, wx.GREEN)
        elif status == "Offline":
            self.grid.SetCellTextColour(row, 1, wx.RED)
        self.grid.SetCellValue(row, 2, suspicious_apps)
        self.grid.SetCellValue(row, 3, check_processes)
        self.grid.SetCellValue(row, 4, camera_on)
        self.grid.SetCellValue(row, 5, unknown_sources)
        self.grid.SetCellValue(row, 6, email)
        self.grid.AutoSizeColumns(True)

    def delete_user(self, username):
        """The function gets username and deletes him from the table."""
        for i in range(100):
            check_username = self.grid.GetCellValue(i, 0)
            if check_username == username:
                self.grid.SetCellValue(i, 0, "")
                self.grid.SetCellValue(i, 1, "")
                self.grid.SetCellValue(i, 2, "")
                self.grid.SetCellValue(i, 3, "")
                self.grid.SetCellValue(i, 4, "")
                self.grid.SetCellValue(i, 5, "")
                self.grid.SetCellValue(i, 6, "")
                self.grid.AutoSizeColumns(True)
                break

    def set_status(self, username, status):
        """The function sets the status of the relevant user in the table."""
        for row in range(100):
            check_username = self.grid.GetCellValue(row, 0)
            if check_username == username and check_username != '':
                self.grid.SetCellValue(row, 1, status)
                if status == "Online":
                    self.grid.SetCellTextColour(row, 1, wx.GREEN)
                elif status == "Offline":
                    self.grid.SetCellTextColour(row, 1, wx.RED)
                break

    def change_cell(self, username, new_value, column):
        """The function gets username to handle, column, value and changes the relevant cell."""
        for row in range(100):
            check_username = self.grid.GetCellValue(row, 0)
            if check_username == username:
                self.grid.SetCellValue(row, column, new_value)

    def add_notification(self, notification):
        """The function gets notification and adds it to the notifications window at the menu panel."""
        self.parent.GetParent().menu_panel.notifications_window.AppendText(notification + "\n")

    def on_selected_cell(self, event):
        """When the user select the cell of one of the clients, the function called, and starts the thread that shows
         the information about this client."""
        row = event.GetRow()
        if event.GetCol() == 0:
            username = self.grid.GetCellValue(row, 0)
            status = self.grid.GetCellValue(row, 1)
            suspicious_apps = self.grid.GetCellValue(row, 2)
            check_processes = self.grid.GetCellValue(row, 3)
            camera_on = self.grid.GetCellValue(row, 4)
            unknown_sources = self.grid.GetCellValue(row, 5)
            email = self.grid.GetCellValue(row, 6)
            show_user_info_thread = Thread(target=show_user_info, args=(username, status, suspicious_apps,
                                                                        check_processes, camera_on,
                                                                        unknown_sources, email))
            show_user_info_thread.daemon = True
            show_user_info_thread.start()

    def increase_cell(self, username, column):
        """The function increase in the UI the count in the relevant cell."""
        for row in range(100):
            check_username = self.grid.GetCellValue(row, 0)
            if check_username == username:
                new_value = str(int(self.grid.GetCellValue(row, column)) + 1)
                self.grid.SetCellValue(row, column, new_value)
