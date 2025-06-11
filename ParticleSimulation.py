import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy


fig, ax = plt.subplots()

ax.set_title("Empty Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
point, = ax.plot([], [], 'bo')

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)


# animation initialization - setst the background
def init():
	point.set_data([], [])
	return point,
	
# animation update function
def update(frame):
	x = frame * 0.1
	y = 0.5
	point.set_data(x, y)
	return point,
	
# animation func
ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True, interval=5, repeat_delay=100, repeat=True)


plt.show()


