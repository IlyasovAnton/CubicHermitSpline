import wx
from wx import glcanvas
from OpenGL.GL import *

from CubicHermitSpline import *

HERMITE = 1
BEZIER = 2


def clickOnPoint(point, pos, r=5.):
    return (point[0] - pos.x) ** 2 + (point[1] - pos.y) ** 2 < r ** 2


def drawCircle(cx, cy, r):
    glBegin(GL_POLYGON)
    glColor3d(0.25, 0.25, 0.25)
    for t in np.linspace(0, 2*np.pi, 100):
        glVertex2d(cx + (r + 0.2) * np.cos(t) * 0.1, cy + (r + 0.2) * np.sin(t) * 0.1)
    glEnd()


class OpenGlCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        self.size = (800, 800)
        glcanvas.GLCanvas.__init__(self, parent, -1, size=self.size)
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)

        self.mode = HERMITE
        self.KeyPoints = []

        self.Bind(wx.EVT_PAINT, self.OnDraw)
        self.Bind(wx.EVT_MOTION, self.SetPointPos)
        self.Bind(wx.EVT_RIGHT_DOWN, self.RemovePoint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.AppendPoint)
        self.Bind(wx.EVT_MOUSEWHEEL, self.SetTension)

    def SetPointPos(self, event):
        if wx.MouseEvent.Dragging(event):
            pos = event.GetPosition()
            for idx in range(len(self.KeyPoints)):
                if clickOnPoint(self.KeyPoints[idx], pos, 10.):
                    self.KeyPoints[idx][0] = pos.x
                    self.KeyPoints[idx][1] = pos.y
                    if self.mode == HERMITE:
                        self.KeyPoints.sort()
                    break
            self.draw()

    def AppendPoint(self, event):
        pos = event.GetPosition()
        self.KeyPoints.append([pos.x, pos.y, 0.])
        if self.mode == HERMITE:
            self.KeyPoints.sort()

        self.draw()

    def RemovePoint(self, event):
        pos = event.GetPosition()
        for pt in self.KeyPoints:
            if clickOnPoint(pt, pos):
                self.KeyPoints.remove(pt)
                break
        self.draw()

    def SetTension(self, event):
        if self.mode == HERMITE:
            pos = event.GetPosition()
            for idx in range(len(self.KeyPoints)):
                if clickOnPoint(self.KeyPoints[idx], pos, 10.):
                    if wx.MouseEvent.GetWheelRotation(event) > 0 and 1 - self.KeyPoints[idx][2] > 10**(-5):
                        self.KeyPoints[idx][2] += 0.1
                    elif wx.MouseEvent.GetWheelRotation(event) < 0 and self.KeyPoints[idx][2] > 3 * 10**(-17):
                        self.KeyPoints[idx][2] -= 0.1
                    self.draw()

    def OnDraw(self, event):
        self.draw()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.mode == HERMITE:
            self.drawHermitCurve()
        elif self.mode == BEZIER:
            self.drawBezierCurve()

        self.SwapBuffers()

    def drawHermitCurve(self):
        pts = [[2 * pt[0] / self.size[0] - 1., 1 - 2 * pt[1] / self.size[1], pt[2]] for pt in self.KeyPoints]

        for pt in pts:
            drawCircle(*pt)

        if len(pts) > 1:
            spline = CubicHermiteSpline()

            spline.Initialize(pts)
            X, Y = spline.Evaluate()

            glPointSize(1)
            glBegin(GL_LINE_STRIP)
            glColor3d(1, 0.5, 0)
            for x, y in zip(X, Y):
                glVertex(x, y)
            glEnd()

    def drawBezierCurve(self):
        pts = [[2 * pt[0] / self.size[0] - 1., 1 - 2 * pt[1] / self.size[1], 0.] for pt in self.KeyPoints]

        for pt in pts:
            drawCircle(*pt)

        if len(pts) > 1:
            glMap1d(GL_MAP1_VERTEX_3, 0., 1., pts)
            glEnable(GL_MAP1_VERTEX_3)

            glColor3d(1, 0.5, 0)
            glBegin(GL_LINE_STRIP)
            for t in range(101):
                glEvalCoord1d(t/100)
            glEnd()
