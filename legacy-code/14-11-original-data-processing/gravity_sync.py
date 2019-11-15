"""
this is the original gravity sync code, that didn't make good use of arrays
"""


#importing lists from other files in python: https://stackoverflow.com/a/29267100
from string_processor_for_ryan_app import gravPackets
from string_processor_for_ryan_app import accPackets

timesOfGrav = []
timesOfAcc = []
vectorsOfGrav = []
vectorsOfAcc = []
correctedAccPackets = accPackets.copy()


for i in range(len(gravPackets)):
    timesOfGrav.append(gravPackets[i][0])

for i in range(len(accPackets)):
    timesOfAcc.append(accPackets[i][0])

for i in range(len(gravPackets)):
    vectorsOfGrav.append([gravPackets[i][1], gravPackets[i][2], gravPackets[i][3]])

for i in range(len(accPackets)):
    vectorsOfAcc.append([accPackets[i][1], accPackets[i][2], accPackets[i][3]])


for j in range(len(timesOfAcc)):
    if timesOfAcc[0] < timesOfGrav[0]:
        timesOfAcc.pop(0)
        vectorsOfAcc.pop(0)
        correctedAccPackets.pop(0)
    elif timesOfGrav[-1] < timesOfAcc[-1]:
        timesOfAcc.pop(-1)
        correctedAccPackets.pop(-1)

# we now have the acceleration list shortened so that we can work with it.

correctedGravPackets = []

correctedVectorOfGrav = []

largeDeltaT = 0
smallDeltaT = 0
shiftInGravX = 0.0
shiftInGravY = 0.0
shiftInGravZ = 0.0
corGravX = 0.0
corGravY = 0.0
corGravZ = 0.0

# note see john's notes for the explanations, this is basically the gradient we'll be using kinda.
for i in range(len(timesOfGrav)):

    for j in range(len(timesOfAcc)):
        if timesOfGrav[i] == timesOfAcc[j]:
            correctedGravPackets.append([timesOfAcc[j], vectorsOfGrav[i][0], vectorsOfGrav[i][1], vectorsOfGrav[i][2]])
            correctedVectorOfGrav.append([vectorsOfGrav[i][0], vectorsOfGrav[i][1], vectorsOfGrav[i][2]])
            break
        elif (timesOfGrav[i] > timesOfAcc[j]) and (timesOfGrav[i-1] < timesOfAcc[j]):
            largeDeltaT = timesOfGrav[i] - timesOfGrav[i-1]
            smallDeltaT = timesOfAcc[j] - timesOfGrav[i-1]
            shiftInGravX = vectorsOfGrav[i][0] - vectorsOfGrav[i-1][0]
            shiftInGravY = vectorsOfGrav[i][1] - vectorsOfGrav[i-1][1]
            shiftInGravZ = vectorsOfGrav[i][2] - vectorsOfGrav[i-1][2]
            
            corGravX = (smallDeltaT/largeDeltaT)*shiftInGravX + vectorsOfGrav[i-1][0]
            corGravY = (smallDeltaT/largeDeltaT)*shiftInGravY + vectorsOfGrav[i-1][1]
            corGravZ = (smallDeltaT/largeDeltaT)*shiftInGravZ + vectorsOfGrav[i-1][2]

            correctedGravPackets.append([timesOfAcc[j], corGravX, corGravY, corGravZ])
            correctedVectorOfGrav.append([corGravX, corGravY, corGravZ])
            break
