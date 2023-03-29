import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

number_of_particles = 27
particles = []
prticles_clone = []
dt = 0.01
sigma = 1
epsilon = 1
cell_s = 10*sigma
cell_n = 27
Ep = [0]
Ek = [0]
T = [0]
pos_file = open('pos.xyz', 'w')

class Particle():
    def __init__(self, position, velocity):
        self.pos = position
        self.pos0 = np.array([0, 0, 0])
        self.v = velocity
        self.pos0 = self.pos - self.v*dt
        self.f = np.array([0.0, 0.0, 0.0])
        self.m = 1

def pos_update(particles):
    for i, p in enumerate(particles):
        current_pos = p.pos
        p.pos = 2*p.pos - p.pos0 + np.divide(p.f, p.m)*dt**2
        p.pos0 = current_pos
        pos_string = '\n' + str(i) + " " + str(p.pos[0]) + " " + str(p.pos[1]) + " " + str(p.pos[2])
        pos_file.write(pos_string)

def forces_update(particles):
    for p1 in particles:
        p1.f = np.array([0, 0, 0])
        for p2 in particles:
            if p1 != p2:
                r = np.array(p2.pos - p1.pos)
                for axis in range(3):
                    if r[axis] > cell_s / 2:
                        r[axis] -= cell_s
                    if r[axis] < -cell_s / 2:
                        r[axis] += cell_s
                r_norm = np.linalg.norm(r)
                r_norm /= sigma
                s = (sigma / r_norm)**6
                p1.f = p1.f + ((24*epsilon*(2*s**2 - s)) / (r_norm**2)) * r

def energy_update(particles):
    Ek = 0
    Ep = 0
    for p1 in particles:
        p1.f = np.array([0, 0, 0])
        Ek += np.linalg.norm((p1.pos - p1.pos0) / dt)**2*p1.m/2
        for p2 in particles:
            if p1 != p2:
                r = np.array(p2.pos - p1.pos)
                for axis in range(3):
                    if r[axis] > cell_s / 2:
                        r[axis] -= cell_s
                    if r[axis] < -cell_s / 2:
                        r[axis] += cell_s
                r_norm = np.linalg.norm(r)
                s = (sigma / r_norm)**6
                Ep -= 4*epsilon*(s**2 - s)
    return(Ek, Ep/2)
                

#update coords of particle (we'll give this function to matplotlib's "animation" subroutine)
def plot_update(data):
    title_string = str(number_of_particles) + "\n" + "sample text"
    pos_file.write(title_string)

    forces_update(particles)
    pos_update(particles)

    E_vals = energy_update(particles)
    Ek.append(E_vals[0])
    Ep.append(E_vals[1])
    T.append(T[len(T) - 1] + dt)

    #cell borders
    for axis in range(3):
        for p in range(number_of_particles):
            if particles[p].pos[axis] > cell_s / 2:
                particles[p].pos[axis] -= cell_s
                particles[p].pos0[axis] -= cell_s
            if particles[p].pos[axis] < -cell_s / 2:
                particles[p].pos[axis] += cell_s
                particles[p].pos0[axis] += cell_s
    
    #input particles coords into a data list
    for axis in range (3):
        for p in range (number_of_particles):
            data[axis][p] = particles[p].pos[axis]        

    for i in range(3):
        ax[i].clear()
    ax[0].set_xlim3d([-cell_s/2, cell_s/2])
    ax[0].set_ylim3d([-cell_s/2, cell_s/2])
    ax[0].set_zlim3d([-cell_s/2, cell_s/2])
    img=[ax[0].scatter3D(data[0],data[1],data[2],c='red', alpha = 1,s=10),
         ax[1].plot(T, Ek, label = 'Kinetic energy'),
         ax[1].plot(T, Ep, label = 'Potential energy'),
         ax[1].plot(T, np.array(Ep) + np.array(Ek), label = 'Full energy')]

    ax[1].legend(loc = 'upper left')
    pos_file.write("\n")
    return img

# particles initialization
for i in range(3):
    for j in range(3):
        for k in range(3):
            if len(particles) >= number_of_particles:
                break
            particles.append(Particle(np.array([-cell_s/4 + cell_s/4 * axis for axis in [i, j, k]]),
                                      np.array([random.randint(-10, 10)*sigma/10 for axis in range(3)])))

#np.array([random.randint(-10, 10)*sigma/10 for axis in range(3)])

#energy initialization
E_vals = energy_update(particles)
Ek[0] = E_vals[0]
Ep[0] = E_vals[1]

# data array initialization
data = [[[0 for p in range(number_of_particles)] for axis in range(3)]]
for axis in range (3):
    for p in range (number_of_particles):
        data[0][axis][p] = particles[p].pos[axis]

#technical stuff: initiation of figure etc
fig = plt.figure()
ax0 = fig.add_subplot(1,2,1, projection='3d')
ax1 = fig.add_subplot(2,2,2)
ax2 = fig.add_subplot(2,2,4)
ax = [ax0, ax1, ax2]
line_ani = animation.FuncAnimation(fig, plot_update, data, interval = 1, blit=False)
plt.show()
