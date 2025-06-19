import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

## initialize params
num_electrons = 14
dt = 0.1
teleport_stddev = 0.5 # jump size
boundary_radius = 3.5 # boundary around the center

#nucleus positions
nuclei = np.array([[4, 5], [6, 5]])
center = np.mean(nuclei, axis=0)

#initialize electrons randomly near nuclei
electron_positions = []
for _ in range(num_electrons):
	nucleus = nuclei[np.random.randint(0, 2)] #pick a random nucleus
	pos = nucleus + np.random.normal(0, 0.5, size=2)
	electron_positions.append(pos)
electron_positions = np.array(electron_positions)

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title("Empty Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
nucleus_scatter = ax.scatter(nuclei[:, 0], nuclei[:, 1], s=100, color='red', label='Nuclei')
electron_scatter = ax.scatter([], [], s=30, color='blue', label='Electrons')
circle = plt.Circle(center, boundary_radius, color='gray', alpha=0.1)
ax.add_patch(circle)
ax.set_title("Electron Fluctuations Around Ethane-Like Molecule")
ax.legend()



# animation initialization - setst the background
def init():
	electron_scatter.set_offsets(electron_positions)
	return electron_scatter,
	
# animation update function
def update(frame):
	global electron_positions
	
	jumps = np.random.normal(0, teleport_stddev, size=electron_positions.shape)
	new_positions = electron_positions + jumps
	
	# checking for boundaries
	for i, pos in enumerate(new_positions):
		if np.linalg.norm(pos - center) > boundary_radius:
			# Re-teleport to random point near center
			new_positions[i] = center + np.random.normal(0, boundary_radius * 0.5, size=2)
    
	electron_positions[:] = new_positions
	electron_scatter.set_offsets(electron_positions)
	
	return electron_scatter,
	
# animation func
ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True, interval=500, repeat_delay=100, repeat=True)


plt.show()


