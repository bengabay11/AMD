import wx
from src.server import config


class MenuPanel(wx.Panel):

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
