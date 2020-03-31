import numpy as np


class KeyPoint:
    def __init__(self, t=0., x=0., c=0., m=0.):
        self.T = t
        self.X = x
        self.C = c
        self.M = m

    def __str__(self):
        return f"KeyPoint({self.T}, {self.X}, {self.C}, {self.M})"

    def __repr__(self):
        return f"KeyPoint({self.T}, {self.X}, {self.C}, {self.M})\n"


class CubicHermiteSpline:
    def __init__(self):
        self.KeyPts = []

    def __str__(self):
        return self.KeyPts.__repr__()

    def Initialize(self, keyPoints):
        def grad(idx):
            if idx == 0 or idx == -1:
                return (self.KeyPts[2*idx+1].X - self.KeyPts[2*idx].X) / (self.KeyPts[2*idx+1].T - self.KeyPts[2*idx].T)
            else:
                return (self.KeyPts[idx+1].X - self.KeyPts[idx-1].X) / (self.KeyPts[idx+1].T - self.KeyPts[idx-1].T)

        self.KeyPts = [KeyPoint(*point) for point in keyPoints]

        for idx in range(1, len(self.KeyPts) - 1):
            self.KeyPts[idx].M = (1.0 - self.KeyPts[idx].C) * grad(idx)

        self.KeyPts[0].M = grad(0)
        self.KeyPts[-1].M = grad(-1)

    def Evaluate(self, dt=0.001):
        X = []
        Y = []
        for idx in range(1, len(self.KeyPts)):
            pt1 = self.KeyPts[idx-1]
            pt2 = self.KeyPts[idx]

            Xrange = np.linspace(pt1.T, pt2.T, num=int((pt2.T-pt1.T)/dt))
            X.extend(Xrange)
            for x in Xrange:
                h00 = lambda a: a * a * (2.0 * a - 3.0) + 1.0
                h10 = lambda a: a * (a * (a - 2.0) + 1.0)
                h01 = lambda a: a * a * (-2.0 * a + 3.0)
                h11 = lambda a: a * a * (a - 1.0)

                t = (x - pt1.T) / (pt2.T - pt1.T)
                p = h00(t) * pt1.X + h10(t) * (pt2.T - pt1.T) * pt1.M + h01(t) * pt2.X + h11(t) * (pt2.T - pt1.T) * pt2.M
                Y.append(p)
        return X, Y
