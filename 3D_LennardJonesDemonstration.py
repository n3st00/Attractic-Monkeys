import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

#----- PARAMETERS --------------------------------------------------
N = 20                     # number of particles
box_size = 10.0            # Size of the cubic box
epsilon = 1.0              # depth of the potential well
sigma = 1.0                # Characteristic distance
dt = 0.005                 # Time step
mass = 1.0                 # mass of each particle

#----- INITIAL STATE -----------------------------------------------
# random positions inside a box
positions = np.random.rand(N, 3) * box_size

# random initial velocities(small)
velocities = np.random.randn(N, 3) * 0.1

# array for accelerations
accelerations = np.zeros((N, 3))

#----- FUNCTIONS ---------------------------------------------------
def lennard_jones_force(r_vec):
    r = np.linalg.norm(r_vec)
    if r == 0:
        return np.zeros(3)
    factor = 24 * epsilon * (2 * (sigma**12 / r**13) - (sigma**6 / r**7))
    return factor * (r_vec / r)

def compute_forces(positions):
    N = len(positions)
    forces = np.zeros((N, 3))
    for i in range(N):
        for j in range(i + 1, N):
            r_vec = positions[j] - positions[i]
            r = np.linalg.norm(r_vec)
            if r == 0:
                continue
            f = lennard_jones_force(r_vec)
            forces[i] += f
            forces[j] -= f  # newton's third law
    return forces


#----- PLOTTING -------------------------------------------------
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, box_size)
ax.set_ylim(0, box_size)
ax.set_zlim(0, box_size)
ax.set_title("#D Lennard-Jones Particle Simulation")

scat = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='blue', s=50)

def update_plot(frame):
    # Later: insert motion updates here
    scat._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])
    return scat,
    
ani = FuncAnimation(fig, update_plot, frames=2000, interval=50, blit=False)
plt.show()



