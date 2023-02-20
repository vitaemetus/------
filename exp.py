import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(0, 5, 421)
y = [0]
delta = 0

for i in range(len(x) - 1):
    y.append(y[i] + np.exp(x[i + 1])*(x[i + 1] - x[i]))

delta = np.abs(y[len(y) - 1] - np.exp(x[len(x) - 1]))

print("points: ", len(x))
print("deviation: ", delta)
