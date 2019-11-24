import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation

from grav_sync_with_acc import correctedAccPackets
from grav_sync_with_acc import syncedGravPackets


accWithoutGrav = []

for i in range(len(correctedAccPackets)):
    correctedAccPackets[i][0] = correctedAccPackets[i][0]/1000


for i in range(len(correctedAccPackets)):
    accWithoutGrav.append(correctedAccPackets[i][1] - syncedGravPackets[i][1])
    #soure for correct np array!! https://stackoverflow.com/a/48343452

velocityVector = []
postionVector = []

timesOfAcc = []

for i in range(len(correctedAccPackets)):
    timesOfAcc.append(correctedAccPackets[i][0])

tempVelocity = np.zeros(3)
for i in range(len(accWithoutGrav) - 1):
    tempVelocity = tempVelocity + (accWithoutGrav[i+1] + accWithoutGrav[i])*(correctedAccPackets[i+1][0] - correctedAccPackets[i][0])*0.5
    velocityVector.append(tempVelocity)

timesOfVel = timesOfAcc.copy()
timesOfVel.pop(0)

currentaccX = []
currentaccY = []
currentaccZ = []
for i in range(len(accWithoutGrav)):
    currentaccX.append(accWithoutGrav[i][0])
    currentaccY.append(accWithoutGrav[i][1])
    currentaccZ.append(accWithoutGrav[i][2])
plt.plot(timesOfAcc, currentaccX, '-', label = 'the joyful x values')
plt.plot(timesOfAcc, currentaccY, '-', label = 'the joyful y values')
plt.plot(timesOfAcc, currentaccZ, '-', label = 'the joyful z values')
plt.xlabel('time')
plt.ylabel('acceleartion without grav')
plt.title('Acceleration over time')
plt.legend(loc = 1)
plt.show()

currentvelX = []
currentvelY = []
currentvelZ = []
for i in range(len(velocityVector)):
    currentvelX.append(velocityVector[i][0])
    currentvelY.append(velocityVector[i][1])
    currentvelZ.append(velocityVector[i][2])
plt.plot(timesOfVel, currentvelX, '-', label = 'the joyful x values')
plt.plot(timesOfVel, currentvelY, '-', label = 'the joyful y values')
plt.plot(timesOfVel, currentvelZ, '-', label = 'the joyful z values')
plt.xlabel('time')
plt.ylabel('velocity in xyz')
plt.title('Velocity over time')
plt.legend(loc =1)
plt.show()


tempPosition = np.zeros(3)
for i in range(len(velocityVector) - 1):
    tempPosition = tempPosition + (velocityVector[i+1] + velocityVector[i])*(timesOfVel[i+1] - timesOfVel[i])*0.5
    postionVector.append(tempPosition)

timesOfPos = timesOfVel.copy()
timesOfPos.pop(0)

currentposX = []
currentposY = []
currentposZ = []

for i in range(len(postionVector)):
    currentposX.append(postionVector[i][0])
    currentposY.append(postionVector[i][1])
    currentposZ.append(postionVector[i][2])

plt.plot(timesOfPos, currentposX, '-', label = 'the joyful x values')
plt.plot(timesOfPos, currentposY, '-', label = 'the joyful y values')
plt.plot(timesOfPos, currentposZ, '-', label = 'the joyful z values')
plt.xlabel('time')
plt.ylabel('position in xyz')
plt.title('Position over time.')
plt.legend(loc = 1)
plt.show()

"""at this point, we have the new 3D animation code.
This has been cobbled together from various sources, but
mainly from matplotlibanimator.py, after using matplotlibanimator_3.py 
to understand the core concepts.
"""

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

#source: https://stackoverflow.com/a/38121759
