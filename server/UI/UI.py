import wx
import wx.grid
import wx.lib.newevent
from threading import Thread
from server import config
from server.db.database import DataBase

MALICIOUS_PROCESSES_DICT = {}
ComputationDoneEvent, EVT_COMPUTATION_DONE = wx.lib.newevent.NewEvent()
LIST_NOTIFICATIONS = []
NOTIFICATION = ""
CONTINUE = True
START = False
FINISH = False


def set_icon(frame):
    """Set icon for frame"""
    if "3.0" in wx.version():
        new_icon = wx.EmptyIcon()
    else:
        new_icon = wx.Icon()
    new_icon.CopyFromBitmap(wx.Bitmap(config.ICON_PIC_NAME))
    frame.SetIcon(new_icon)


class TablePanel(wx.Panel):
    """Panel that presents table of the clients that signed to the server."""

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


class MenuPanel(wx.Panel):
    """Panel that presents searching box and notifications window."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        # set background colour
        self.SetBackgroundColour("LIGHT BLUE")

        self.title = wx.StaticText(self, label="AMD Server", pos=(20, 40), size=(300, -1))
        font = wx.Font(25, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.title.SetFont(font)
        self.title.SetForegroundColour(wx.BLUE)

        img = wx.Image(config.ICON_PIC_NAME, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(self, -1, img, pos=(230, 30), size=(60, 60))

        font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.find_user_input = wx.TextCtrl(self, size=(200, 25), pos=(10, 115),
                                           style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.find_user_input.SetFont(font)
        self.find_user_button = wx.Button(self, label="Find User", pos=(225, 115), size=(85, -1))
        self.notifications_title = wx.StaticText(self, label="Notifications Window", pos=(80, 170), size=(100, -1))
        self.notifications_title.SetFont(font)
        self.notifications_window = wx.TextCtrl(self, size=(300, 250), pos=(10, 200),
                                                style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_READONLY)
        self.close_server_button = wx.Button(self, label="Close Server", pos=(170, 490), size=(100, -1))
        self.close_server_button.Bind(wx.EVT_BUTTON, self.parent.GetParent().on_close_window)
        self.clear_window_button = wx.Button(self, label="Clear Window", pos=(40, 490), size=(100, -1))
        self.clear_window_button.Bind(wx.EVT_BUTTON, self.clear_window)

    def clear_window(self, event):
        """The function clear the notifications window."""
        self.notifications_window.SetValue("")


class UserInfoFrame(wx.Frame):
    """Frame the present the details of the relevant user."""

    def __init__(self, username, status, suspicious_apps, check_processes, camera_on, unknown_sources, email):
        wx.Frame.__init__(self, None, -1, username + "'s Details", size=(600, 300))

        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        self.username = username
        self.details_grid = ""
        self.processes_grid = ""
        set_icon(self)
        self.create_details_grid(status, suspicious_apps, check_processes, camera_on, unknown_sources, email)
        self.create_processes_grid()
        self.details_grid.AutoSizeColumns(True)
        self.processes_grid.AutoSizeColumns(True)
        self.Center()
        # set background colour
        self.SetBackgroundColour("LIGHT BLUE")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.create_title(username + "'s Details"), 0, wx.EXPAND)
        sizer.Add(self.details_grid, 0, wx.EXPAND)
        sizer.Add(self.create_title("Malicious Processes"), 0, wx.EXPAND)
        sizer.Add(self.processes_grid, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def create_title(self, text):
        """The function creates StaticText According to the appropriate parameters and return the object."""
        title = wx.StaticText(self, label=text, pos=(250, 20))
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        title.SetFont(font)
        title.SetForegroundColour(wx.BLUE)
        return title

    def create_details_grid(self, status, suspicious_apps, check_processes, camera_on, unknown_sources, email):
        """The function return the grid that present the details of the user."""
        self.details_grid = wx.grid.Grid(self)
        self.details_grid.CreateGrid(2, 7)
        for row in range(2):
            for col in range(7):
                self.details_grid.SetReadOnly(row, col, True)

        self.details_grid.SetColLabelValue(0, "Username")
        self.details_grid.SetCellValue(0, 0, self.username)
        self.details_grid.SetColLabelValue(1, "Status")
        self.details_grid.SetCellValue(0, 1, status)
        self.details_grid.SetColLabelValue(2, "Suspicious Apps")
        self.details_grid.SetCellValue(0, 2, suspicious_apps)
        self.details_grid.SetColLabelValue(3, "Suspicious Processes")
        self.details_grid.SetCellValue(0, 3, check_processes)
        self.details_grid.SetColLabelValue(4, "Camera On")
        self.details_grid.SetCellValue(0, 4, camera_on)
        self.details_grid.SetColLabelValue(5, "Unknown Sources")
        self.details_grid.SetCellValue(0, 5, unknown_sources)
        self.details_grid.SetColLabelValue(6, "Email")
        self.details_grid.SetCellValue(0, 6, email)

    def create_processes_grid(self):
        """The function return the grid that present the malicious processes of the user."""
        final_list_processes = []
        try:
            list_processes = MALICIOUS_PROCESSES_DICT[self.username]
            for process in list_processes:
                final_list_processes.append(process.split(chr(20)))

            final_list_processes = final_list_processes[:len(final_list_processes)-1]
        except TypeError:
            pass
        except KeyError:
            pass

        self.processes_grid = wx.grid.Grid(self)
        self.processes_grid.CreateGrid(len(final_list_processes), 5)
        for row in range(len(final_list_processes)):
            for col in range(5):
                self.processes_grid.SetReadOnly(row, col, True)

        self.processes_grid.SetColLabelValue(0, "NAME")
        self.processes_grid.SetColLabelValue(1, "USER")
        self.processes_grid.SetColLabelValue(2, "PID")
        self.processes_grid.SetColLabelValue(3, "PPID")
        self.processes_grid.SetColLabelValue(4, "WCHAN")

        row = 0
        for process_info in final_list_processes:
            self.processes_grid.SetCellValue(row, 0, process_info[0])
            self.processes_grid.SetCellValue(row, 1, process_info[1])
            self.processes_grid.SetCellValue(row, 2, process_info[2])
            self.processes_grid.SetCellValue(row, 3, process_info[3])
            self.processes_grid.SetCellValue(row, 4, process_info[4])
            row += 1

    def on_close_window(self, event):
        self.Destroy()


def show_user_info(username, status, suspicious_apps, check_processes, camera_on, unknown_sources, email):
    """Thread that presents the UserInfo Frame."""
    app = wx.App(False)
    user_frame = UserInfoFrame(username, status, suspicious_apps, check_processes, camera_on, unknown_sources, email)
    user_frame.Show()
    app.MainLoop()
    print("finish1")


class MyFrame(wx.Frame):
    """The main frame of the UI that has Menu Panel and Table Panel."""

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "AMD Server", size=(937, 600))

        self.Center()
        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        splitter = wx.SplitterWindow(self)
        self.menu_panel = MenuPanel(splitter)
        self.table_panel = TablePanel(splitter)
        splitter.SplitVertically(self.menu_panel, self.table_panel)
        splitter.SetSashGravity(0.34)

        set_icon(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.menu_panel.find_user_button.Bind(wx.EVT_BUTTON, self.find_username)
        self.menu_panel.find_user_input.Bind(wx.EVT_TEXT_ENTER, self.find_username)

    def find_username(self, event):
        """The function search username in the table."""
        if self.menu_panel.find_user_input.GetValue().split('\n')[0] == '':
            username = self.menu_panel.find_user_input.GetValue().split('\n')[1]
        else:
            username = self.menu_panel.find_user_input.GetValue()
        self.menu_panel.find_user_input.SetValue('')
        find = False
        for i in range(100):
            check_username = self.table_panel.grid.GetCellValue(i, 0)
            if check_username == username:
                find = True
                status = self.table_panel.grid.GetCellValue(i, 1)
                suspicious_apps = self.table_panel.grid.GetCellValue(i, 2)
                check_processes = self.table_panel.grid.GetCellValue(i, 3)
                camera_on = self.table_panel.grid.GetCellValue(i, 4)
                unknown_sources = self.table_panel.grid.GetCellValue(i, 5)
                email = self.table_panel.grid.GetCellValue(i, 6)
                show_user_info_thread = Thread(target=show_user_info,
                                               args=(username, status, suspicious_apps, check_processes,
                                                     camera_on, unknown_sources, email))
                show_user_info_thread.daemon = True
                show_user_info_thread.start()
                break
        if find is False:
            dlg = wx.MessageDialog(self, "The username: '" + username + "' does'nt exist in the Database. "
                                                                        "try again.", "User Not Found",
                                   style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def on_close_window(self, event):
        """Dialog to verify exit."""
        global FINISH
        dlg = wx.MessageDialog(self, "Are you sure you wan  t to exit AMD Server?", "Confirm Exit",
                               wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            file_object = open("UI data.txt", "w")
            file_object.write("")
            file_object.close()
            FINISH = True
            self.Destroy()

        dlg.Destroy()
