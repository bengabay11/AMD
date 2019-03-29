import wx
from server import config


def set_icon(frame):
    """Set icon for frame"""
    if "3.0" in wx.version():
        new_icon = wx.EmptyIcon()
    else:
        new_icon = wx.Icon()
    new_icon.CopyFromBitmap(wx.Bitmap(config.ICON_PIC_NAME))
    frame.SetIcon(new_icon)
