import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.set_title("KLennardJonesPotential")


particle_positions = np.array([[3, 5], [7, 5]])


particle_plot = ax.plot(particle_positions[:, 0], particle_positions[:, 1], 'bo', markersize=10)

plt.show()

