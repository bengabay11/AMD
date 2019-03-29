from wx.core import wx
from src.server.UI.utils import set_icon

MALICIOUS_PROCESSES_DICT = {}


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
