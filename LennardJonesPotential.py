import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

stop_animation = False

#-----PARAMETERS--------------------------------------------------
epsilon = 1.0
sigma = 1.0

dt = 0.01
mass = 1.0
#-----/PARAMETERS-------------------------------------------------
particle_positions = np.array([[4.5, 5], [6.5, 5]], dtype=float)
particle_velocities = np.array([[0.05, 0.0], [-0.1, 0.05]]) # set up the initial velocities
# Iiitial acceleration
r_vec = particle_positions[1] - particle_positions[0]

energies = []
time_points = []

#graphs
def compute_energies():
    # Potential Energy = LJ potential
    r_vec = particle_positions[1] - particle_positions[0]
    r = np.linalg.norm(r_vec)
    r_min = 1.12  # minimum allowed distance to avoid spike

    if r < r_min:
        r = r_min

    if r == 0:
        potential = 0
    else:
        potential = 4 * epsilon * ((sigma / r)**12 - (sigma / r)**6)
    return potential


def lennard_jones_force(r_vec):
	r = np.linalg.norm(r_vec)
	if r == 0:
		return np.zeros_like(r_vec)
		
	factor = 24 * epsilon * (2 * (sigma **12 / r **13) - (sigma **6/ r**7))
	return factor * (r_vec / r)
	
	
initial_force = lennard_jones_force(r_vec)	
accelerations = np.array([-initial_force / mass, initial_force / mass])
steps_per_frame = 14  # calculating multiple steps at once
def update(frame):
    global particle_positions, particle_velocities, accelerations

    if stop_animation:
        ani.event_source.stop()
        return particle_plot

    for _ in range(steps_per_frame):
        # updating positions
        particle_positions += particle_velocities * dt + 0.5 * accelerations * dt**2

        # new accels
        r_vec = particle_positions[1] - particle_positions[0]
        force = lennard_jones_force(r_vec)
        new_accelerations = np.array([-force / mass, force / mass])

        # new vls
        particle_velocities += 0.5 * (accelerations + new_accelerations) * dt

        
        accelerations = new_accelerations
        pot = compute_energies()
        energies.append(pot)
        time_points.append(frame + _ / steps_per_frame)

    
    energy_line.set_data(time_points, energies)
    ax_energy.set_xlim(0, max(20, time_points[-1]))
    ax_energy.set_ylim(min(energies) - 0.1, max(energies) + 0.1)

    
    particle_plot[0].set_data(particle_positions[:, 0], particle_positions[:, 1])
    return particle_plot + [energy_line]



def on_key_press(event):
	global stop_animation
	if event.key == 'c':
		stop_animation = True
	print("animation stopped")

fig, (ax, ax_energy) = plt.subplots(2, 1, figsize=(6, 8)) # ENERGY GRAPHS
ax.set_xlim(0, 15)
ax.set_ylim(0, 15)
ax.set_aspect('equal')
ax.set_title("KLennardJonesPotential")

fig.canvas.mpl_connect('key_press_event', on_key_press) #stoppingp the animation

ax_energy.set_xlim(0, 100) ## to calibrate
ax_energy.set_ylim(-1, 1) 
ax_energy.set_title("Potential Energy Over Time")
energy_line, = ax_energy.plot([], [], "r-")



particle_plot = ax.plot(particle_positions[:, 0], particle_positions[:, 1], 'go', markersize=25)

ani = FuncAnimation(fig, update, frames=2000, interval=50, blit=True)

plt.show()

