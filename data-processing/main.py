import numpy as np
import os
from packet_processor_multiple_sources_timeclear import packet_processor
from single_source_grav_sync import single_data_source_sync
from multiple_source_grav_sync import multi_data_source_sync 
from integration_and_plotting import integration_and_plot

listOfFilesToBeProcessed = []
print('Enter the filenames of the programs that you wish to process. \nIf they are in the same folder as this program, just enter the filename. \nIf they are in another folder, use the complete file path.')   
while True:
    inputFile = input('List a file to be processed: ')
    if inputFile == 'y' or inputFile == 'Y':
        break
    try:
        testIfExists = open(inputFile)
        testIfExists.close()
        listOfFilesToBeProcessed.append(inputFile)
        print('File exists.')
        print('Have you finished listing imu files? \nContinue entering more file names, or press Y to start processing. ')
    except FileNotFoundError:
        print('File does not exist. Please try again: \n')
        continue
    #open file check if exists: https://dbader.org/blog/python-check-if-file-exists
if len(listOfFilesToBeProcessed) == 0:
    raise ValueError('Error. You have not entered any files to be processed.')
for file in listOfFilesToBeProcessed:
    process = packet_processor(file)
    process.packetProcessor()

print('Files have been processed.')

allData = []
for file in listOfFilesToBeProcessed:
    data = np.load("Processed--%s.npy"%(file), allow_pickle=True)
    allData.append(data)
    os.remove("Processed--%s.npy"%(file))


#explanation for allow_pickle = True: https://github.com/tensorflow/tensorflow/issues/28102
if len(listOfFilesToBeProcessed) == 1:
    singlesyncgrav = single_data_source_sync(allData)
    plot = integration_and_plot(singlesyncgrav.syncGravWithAcc()) 
else:
    multisyncgrav = multi_data_source_sync(allData)
    multisyncgrav.dataSynchroniser()
    plot = integration_and_plot(multisyncgrav.syncGravWithAcc())

#printing and returning data source: https://stackoverflow.com/a/7664904
plot.integration()
plot.plotting(listOfFilesToBeProcessed[0])




#loading npy data: https://stackoverflow.com/a/33885940
#of course, now we have the allData list:
#allData[i], choice of 0 ... len(listOfFilesToBeProcessed) which decides which file to process the data from.
#allData[][i], choice of 0 or 1, where 0 is all the grav packets and 1 is all the acc packets
#allData[][][i], choice of 0.... len(gravPackets), is where all the packets are stored of a respective type. Increase index to move along packets
#allData[][][][i], choice of 0 or 1, where 0 is the epoch time data and 1 is the grav/acc x,y,z array of values.
#allData[][][][1][i], after choosing 1, choice of 0,1,2 to select either the x, y or z data from the packet
#example: print(allData[0][0][0][1][0])

