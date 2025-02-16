import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import keyboard

number_of_particles = 27
particles = []
prticles_clone = []
data = [[0 for n in range(number_of_particles)] for axis in range(3)]
dt = 0.005
sigma = 1
epsilon = 1
cell_s = 10*sigma
cell_n = 27
Ep = []
Ek = []
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

#update coords of particle (we'll give this function to matplotlib's "animation" subroutine)
while True:
    title_string = str(number_of_particles) + "\n" + "sample text"
    pos_file.write(title_string)

    forces_update(particles)
    pos_update(particles)

    #input particles coords into a data list
    for axis in range (3):
        for p in range (number_of_particles):
            data[axis][p] = particles[p].pos[axis]

    #cell borders
    for axis in range(3):
        for p in range(number_of_particles):
            if data[axis][p] > cell_s / 2:
                particles[p].pos[axis] -= cell_s
                particles[p].pos0[axis] -= cell_s
                print(p, "teleported to", particles[p].pos[axis] / sigma)
            if data[axis][p] < -cell_s / 2:
                particles[p].pos[axis] += cell_s
                particles[p].pos0[axis] += cell_s
                print(p, "teleported to", particles[p].pos[axis] / sigma)
    
    pos_file.write("\n")
    if keyboard.is_pressed('q'):
            break

# particles initialization
for i in range(3):
    for j in range(3):
        for k in range(3):
            particles.append(Particle(np.array([-cell_s/4 + cell_s/4 * axis for axis in [i, j, k]]), 
                                    np.array([random.randint(-10, 10)*sigma/10 for axis in range(3)])))
            print(particles[i+j+k].pos)

# data array initialization
data = np.array([[[0 for p in range(number_of_particles)] for axis in range(3)]])
for axis in range (3):
    for p in range (number_of_particles):
        data[0][axis][p] = particles[p].pos[axis]
