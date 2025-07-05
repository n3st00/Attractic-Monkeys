import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

stop_animation = False
#----- PARAMETERS --------------------------------------------------
N = 30
box_size = 4.0
epsilon = 1.0
sigma = 1.0
dt = 0.001
mass = 1.0

MAX_FORCE = 300.0 

wall_thickness = 0.6     
wall_stiffness = 125.0    
#----- INITIAL STATE -----------------------------------------------
positions = np.random.rand(N, 3) * box_size
velocities = np.random.randn(N, 3) * 0.15


#----- FORCE FUNCTIONS ---------------------------------------------
def lennard_jones_force(r_vec):
    r = np.linalg.norm(r_vec)
    if r == 0:
        return np.zeros(3)

    factor = 24 * epsilon * (2 * (sigma**12 / r**13) - (sigma**6 / r**7))
    f = factor * (r_vec / r)

    # Cap the magnitude of the force
    norm = np.linalg.norm(f)
    if norm > MAX_FORCE:
        f = f / norm * MAX_FORCE

    return f


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
            forces[j] -= f  # Newton's third law
            
    # Soft-wall forces
    for i in range(N):
        for dim in range(3):  # x, y, z
            # Distance to low wall
            d_low = positions[i, dim]
            if d_low < wall_thickness:
                forces[i, dim] += wall_stiffness * (wall_thickness - d_low)

            # Distance to high wall
            d_high = box_size - positions[i, dim]
            if d_high < wall_thickness:
                forces[i, dim] -= wall_stiffness * (wall_thickness - d_high)
    return forces

#----- INITIAL ACCELERATIONS ---------------------------------------
forces = compute_forces(positions)
accelerations = forces / mass

#----- PLOTTING SETUP ----------------------------------------------
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, box_size)
ax.set_ylim(0, box_size)
ax.set_zlim(0, box_size)
ax.set_title("3D Lennard-Jones Particle Simulation")

# Create scatter plot
scat = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='blue', s=50)

#----- ANIMATION UPDATE --------------------------------------------
steps_per_frame = 15  
def update_plot(frame):
    global positions, velocities, accelerations

    if stop_animation:
        ani.event_source.stop()
        return scat,
    
    for _ in range(steps_per_frame):
        # --- Position update (Velocity Verlet step 1) ---
        positions += velocities * dt + 0.5 * accelerations * dt**2

        # --- Compute new forces and accelerations ---
        new_forces = compute_forces(positions)
        new_accelerations = new_forces / mass

        # --- Velocity update (Velocity Verlet step 2) ---
        velocities += 0.5 * (accelerations + new_accelerations) * dt
        accelerations[:] = new_accelerations

    # --- Update scatter plot once per visual frame ---
    scat._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])
    return scat,
    

def on_key_press(event):
	global stop_animation
	if event.key.lower() == "b":
		stop_animation = True
		print("Animation stopped")

#----- RUN ANIMATION -----------------------------------------------
ani = FuncAnimation(fig, update_plot, frames=500, interval=30, blit=False)
fig.canvas.mpl_connect('key_press_event', on_key_press)

plt.show()

