from gravity_sync import timesOfAcc
from gravity_sync import correctedVectorOfGrav
from gravity_sync import vectorsOfAcc
from gravity_sync import correctedAccPackets
import numpy as np
import matplotlib.pyplot as plt


accWithoutGrav = []
tempX = 0.0
tempY = 0.0
tempZ = 0.0

for i in range(len(timesOfAcc)):
    timesOfAcc[i] = timesOfAcc[i]/1000


for i in range(len(vectorsOfAcc)):
    tempX = vectorsOfAcc[i][0] - correctedVectorOfGrav[i][0]
    tempY = vectorsOfAcc[i][1] - correctedVectorOfGrav[i][1]
    tempZ = vectorsOfAcc[i][2] - correctedVectorOfGrav[i][2]
    accWithoutGrav.append(np.array([tempX, tempY, tempZ]))
    #soure for correct np array!! https://stackoverflow.com/a/48343452
currentVelocityX = 0.0
currentVelocityY = 0.0
currentVelocityZ = 0.0

currentPositionX = 0.0
currentPositionY = 0.0
currentPositionZ = 0.0


currentVelocityVector = []
currentPostionVector = []

for i in range(len(accWithoutGrav) - 1):
    currentVelocityX = currentVelocityX + (accWithoutGrav[i+1][0] + accWithoutGrav[i][0])*(timesOfAcc[i+1] - timesOfAcc[i])*0.5
    currentVelocityY = currentVelocityY + (accWithoutGrav[i+1][1] + accWithoutGrav[i][1])*(timesOfAcc[i+1] - timesOfAcc[i])*0.5
    currentVelocityZ = currentVelocityZ + (accWithoutGrav[i+1][2] + accWithoutGrav[i][2])*(timesOfAcc[i+1] - timesOfAcc[i])*0.5
    currentVelocityVector.append(np.array([currentVelocityX, currentVelocityY, currentVelocityZ]) )

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
for i in range(len(currentVelocityVector)):
    currentvelX.append(currentVelocityVector[i][0])
    currentvelY.append(currentVelocityVector[i][1])
    currentvelZ.append(currentVelocityVector[i][2])
plt.plot(timesOfVel, currentvelX, '-', label = 'the joyful x values')
plt.plot(timesOfVel, currentvelY, '-', label = 'the joyful y values')
plt.plot(timesOfVel, currentvelZ, '-', label = 'the joyful z values')
plt.xlabel('time')
plt.ylabel('velocity in xyz')
plt.title('Velocity over time')
plt.legend(loc =1)
plt.show()

for i in range(len(currentVelocityVector) - 1):
    currentPositionX = currentPositionX + (currentVelocityVector[i+1][0] + currentVelocityVector[i][0])*(timesOfVel[i+1] - timesOfVel[i])*0.5
    currentPositionY = currentPositionY + (currentVelocityVector[i+1][1] + currentVelocityVector[i][1])*(timesOfVel[i+1] - timesOfVel[i])*0.5
    currentPositionZ = currentPositionZ + (currentVelocityVector[i+1][2] + currentVelocityVector[i][2])*(timesOfVel[i+1] - timesOfVel[i])*0.5
    currentPostionVector.append(np.array([currentPositionX, currentPositionY, currentPositionZ]) )

timesOfPos = timesOfVel.copy()
timesOfPos.pop(0)

currentJOYFULX = []
currentJOYFULY = []
currentJOYFULZ = []

for i in range(len(currentPostionVector)):
    currentJOYFULX.append(currentPostionVector[i][0])
    currentJOYFULY.append(currentPostionVector[i][1])
    currentJOYFULZ.append(currentPostionVector[i][2])

plt.plot(timesOfPos, currentJOYFULX, '-', label = 'the joyful x values')
plt.plot(timesOfPos, currentJOYFULY, '-', label = 'the joyful y values')
plt.plot(timesOfPos, currentJOYFULZ, '-', label = 'the joyful z values')
plt.xlabel('time')
plt.ylabel('position in xyz')
plt.title('Position over time.')
plt.legend(loc = 1)
plt.show()