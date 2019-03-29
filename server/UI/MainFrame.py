from threading import Thread
import wx
from server.UI.TablePanel import TablePanel
from server.UI.utils import set_icon, show_user_info


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "AMD Server", size=(937, 600))

        self.Center()
        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        splitter = wx.SplitterWindow(self)
        self.menu_panel = splitter
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
        dlg = wx.MessageDialog(self, "Are you sure you want to exit AMD Server?", "Confirm Exit",
                               wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            file_object = open("UI data.txt", "w")
            file_object.write("")
            file_object.close()
            FINISH = True
            self.Destroy()

        dlg.Destroy()
