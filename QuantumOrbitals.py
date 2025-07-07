import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set seed for reproducibility
np.random.seed(42)

# Number of points in the cloud
N = 50000

# Maximum radius to consider
r_max = 10

# Rejection sampling for radial distribution: P(r) ∝ r^2 * exp(-2r)
def sample_radial(n_samples):
    samples = []
    while len(samples) < n_samples:
        r = np.random.uniform(0, r_max)
        p = r**2 * np.exp(-2*r)
        threshold = np.random.uniform(0, 1.5)  # 1.5 is approximate max of p(r)
        if threshold < p:
            samples.append(r)
    return np.array(samples)

# Uniform sampling of angles
theta = np.arccos(1 - 2 * np.random.rand(N))   # θ ∈ [0, π]
phi = 2 * np.pi * np.random.rand(N)            # φ ∈ [0, 2π]
r = sample_radial(N)

# Convert to Cartesian coordinates
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)

# Plotting the point cloud
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, s=0.1, alpha=0.1, color='blue')
ax.set_title("Hydrogen 1s Orbital (Probability Cloud)", fontsize=14)
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])
ax.set_axis_off()
plt.show()

