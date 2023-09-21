import numpy as np
import matplotlib.pyplot as plt

y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
x = [4.121916694, 4.089606209, 3.845817191, 6.110061737, 4.040273298, 2.088766977, 2.031051634, 2.015410209, 3.756663271, 2.160061178]

plt.scatter(x, y, s = 20)
plt.scatter(0, 0, s = 0)
plt.grid()
plt.xlabel("Заряд, Кл ⋅ 10^(-19)")
fig = plt.figure()
plt.show()