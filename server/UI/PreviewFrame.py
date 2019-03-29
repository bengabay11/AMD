import wx
from server import config


class PreviewFrame(wx.Frame):
    """The main frame of the UI that has Menu Panel and Table Panel."""

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "AMD Server", size=(500, 250))

        self.Center()

        # set background to the MenuPanel
        self.SetBackgroundColour("LIGHT BLUE")

        self.title = wx.StaticText(self, label="AMD Server", pos=(40, 30))
        font = wx.Font(35, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.title.SetFont(font)
        self.title.SetForegroundColour(wx.BLUE)

        img = wx.Image(config.ICON_PIC_NAME, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(self, -1, img, pos=(325, 10), size=(100, 100))

        self.start_button = wx.Button(self, label="Start Listening...", pos=(190, 120), size=(120, 50))
        self.start_button.Bind(wx.EVT_BUTTON, self.on_listening)

        set_icon(self)

    def on_listening(self, event):
        """the function destroy the frame, and notify the main thread to start the server."""
        global START
        START = True
        self.Destroy()
