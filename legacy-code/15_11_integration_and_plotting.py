"""
This file is the modified integration file that uses arrays and is in general more tidy than before
Does not contain the animation and hence is legacy, in case of emergency
"""

import numpy as np
import matplotlib.pyplot as plt
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
