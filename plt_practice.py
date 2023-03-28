import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np

dt = 0.01
number_of_particles = 2
particles = []
data = [[[0 for p in range(number_of_particles)] for axis in range(3)]]
epsilon = 1
sigma = 0.5

#Particle object
class Particle():
    def __init__(self, position, velocity):
        self.pos = position
        self.pos0 = [0, 0, 0]
        self.v = velocity
        for axis in range(3):
            self.pos0[axis] = self.pos[axis] - self.v[axis]*dt
        self.f = [0, 0, 0]
        self.m = 10

#coords update
def pos_update(particles):
    for p in particles:
        current_pos = [0, 0, 0]
        for axis in range(3):
            current_pos[axis] = p.pos[axis]
            p.pos[axis] = 2*p.pos[axis] - p.pos0[axis] + np.divide(p.f[axis], p.m)
            p.pos0[axis] = current_pos[axis]

def forces_update(particles):
    for p1 in particles:
        for p2 in particles:
            if p1 != p2:
                for axis in range(3):
                    r = p2.pos[axis] - p1.pos[axis]
                    if r == 0:
                        r += 1
                    p1.f[axis] = 0
                    p1.f[axis] += 4*epsilon*(np.divide(6, r) * np.divide(sigma, r)**5 - np.divide(12, r) * np.divide(sigma, r)**11)

#animation function
def plot_update(data):
    forces_update(particles)
    pos_update(particles)
    
    #input particles coords into a data list
    for axis in range(3):
        for p in range(number_of_particles):
            data[axis][p] = particles[p].pos[axis]

    #cell borders
    for axis in range(3):
        for p in range(number_of_particles):
            if data[axis][p] > 40:
                particles[p].pos[axis] -= 80
                particles[p].pos0[axis] -= 80
            if data[axis][p] < -40:
                particles[p].pos[axis] += 80
                particles[p].pos0[axis] += 80

    ax.clear()
    ax.set_xlim3d([-40, 40])
    ax.set_ylim3d([-40, 40])
    ax.set_zlim3d([-40, 40])
    img=[ax.scatter3D(data[0],data[1],data[2],c='red',s=100, alpha = 1)]
    return img

#particle object initialization 
for p in range (number_of_particles):
    particles.append(Particle([random.randint(-20,20) for axis in range(3)], [0, 0, 0]))

#data list filling
for axis in range(3):
        for p in range(number_of_particles):
            data[0][axis][p] = particles[p].pos[axis]

#technical stuff: initiation of figure etc
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
line_ani = animation.FuncAnimation(fig, plot_update, data, interval=1, blit=False)
plt.show()
