import wx
from weather_processor import UI

if __name__ == "__main__":
    app = wx.App()
    frm = UI()
    frm.Show()
    app.MainLoop()
