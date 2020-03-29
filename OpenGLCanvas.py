import random

import wx
from wx import glcanvas
from OpenGL.GL import *

from CubicHermitSpline import *


class OpenGlCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        self.size = (800, 800)
        glcanvas.GLCanvas.__init__(self, parent, -1, size=self.size)
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)

        self.Bind(wx.EVT_PAINT, self.OnDraw)

    def OnDraw(self, event):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.drawHermitCurve()

        self.SwapBuffers()

    def drawHermitCurve(self):
        key_points = [[random.random() * 2. - 1., random.random() * 2. - 1., 0.9] for i in range(5)]
        key_points.sort()

        glPointSize(5)
        glBegin(GL_POINTS)
        glColor3d(1, 0, 0)
        for p in key_points:
            glVertex(p[0], p[1])
        glEnd()

        spline = CubicHermiteSpline()
        spline.Initialize(key_points)
        X, Y = spline.Evaluate()

        glPointSize(1)
        glBegin(GL_LINE_STRIP)
        glColor3d(1, 0.5, 0)
        for x, y in zip(X, Y):
            glVertex(x, y)
        glEnd()
