import wx

from MyFrame import MyFrame


class myApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    app = myApp()
    app.MainLoop()
