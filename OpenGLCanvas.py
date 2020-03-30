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

        self.key_points = []

        self.Bind(wx.EVT_PAINT, self.OnDraw)
        self.Bind(wx.EVT_LEFT_DOWN, self.leftMousePressed)

    def leftMousePressed(self, event):
        pos = event.GetPosition()
        pos = (2 * pos.x / self.size[0] - 1., 1 - 2 * pos.y / self.size[1])
        self.key_points.append([pos[0], pos[1], 0.1])
        self.key_points.sort()

        self.draw()

    def OnDraw(self, event):
        self.draw()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.drawHermitCurve()

        self.SwapBuffers()

    def drawHermitCurve(self):
        glPointSize(5)
        glBegin(GL_POINTS)
        glColor3d(1, 0, 0)
        for p in self.key_points:
            glVertex(p[0], p[1])
        glEnd()

        if len(self.key_points) > 1:
            spline = CubicHermiteSpline()
            spline.Initialize(self.key_points)
            X, Y = spline.Evaluate()

            glPointSize(1)
            glBegin(GL_LINE_STRIP)
            glColor3d(1, 0.5, 0)
            for x, y in zip(X, Y):
                glVertex(x, y)
            glEnd()
