import numpy as np


class TKeyPoint:
    def __init__(self, t=0., x=0., c=0.):
        self.T = t
        self.X = x
        self.C = c
        self.M = 0.


class CubicHermiteSpline:
    def __init__(self):
        self.idx_prev = 0
        self.KeyPts = []

    def Initialize(self, keyPoints):
        if keyPoints is not None:
            self.KeyPts = [TKeyPoint(*point) for point in keyPoints]

            grad = lambda idx1, idx2: (self.KeyPts[idx2].X - self.KeyPts[idx1].X) /\
                                      (self.KeyPts[idx2].T - self.KeyPts[idx1].T)

            for idx in range(1, len(self.KeyPts) - 1):
                self.KeyPts[idx].M = (1.0 - self.KeyPts[idx].C) * grad(idx - 1, idx + 1)

            self.KeyPts[0].M = grad(0, 1)
            self.KeyPts[-1].M = grad(-2, -1)

    def Evaluate(self):
        dt = 0.001
        T = np.arange(self.KeyPts[0].T, self.KeyPts[-1].T, dt)
        X = []

        for t in T:
            idx = self.FindIdx(t, self.idx_prev)
            if abs(t - self.KeyPts[-1].T) < 1.0e-6:
                idx = len(self.KeyPts) - 2
            if idx < 0 or idx >= len(self.KeyPts) - 1:
                if idx < 0:
                    idx = 0
                    t = self.KeyPts[0].T
                else:
                    idx = len(self.KeyPts) - 2
                    t = self.KeyPts[-1].T

            h00 = lambda t: t * t * (2.0 * t - 3.0) + 1.0
            h10 = lambda t: t * (t * (t - 2.0) + 1.0)
            h01 = lambda t: t * t * (-2.0 * t + 3.0)
            h11 = lambda t: t * t * (t - 1.0)

            self.idx_prev = idx
            p0 = self.KeyPts[idx]
            p1 = self.KeyPts[idx + 1]
            tr = (t - p0.T) / (p1.T - p0.T)

            X.append(h00(tr) * p0.X + h10(tr) * (p1.T - p0.T) * p0.M + h01(tr) * p1.X + h11(tr) * (p1.T - p0.T) * p1.M)
        return T, X

    def FindIdx(self, t, idx_prev=0):
        idx = idx_prev
        if idx >= len(self.KeyPts):
            idx = len(self.KeyPts) - 1
        while idx + 1 < len(self.KeyPts) and t > self.KeyPts[idx + 1].T:
            idx += 1
        while idx >= 0 and t < self.KeyPts[idx].T:
            idx -= 1
        return idx
