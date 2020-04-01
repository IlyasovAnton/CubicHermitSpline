import wx

from OpenGLCanvas import *


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.radioButtonHermite = wx.RadioButton(self, -1, pos=(680, 10))
        self.radioButtonHermite.SetBackgroundColour('Black')
        self.labelHermite = wx.StaticText(self, -1, 'Hermite curve', pos=(700, 10))
        self.labelHermite.SetBackgroundColour('Black')
        self.labelHermite.SetForegroundColour('White')

        self.radioButtonBezier = wx.RadioButton(self, -1, pos=(680, 30))
        self.radioButtonBezier.SetBackgroundColour('Black')
        self.labelBezier = wx.StaticText(self, -1, 'Bezier curve', pos=(700, 30))
        self.labelBezier.SetBackgroundColour('Black')
        self.labelBezier.SetForegroundColour('White')

        self.canvas = OpenGlCanvas(self)

        self.Bind(wx.EVT_RADIOBUTTON, self.SetHermite, self.radioButtonHermite)
        self.Bind(wx.EVT_RADIOBUTTON, self.SetBezier, self.radioButtonBezier)

    def SetHermite(self, event):
        self.canvas.mode = HERMITE
        self.canvas.Refresh()

    def SetBezier(self, event):
        self.canvas.mode = BEZIER
        self.canvas.Refresh()
