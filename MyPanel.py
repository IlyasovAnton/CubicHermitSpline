import wx

from OpenGLCanvas import OpenGlCanvas


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#626D58')
        self.canvas = OpenGlCanvas(self)
