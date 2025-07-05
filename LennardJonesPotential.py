import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#-----PARAMETERS--------------------------------------------------
epsilon = 1.0
sigma = 1.0

dt = 0.01
mass = 1.0
#-----/PARAMETERS-------------------------------------------------
particle_positions = np.array([[4.5, 5], [6, 5]], dtype=float)
particle_velocities = np.array([[0.05, 0.0], [-0.05, 0.0]]) # set up the initial velocities

def lennard_jones_force(r_vec):
	r = np.linalg.norm(r_vec)
	if r == 0:
		return np.zeros_like(r_vec)
		
	factor = 24 * epsilon * (2 * (sigma **12 / r **13) - (sigma **6/ r**7))
	return factor * (r_vec / r)
	
	
steps_per_frame = 7  # calculating multiple steps at once
def update(frame):
    global particle_positions, particle_velocities

    for _ in range(steps_per_frame):
        r_vec = particle_positions[1] - particle_positions[0]
        force = lennard_jones_force(r_vec)
        forces = np.array([-force, force])
        particle_velocities += (forces / mass) * dt
        particle_positions += particle_velocities * dt

    particle_plot[0].set_data(particle_positions[:, 0], particle_positions[:, 1])
    return particle_plot


fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.set_title("KLennardJonesPotential")





particle_plot = ax.plot(particle_positions[:, 0], particle_positions[:, 1], 'bo', markersize=10)

ani = FuncAnimation(fig, update, frames=2000, interval=50, blit=True)

plt.show()

