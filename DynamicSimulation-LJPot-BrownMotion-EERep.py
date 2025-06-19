import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Parameters ---
num_electrons = 14
nuclei = np.array([[4, 5], [6, 5]])  # fixed positive particles
center = np.mean(nuclei, axis=0)

epsilon = 1.0
sigma = 0.5
dt = 0.05
max_force = 9
boundary_radius = 3.5

brownian_strength = 0.1  # try 0.1 to 0.5 range






# --- Initialization ---
electron_positions = []
for _ in range(num_electrons):
    nucleus = nuclei[np.random.randint(0, 2)]
    pos = nucleus + np.random.normal(0, 0.5, size=2)
    electron_positions.append(pos)
electron_positions = np.array(electron_positions)
electron_velocities = np.zeros_like(electron_positions)

def electron_electron_repulsion(e_idx, positions, k=0.5, min_dist=0.1, max_dist=2.0):
    force = np.zeros(2)
    e_pos = positions[e_idx]
    for j, other_pos in enumerate(positions):
        if j == e_idx:
            continue
        r = e_pos - other_pos
        dist = np.linalg.norm(r)
        if dist < min_dist or dist > max_dist:
            continue
        direction = r / (dist + 1e-5)
        magnitude = k / (dist**2)
        force += magnitude * direction
    return force




# --- Gaussian well Force Function ---
def tether_force(e_pos, sources):
    force = np.zeros(2)
    for s in sources:
        r = e_pos - s
        dist = np.linalg.norm(r)
        direction = r / (dist + 1e-5)

        # Gaussian well force: minimal at preferred distance
        preferred = 1.7  # preferred radius around nucleus
        spring_k = 1.2
        falloff = 3.0

        magnitude = -spring_k * (dist - preferred) * np.exp(-(dist / falloff)**2)
        force += magnitude * direction
    return force


# --- Plot Setup ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("Electrons under Lennard-Jones Attraction/Repulsion")
nucleus_scatter = ax.scatter(nuclei[:, 0], nuclei[:, 1], s=100, color='red', label='Nuclei')
electron_scatter = ax.scatter([], [], s=30, color='blue', label='Electrons')
circle = plt.Circle(center, boundary_radius, color='gray', alpha=0.1)
ax.add_patch(circle)
ax.legend()

dipole_arrow = ax.arrow(center[0], center[1], 0, 0,
                        color='purple', width=0.05, head_width=0.3,
                        label='Dipole')

dipole_text = ax.text(0.5, 9.5, '', fontsize=10, color='purple')



# --- Animation Functions ---
def init():
    electron_scatter.set_offsets(electron_positions)
    return electron_scatter, dipole_arrow, dipole_text

def update(frame):
    global electron_positions, electron_velocities

    for i in range(num_electrons):
        force = tether_force(electron_positions[i], nuclei)
        force += electron_electron_repulsion(i, electron_positions)
        electron_velocities[i] += force * dt
        electron_positions[i] += electron_velocities[i] * dt

        # keep within boundary
        if np.linalg.norm(electron_positions[i] - center) > boundary_radius:
            electron_positions[i] = center + np.random.normal(0, boundary_radius * 0.5, size=2)
            electron_velocities[i] = 0  # reset velocity to prevent escape

    electron_scatter.set_offsets(electron_positions)
    
    force = tether_force(electron_positions[i], nuclei)
    electron_velocities[i] += force * dt
    electron_velocities[i] += np.random.normal(0, brownian_strength, size=2)  # ← added noise
    electron_positions[i] += electron_velocities[i] * dt

    
    # Compute dipole moment (negative sum of displacements)
    dipole_vector = -np.sum(electron_positions - center, axis=0)

    # Remove old arrow and draw new one
    dipole_arrow.remove()
    arrow_scale = 0.1
    new_arrow = ax.arrow(center[0], center[1],
                     dipole_vector[0] * arrow_scale,
                     dipole_vector[1] * arrow_scale,
                     color='purple', width=0.05, head_width=0.3)
    globals()['dipole_arrow'] = new_arrow

    dipole_magnitude = np.linalg.norm(dipole_vector)
    dipole_text.set_text(f'Dipole Magnitude: {dipole_magnitude:.2f}')

    return electron_scatter, dipole_arrow, dipole_text

ani = FuncAnimation(fig, update, frames=300, init_func=init, blit=True, interval=5)
plt.show()

