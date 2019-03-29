import wx
from src.server import config
from src.server.UI.UserInfoFrame import UserInfoFrame


def set_icon(frame):
    if config.WX_VERSION not in wx.version():
        new_icon = wx.EmptyIcon()
    else:
        new_icon = wx.Icon()
    new_icon.CopyFromBitmap(wx.Bitmap(config.ICON_PIC_NAME))
    frame.SetIcon(new_icon)


def show_user_info(username, status, suspicious_apps, check_processes, camera_on, unknown_sources, email):
    app = wx.App(False)
    user_frame = UserInfoFrame(username, status, suspicious_apps, check_processes, camera_on, unknown_sources, email)
    user_frame.Show()
    app.MainLoop()
