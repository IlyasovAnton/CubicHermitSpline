import wx
import sys

from MyPanel import MyPanel


class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (800, 800)
        wx.Frame.__init__(self, None, title='curves', size=self.size, pos=(700, 50),
                          style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        self.SetMinSize(self.size)
        self.SetMaxSize(self.size)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.panel = MyPanel(self)

    def on_close(self, event):
        self.Destroy()
        sys.exit(0)
