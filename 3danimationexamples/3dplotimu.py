from integration_and_plotting import timesOfPos
from integration_and_plotting import currentposX
from integration_and_plotting import currentposY
from integration_and_plotting import currentposZ

from matplotlib import pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation

fig = plt.figure()
ax = p3.Axes3D(fig)

def gen():
    i = 0
    while i < len(timesOfPos):
        yield np.array([currentposX[i], currentposY[i], currentposZ[i]])
        i += 1

def update(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])

data = np.array(list(gen())).T
line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])

#Setting the axes properties
ax.set_xlim3d([-2, 2])
ax.set_xlabel('X')

ax.set_ylim3d([-2, 2])
ax.set_ylabel('Y')

ax.set_zlim3d([-2, 2])
ax.set_zlabel('Z')

ani = animation.FuncAnimation(fig, update, len(timesOfPos), fargs=(data, line), interval=1, blit=False)
#ani.save('matplot003.gif', writer='imagemagick')
plt.show()

#where this came from: https://stackoverflow.com/q/38118598