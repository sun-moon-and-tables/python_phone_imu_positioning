#importing lists from other files in python: https://stackoverflow.com/a/29267100


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
# note see john's notes for the explanations, this is basically the gradient we'll be using kinda.
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

import re as regex
import numpy as np

class data_source_sync:
    """
    This class will have two functions. First will sync all the grav data and acc data. 
    Second function will do the grav synced with the acceleration data.
    """

    def __init__(self, fileList):
        """
        """
        self.fileList = fileList

    def dataSynchroniser(self):
        
    #for j in range(len(self.fileList[0])):


    """
    let's start with the grav stuff, we'll make it more OOP later.
    """
    for i in range(len(firstList)): #this is the number of gravity packets in the first input file. The first 'master'. 
        #This might need some kind of for loop to iterate throught the different lists of data remaining. 
        #another for loop outside should be fine, but that would have to occur AFTER the mean calculations had been made, as we need to find the shortened [i] packet list.
    t = 0    
        for j in range(len(secondList))

            if firstList[i][time] == secondList[j][time]:
                firstListImproved.append( secondList time, (array of firstList data) )
                break
            elif firstList[i-1][time] < secondList[j][time] and firstList[i][time] > secondList[j][time]:
                find the intermediate value of firstList[i] and firstList[i-1] at time, secondList[j]
                firstListImproved.append( secondList time, (array of intermediate firstList[i,i-1] data)
                break
            t += 1
            elif t = len(secondList):
                firstListImproved.append( firstList time, (array of firstList data) )





    for i in range(len(firstListImproved)):
    t = 0
        for j in range(len(secondList)):

            if firstListImproved[i][time] == secondList[j][time]:
                take the average of them.
                master.append(average[ij])
                break
            t += 1
            elif t = (len(secondList)) :
                master.append(firstListImproved[i])
                break

    for j in range(len(secondList)):
    s = 0
        for i in range(len(firstListImproved)):
            if firstListImproved[j][time] == secondList[i][time]:
                break
            s += 1
            elif s = (len(firstListImproved)):
                master.append(secondList[j])
                break



    def syncGravWithAcc(self):









