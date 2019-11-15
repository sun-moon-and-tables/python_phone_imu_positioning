#importing lists from other files in python: https://stackoverflow.com/a/29267100
from packet_processor import gravPackets
from packet_processor import accPackets
import numpy as np

correctedAccPackets = accPackets.copy()

for j in range(len(accPackets)):
    if correctedAccPackets[0][0] < gravPackets[0][0]:
        correctedAccPackets.pop(0)
    elif correctedAccPackets[-1][0] > gravPackets[-1][0]:
        correctedAccPackets.pop(-1)
    else:
        break

syncedGravPackets = []

largeDeltaT = 0
smallDeltaT = 0
differenceInGravBetweenPackets = []
changeInGravValue = np.zeros(3)
syncedGrav = np.zeros(3)
firstGravValue = np.zeros(3)
# note see john's notes for the explanations, this is basically the gradient we'll be using kinda. just. shut up.
for i in range(len(gravPackets)):

    for j in range(len(correctedAccPackets)):

        if gravPackets[i][0] == correctedAccPackets[j][0]:
            syncedGravPackets.append([correctedAccPackets[j][0], np.array([gravPackets[i][1][0], gravPackets[i][1][1], gravPackets[i][1][2] ]) ])
            break
        elif (gravPackets[i][0] > correctedAccPackets[j][0]) and (gravPackets[i-1][0] < correctedAccPackets[j][0]):
            smallDeltaT = correctedAccPackets[j][0] - gravPackets[i-1][0]
            largeDeltaT = gravPackets[i][0] - gravPackets[i-1][0]
            changeInGravValue = gravPackets[i][1] - gravPackets[i-1][1]
            syncedGrav = (smallDeltaT/largeDeltaT)*changeInGravValue + gravPackets[i-1][1]
            syncedGravPackets.append([correctedAccPackets[j][0], np.around(syncedGrav, 3)])
            break

#np.around is used to round the synced value to 3 decimal places: https://stackoverflow.com/a/46994452
