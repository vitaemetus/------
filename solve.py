import matplotlib.pyplot as plt
import numpy as np

#initial parameters
h=0.001
x_min, x_max = 0, 10
x=np.linspace(x_min,x_max,int((x_max-x_min)/h))
y=np.zeros(len(x))
y[0]=0

#calculating y(x)
for i in range(len(x)-1):
    y[i+1]=y[i]+(x[i+1]-x[i])*np.exp(x[i])

#exact solution
x_exact=np.linspace(x_min,x_max,1000)
y_exact=np.exp(x_exact)

delta = abs(y[len(y) - 1] - np.exp(5))
print(delta)

plt.plot(x,y,'r.-')
plt.plot(x_exact,y_exact,'b.-')
plt.show()

