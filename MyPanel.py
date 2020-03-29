import wx

from OpenGLCanvas import OpenGlCanvas


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#626D58')
        self.canvas = OpenGlCanvas(self)

        # тестовая херня, можно убирать
        self.sliderTitle = wx.StaticText(self, -1, 'параметр с', pos=(800, 230),
                                         size=(200, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.slider1 = wx.Slider(self, -1, pos=(800, 250), size=(200, 50), style=wx.SL_HORIZONTAL)

        self.sliderTitle = wx.StaticText(self, -1, 'параметр с', pos=(800, 330),
                                         size=(200, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.slider2 = wx.Slider(self, -1, pos=(800, 350), size=(200, 50), style=wx.SL_HORIZONTAL)

        self.sliderTitle = wx.StaticText(self, -1, 'параметр с', pos=(800, 430),
                                         size=(200, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.slider3 = wx.Slider(self, -1, pos=(800, 450), size=(200, 50), style=wx.SL_HORIZONTAL)

        self.sliderTitle = wx.StaticText(self, -1, 'параметр с', pos=(800, 530),
                                         size=(200, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.slider4 = wx.Slider(self, -1, pos=(800, 550), size=(200, 50), style=wx.SL_HORIZONTAL)

        self.sliderTitle = wx.StaticText(self, -1, 'параметр с', pos=(800, 630),
                                         size=(200, 20), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.slider5 = wx.Slider(self, -1, pos=(800, 650), size=(200, 50), style=wx.SL_HORIZONTAL)

        # обработка событий
        self.Bind(wx.EVT_SLIDER, self.setParamC1, self.slider1)
        self.Bind(wx.EVT_SLIDER, self.setParamC2, self.slider2)
        self.Bind(wx.EVT_SLIDER, self.setParamC3, self.slider3)
        self.Bind(wx.EVT_SLIDER, self.setParamC4, self.slider4)
        self.Bind(wx.EVT_SLIDER, self.setParamC5, self.slider5)

    def setParamC1(self, event):
        self.canvas.c[0] = self.slider1.GetValue() / 100
        self.canvas.Refresh()

    def setParamC2(self, event):
        self.canvas.c[1] = self.slider2.GetValue() / 100
        self.canvas.Refresh()

    def setParamC3(self, event):
        self.canvas.c[2] = self.slider3.GetValue() / 100
        self.canvas.Refresh()

    def setParamC4(self, event):
        self.canvas.c[3] = self.slider4.GetValue() / 100
        self.canvas.Refresh()

    def setParamC5(self, event):
        self.canvas.c[4] = self.slider5.GetValue() / 100
        self.canvas.Refresh()