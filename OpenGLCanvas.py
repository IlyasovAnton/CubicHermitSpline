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

        self.c = [0.1, 0.1, 0.1, 0.1, 0.1]
        random.seed(228)
        self.key_points = [[random.random() * 2. - 1., random.random() * 2. - 1., self.c] for i in range(5)]
        self.key_points.sort()

        self.Bind(wx.EVT_PAINT, self.OnDraw)

    def OnDraw(self, event):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.key_points = [[p[0], p[1], c] for p, c in zip(self.key_points, self.c)]
        self.drawHermitCurve()

        self.SwapBuffers()

    def drawHermitCurve(self):
        glPointSize(5)
        glBegin(GL_POINTS)
        glColor3d(1, 0, 0)
        for p in self.key_points:
            glVertex(p[0], p[1])
        glEnd()

        spline = CubicHermiteSpline()
        spline.Initialize(self.key_points)
        X, Y = spline.Evaluate()

        glPointSize(1)
        glBegin(GL_LINE_STRIP)
        glColor3d(1, 0.5, 0)
        for x, y in zip(X, Y):
            glVertex(x, y)
        glEnd()
