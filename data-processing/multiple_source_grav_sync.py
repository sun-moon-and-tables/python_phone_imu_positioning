#importing lists from other files in python: https://stackoverflow.com/a/29267100
import copy
import numpy as np


class multi_data_source_sync:
    """
    This class will have two functions. First will sync all the grav data and acc data. 
    Second function will do the grav synced with the acceleration data.
    """
    
    def __init__(self, fileList):
        """
        """
        self.fileList = fileList

    def dataSynchroniser(self):
        
        firstList = []
        master = [] 
        firstListImproved = []

        gravMaster = []
        accMaster = []
        

        #source for ordering lists: https://www.geeksforgeeks.org/python-list-sort/

        
        """
        what we are after is to make it so that the list passsed as first list to the syncing is the file 
        with the last timestep and this needs to be ordered for grav and acc, but this may need to be done 
        before we pass it to here. Creates sortedLists with gravData and accData. In those is the ordered 
        first, second, third... ect SensorPackets (otherway round to fileList). Created unsortedList as a 
        deepcopy of fileList as I believe that appending a list is possible but it will alter the nested 
        list outside of the larger list source https://thomas-cokelaer.info/blog/2011/03/post-2/
        """
        sortSources = [[],[]]
        for m in range(2):

            for r in range(len(self.fileList)):
                
                sortSources[m].append(self.fileList[r][m][-1][0]) #this line pulls the final timestamp from each of the sensors, and appends it to the sortSources list.
                #note, this is the point where the order of m and r are changed.
                #before, we had the order of the devices, followed by whether it was an acceleration or gravity sensor stream.
                #now, the order swaps, so that all of the gravity data is in the same place, and all the acc data is in the same place.

            sortSources[m].sort(reverse=True) #this line sorts the final timestamp of the acc and grav streams in descending order.
        
        sortedLists = [[],[]]
        for m in range(2):
            
            for q in range(len(sortSources)):

                for r in range(len(self.fileList)):

                    if sortSources[m][q] == self.fileList[r][m][-1][0]:
                        sortedLists[m].append(self.fileList[r][m])
                        break
                    else:
                        continue


        for m in range(2):
            #this makes sure that we perform the function separately for the grav and acc packets that we have
            gravityOrAcceleration = m

            firstList = copy.deepcopy(sortedLists[m][0])
            """
            FOR THE VERY, VERY FIRST BIT, IN THE RANGE(1) AREA WE HAVE:
                firstList = copy.deepcopy(self.fileList[0][m])
            This will ensure that we start off either the acc packet, or grav packet masterlist, with the firstList. We need this so that we can then 
            allow this algorithm to be recursive, and repeat, by wiping the firstList, master and improvedfirstLists. I've kept 
            """

            for r in range( len(sortedLists[m]) - 1):
                #if we have 4 lists, we need to do 3 list comparison operations, of course, this would need to be run against the all the gravity data and then all the acceleration
                # data separately, which would mean a total of 6 list comparison operations took place, in two separate groups. 

                #from here on, we assume that we are working with the first list, and the second list, and making a combined list, the "master" list from the both of them. 
                #if this code were used in operation, then "master" would become the new first list, and then the third of 4 lists would become the new "secondList". 
                #this would generate another "master" which would then be compared against the 4th list to create the final iteration of "master". 

                #we would then end up with "masterGrav" and "masterAcc" lists, which THEN would be compared against one another using the algorithm previously laid out.
            
                #these names are subject to change, I need to work out how I want to save this data again, so that it can be used for grav sync stuff.
                 #THIS IS REALLY IMPORTANT. WE WILL USE THIS LIST AS A PLACEHOLDER, WHICH WILL BE REPLACED EVERY TIME WE ARE DOING A NEW COMPARISON. 
                """
                FOR THE VERY, VERY FIRST BIT, IN THE RANGE(1) AREA WE HAVE:
                firstList = copy.deepcopy(self.fileList[0][m])
                WE START WITH
                and by clearing out master; master = []
                and clearing our firstListImproved; firstListImproved = []
                WE WILL END WITH
                firstList = copy.deepcopy(master)
                AND ONCE THE RANGE(1) SECTION HAS BEEN COMPLETED, WE DO:
                if gravityOrAcceleration = 0 (grav packets), 
                gravMaster = copy.deepcopy(master)
                if gravityOrAcceleration = 1 (acc packets),
                accMaster = copy.deepcopy(master)
                """
                

                largeDeltaT = 0.0
                smallDeltaT = 0.0
                changeInFirstListValue = np.zeros(3)
                intermediateFirstListValue = np.zeros(3)

                meanOfSyncedData = np.zeros(3)

                #guide to understanding indecies of the sortedLists!
                #allData[i], choice of 0 or 1, where 0 is all the grav packets and 1 is all the acc packets
                #allData[][i], choice of 0 ... len(listOfFilesToBeProcessed) which decides which file to process the data from.
                #allData[][][i], choice of 0.... len(gravPackets), is where all the packets are stored of a respective type. Increase index to move along packets
                #allData[][][][i], choice of 0 or 1, where 0 is the epoch time data and 1 is the grav/acc x,y,z array of values.
                #allData[][][][1][i], after choosing 1, choice of 0,1,2 to select either the x, y or z data from the packet
                #example: print(allData[0][0][0][1][0])

                """
                this for loop starts by comparing all the packets in the firstList with secondList, and effectively doing a slightly modified "sync" operation. 
                Here we are trying to create an improved firstList, where whenever there is the option of averaging the data between timesteps (like we did last time)
                we create those values. If the timestamps of the two values in firstList and SecondList match, we don't need to find an intermediate value for the firstList,
                we can just append it straight away.
                we include the variable that checks if the entire list has been checked through so that we don't waste any packets. If say, sensor 1 was recording for 5 seconds
                before sensor 2 was, that's 500 ish data packets that we have! We don't want to waste that uneccessarily, especially if say sensor 3 and sensor 4 were operational
                at the same time and so can be used to get an average for those too. As a result, we check if the timestamp in firstList is recording at a time when secondList
                wasn't, and we append it to improvedList anyway.
                as this could work BOTH WAYS, you'll see that we repeat this operation later for secondList.
                """

                for i in range(len(firstList)): # firstList = firstList
                    p = 0  

                    for j in range(len(sortedLists[m][r+1])): #secondList = sortedLists[m][r+1]

                        if firstList[i][0] == sortedLists[m][r+1][j][0]:
                            firstListImproved.append([ sortedLists[m][r+1][j][0], np.around(firstList[i][1], 3) ])
                            break

                        elif ( firstList[i-1][0] < sortedLists[m][r+1][j][0] ) and ( firstList[i][0] > sortedLists[m][r+1][j][0] ):
                            
                            smallDeltaT = sortedLists[m][r+1][j][0] - firstList[i-1][0]
                            largeDeltaT = firstList[i][0] - firstList[i-1][0]
                            changeInFirstListValue = firstList[i][1] - firstList[i-1][1]
                            intermediateFirstListValue = (smallDeltaT/largeDeltaT)*changeInFirstListValue + firstList[i-1][1] #I think that the z value errors may come from this section of code
                            firstListImproved.append([ sortedLists[m][r+1][j][0], np.around(intermediateFirstListValue, 3) ])#most specifically, the timestamps. I think they may cause the problem.
                            break

                        p += 1
                        if p == len(sortedLists[m][r+1]): #I can't see why this line is yielding a syntax error when it is an elif statement, so it is an if statement.
                            firstListImproved.append([firstList[i][0], np.around(firstList[i][1], 3) ])
                            break
                        else:
                            continue
                """
                Now that we have made the firstListImproved, where we have some original packets that were recording when sensor 2 wasn't on, and lots more averaged
                packets, where we found the intermediate value between two sensor results.. we can now start taking a mean.
                The first for loop compares the firstListImproved against the secondList, now that the times have been synced, we can begin to take a mean of the two lists 
                of the same type of data.
                Once again, we check if a value is not matched in the secondList by the firstListImproved, and if that is the case, we append that value to the master.
                """
                for i in range(len(firstListImproved)):
                    t = 0

                    for j in range(len(sortedLists[m][r+1])):

                        if firstListImproved[i][0] == sortedLists[m][r+1][j][0]:
                            meanOfSyncedData = ( firstListImproved[i][1] + sortedLists[m][r+1][j][1] )/2
                            master.append([ sortedLists[m][r+1][j][0], meanOfSyncedData])
                            break

                        t += 1
                        if t == (len(sortedLists[m][r+1])) :
                            master.append( firstListImproved[i] )
                            break
                        else:
                            continue
                """
                This second loop is now to check that we have all the unmatched values in the secondList too, where there is data for the secondList and there isn't in the firstList
                for example if the sensor 2 recorded for 6 seconds after sensor 1 switched off, we need to save that data too, no sense in it going to waste.
                """
                
                del firstList[:]
                #clearing lists in python3 source: https://stackoverflow.com/a/850831
                firstList = copy.deepcopy(master) 
                del firstListImproved[:]
                del master[:]           
            
            if gravityOrAcceleration == 0:
                gravMaster = copy.deepcopy(firstList)
                continue
            if gravityOrAcceleration == 1:
                accMaster = copy.deepcopy(firstList)
                continue
            
        self.gravMaster = gravMaster
        self.accMaster = accMaster
            
        #source for calling variables: https://stackoverflow.com/a/10139935
        
        print('Data sources have been synchronised')

    def syncGravWithAcc(self):
        
        gravMasterSynced = []
            
        for j in range(len(self.accMaster)):
            if self.accMaster[0][0] < self.gravMaster[0][0]:
                self.accMaster.pop(0)
            elif self.accMaster[-1][0] > self.gravMaster[-1][0]:
                self.accMaster.pop(-1)
            else:
                break

        largeDeltaT = 0.0
        smallDeltaT = 0.0
        changeInGravValue = np.zeros(3)
        syncedGrav = np.zeros(3)
        # note see john's notes for the explanations, this is basically the gradient we'll be using kinda.
        for j in range(len(self.accMaster)):
#note, I have changed the order of these now, to try and account for the bug where we can have:
# s1:  * * (*   *) *
# s2: - - - (- -) - -
            for i in range(len(self.gravMaster)):
        
                if self.gravMaster[i][0] == self.accMaster[j][0]:
                    gravMasterSynced.append([ self.accMaster[j][0], self.gravMaster[i][1] ]) 
                    break
                
                elif (self.gravMaster[i][0] > self.accMaster[j][0]) and (self.gravMaster[i-1][0] < self.accMaster[j][0]):
                    smallDeltaT = self.accMaster[j][0] - self.gravMaster[i-1][0]
                    largeDeltaT = self.gravMaster[i][0] - self.gravMaster[i-1][0]
                    changeInGravValue = self.gravMaster[i][1] - self.gravMaster[i-1][1]
                    syncedGrav = (smallDeltaT/largeDeltaT)*changeInGravValue + self.gravMaster[i-1][1]
                    gravMasterSynced.append([self.accMaster[j][0], np.around(syncedGrav, 3)])
                    break
                
        allData = [gravMasterSynced, self.accMaster]
        
        print('Gravity data synchronised with acceleration data')
        return allData
        #np.around is used to round the synced value to 3 decimal places: https://stackoverflow.com/a/46994452
                