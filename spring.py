import numpy as np
import time

class Particle:
    def __init__(self, mass, position, velocity):
        self.m = mass
        self.x = position
        self.v = velocity
        self.x0 = self.x - self.v * dt

class Spring:
    def __init__(self, stretch, k):
        self.x = stretch
        self.k = k

def calc(p1, s1):
    # динамика
    current_x = p1.x
    s1.x = p1.x
    p1.x = 2*p1.x - np.divide(s1.x*s1.k, p1.m) * (dt**2) - p1.x0
    p1.x0 = current_x
    p1.v = np.divide(abs(p1.x - p1.x0), dt)

def calc_E(p1, s1):
    # энергия
    E = (p1.m * p1.v**2 + s1.k * s1.x**2) / 2
    return(E)

ongoing = True
dt = 0.1
p1 = Particle(1, 0, 0.1)
s1 = Spring(p1.x, 0.5)

while ongoing:
    calc(p1, s1)    # шаг интегрирования
    print(calc_E(p1, s1))   # вывод механической энергии системы
