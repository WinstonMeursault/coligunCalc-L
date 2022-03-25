# common.py

from math import e, pi, pow, sqrt

import numpy as np

from scipy.integrate import quad
from scipy.special import j0, j1, struve
from scipy.special import ellipe as eE
from scipy.special import ellipk as eK


μ0 = 4 * pi * pow(10, -7)


def L(coilA, limit = 125):
    p = coilA.re / coilA.ri
    q = coilA.l / coilA.ri
        
    # U = lambda x: quad(lambda x: x * j1(x), x, p * x)[0] / pow(x, 3)
    U = lambda x: pi * (-j1(x) * struve(0, x)  +  p * j1(p * x) * struve(0, p * x)  + j0(x) * struve(1, x)  -  p * j0(p * x) * struve(1, p * x)) / (2 * pow(x,2))
        
    integrationT = lambda x: pow(U(x), 2) * (q * x  +  pow(e,(-1 * q * x))  -  1)
    T = quad(integrationT, 0, np.inf, limit = limit)[0]
        
    return 2 * pi * μ0 * np.power(coilA.nc, 2) * np.power(coilA.ri, 5) * T

def calcK(coilA, coilB, d):
    return sqrt((4 * coilA.r * coilB.r) / (pow((coilA.r + coilB.r), 2) + pow(d, 2)))

def M(coilA, coilB, d = None):
    if d == None:
        d = abs(coilA.x - coilB.x)
    k = calcK(coilA, coilB, d)

    return μ0 * sqrt(coilA.r * coilB.r) * ((2 / k - k) * eK(k) - (2 / k) * eE(k))

def dM(coilA, coilB, d = None):
    if d == None:
        d = abs(coilA.x - coilB.x)
    k = calcK(coilA, coilB, d)

    return (μ0 * k * d * (2 * (1 - pow(k, 2)) * eK(k) - (2 - pow(k, 2)) * eE(k))) / (4 * (1 - pow(k, 2)) * sqrt(coilA.r * coilB.r))


class drivingCoil():
    def __init__(self,rdi, rde, ld, n, x0, resistivity, s, k):
        self.ri = rdi
        self.re = rde
        self.l = ld
        self.n = n                      # 线圈匝数
        self.x = x0
        self.SR = resistivity           # 电阻率
        self.s = s                      # 单根导线的截面积
        self.k = k                      # 驱动线圈填充率
        
        self.r = (self.ri + self.re) / 2
        Sd = (self.re - self.ri) * self.l
        
        self.nc = self.n / Sd
        
        self.R = self.R()
        self.L = L(self)

    def R(self):
        return (self.SR * self.k * pi * (pow(self.re, 2) - pow(self.ri, 2)) * self.l) / pow(self.s, 2)

class armature():
    def __init__(self,rai, rae, la, x0, resistivity, m, n):
        self.ri = rai
        self.re = rae
        self.l = la
        self.x = x0
        self.SR = resistivity
        self.m = m
        self.n = n
        
        self.currentFilaments = {}
        for i in range(1, self.m + 1):
            for j in range(1, self.n + 1):
                self.currentFilaments[i][j] = {
                    "r": None,
                    "R":None,
                    "L":None
                }
    
    def R(self):
        deltaR = 2 * pi * self.SR * self.m / self.l
        for k in self.currentFilaments:
            for l in range(1, self.m + 1):
                pass    # TODO
    
    def updatePosition(self, delta):
        self.x += delta