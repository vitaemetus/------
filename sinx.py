import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(0, 5, 5001)
y = [0]
delta = 0
delta_list = []

for i in range(len(x) - 1):
    y.append(y[i] + np.sin(x[i + 1])*(x[i + 1] - x[i]))
    delta += np.abs(y[i] - np.sin(x[i]))
    delta_list.append(np.abs(y[i] - np.sin(x[i])))
delta = delta / len(x)

print("points: ", len(x))
print("deviation: ", delta)

plt.plot(x, y)
plt.show()
