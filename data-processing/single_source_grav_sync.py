#importing lists from other files in python: https://stackoverflow.com/a/29267100
import numpy as np


class single_data_source_sync:
    """
    This class will have only one function, that will serve to synchronise the gravity data to acceleration data, but only for one data source.
    """
    def __init__(self, inputFile):
        """
        """
        self.inputFile = inputFile

    def syncGravWithAcc(self):
        gravMaster = self.inputFile[0][0]
        accMaster = self.inputFile[0][1]

        for j in range(len(accMaster)):
            if accMaster[0][0] < gravMaster[0][0]:
                accMaster.pop(0)
            elif accMaster[-1][0] > gravMaster[-1][0]:
                accMaster.pop(-1)
            else:
                break

        syncedgravMaster = []
        largeDeltaT = 0
        smallDeltaT = 0
        changeInGravValue = np.zeros(3)
        syncedGrav = np.zeros(3)
        # note see john's notes for the explanations, this is basically the gradient we'll be using kinda.
        for j in range(len(accMaster)):
#note, I have changed the order of these now, to try and account for the bug where we can have:
# s1:  * * (*   *) *
# s2: - - - (- -) - -
            for i in range(len(gravMaster)):

                if gravMaster[i][0] == accMaster[j][0]:
                    syncedgravMaster.append([accMaster[j][0], np.array([gravMaster[i][1][0], gravMaster[i][1][1], gravMaster[i][1][2] ]) ])
                    break
                elif (gravMaster[i][0] > accMaster[j][0]) and (gravMaster[i-1][0] < accMaster[j][0]):
                    smallDeltaT = accMaster[j][0] - gravMaster[i-1][0]
                    largeDeltaT = gravMaster[i][0] - gravMaster[i-1][0]
                    changeInGravValue = gravMaster[i][1] - gravMaster[i-1][1]
                    syncedGrav = (smallDeltaT/largeDeltaT)*changeInGravValue + gravMaster[i-1][1]
                    syncedgravMaster.append([accMaster[j][0], np.around(syncedGrav, 3)])
                    break

        allData = [syncedgravMaster, accMaster]
        print('Gravity data synchronised with acceleration data')

        return allData
        #np.around is used to round the synced value to 3 decimal places: https://stackoverflow.com/a/46994452