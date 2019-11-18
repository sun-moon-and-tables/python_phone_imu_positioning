import numpy as np
from packet_processor_multiple_sources import packet_processor

listOfFilesToBeProcessed = []
print('Enter the filenames of the programs that you wish to process. \nIf they are in the same folder as this program, just enter the filename. \nIf they are in another folder, use the complete file path.')   
while True:
    inputFile = input('List a file to be processed: ')
    try:
        testIfExists = open(inputFile)
        testIfExists.close()
        listOfFilesToBeProcessed.append(inputFile)
        print('File exists.')
        checkIfDone = input('Have you finished listing imu files? \nPress Y to start processing, press N to enter more files: ')
        checkIfDone.capitalize()
        if checkIfDone == 'Y':
            break
        elif checkIfDone == 'N':
            continue
    except FileNotFoundError:
        print('File does not exist. Please try again: \n')
        continue
    #open file check if exists: https://dbader.org/blog/python-check-if-file-exists

for file in listOfFilesToBeProcessed:
    process = packet_processor(file)
    process.packetProcessor()

print('Files have been processed.')

allData = []
for file in listOfFilesToBeProcessed:
    data = np.load("Processed--%s.npy"%(file))
    allData.append(data)

print(len(allData[0][0]))



#loading npy data: https://stackoverflow.com/a/33885940
#of course, now we have the allData list:
#allData[i], choice of 0 ... len(listOfFilesToBeProcessed) which decides which file to process the data from.
#allData[][i], choice of 0 or 1, where 0 is all the grav packets and 1 is all the acc packets
#allData[][][i], choice of 0.... len(gravPackets), is where all the packets are stored of a respective type. Increase index to move along packets
#allData[][][][i], choice of 0 or 1, where 0 is the epoch time data and 1 is the grav/acc x,y,z array of values.
#allData[][][][1][i], after choosing 1, choice of 0,1,2 to select either the x, y or z data from the packet
#example: print(allData[0][0][0][1][0])


