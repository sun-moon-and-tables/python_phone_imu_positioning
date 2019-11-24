import re as regex
import numpy as np
"""
The epoch time on phones is prone to drift by several seconds rather quickly, depending on the quality of the phone.
This isn't a problem for regular use, as people don't use their phones for precise timing, generally, and if the time
moves off by a minute, then it gets corrected by the network.

This means our data is prone to some serious error, error that is pretty much unknown and changes every time we would do an experiment.
As a result, we are using this program to "synchronise" the timestamps for each of the packets, by clearing them all to the starting first value for the sensor.

This therefore requires all sensors to be switched on at pretty much the same time, and the difference in switch on time, will be what
contributes our error.

This is an unknown error too, but it should smaller, and at least we can visualise the error quickly.

"""
class packet_processor:
    """
    This class processes the packets that are supplied in each recorded data set.
    Cleans them up and saves them as two lists, entry [0] are the gravity packets and entry [1] are the acceleration packets
    """

    def __init__(self, inputFile):
        """
        """
        self.inputFile = inputFile

    def packetProcessor (self):

        inputFile = open(self.inputFile,"r")
        fileContents = inputFile.read()
        #read in the file contents, currently this needs to be typed in, as its generally faster than a GUI.

        delimiters = ['\n']

        separatedListOfPackets = []
        separatedListOfPackets = regex.split('|'.join(delimiters), fileContents)
        #separates the new file to identify each newline as a new string in a list of strings, and removes the newline characters.
        #https://stackoverflow.com/a/19720443

        matchesAnAcc = '.*Acc.*'
        matchesAGrav = '.*Grav*'

        accPacketsWithText = []
        gravPacketsWithText = []
        #matchesAnAcc and matchesAGrav are used to read each packet and determine if it contains "Acc", or a "Grav"
        #the packets are then sorted into separate lists depending on whether the packet is Accelerometer or Gravity Sensor data
        #https://stackoverflow.com/a/22199919

        for i in range(len(separatedListOfPackets)):
            
            if regex.match(matchesAnAcc, separatedListOfPackets[i]):
                accPacketsWithText.append(separatedListOfPackets[i])
            elif regex.match(matchesAGrav, separatedListOfPackets[i]):
                gravPacketsWithText.append(separatedListOfPackets[i])
        #iterates through the list of packets and sorts them into the lists, and raises an error if there are any unknown packets that
        #don't match what we would expect.

        accPacketsTogether = []
        gravPacketsTogether = []
        temp = ''
        for i in range(len(accPacketsWithText)):
            temp = regex.sub("[a-zA-Z:]", "", accPacketsWithText[i])
            accPacketsTogether.append(regex.sub(";", " ", temp).split())
            
        for i in range(len(gravPacketsWithText)):
            temp = regex.sub("[a-zA-Z:]", "", gravPacketsWithText[i])
            gravPacketsTogether.append(regex.sub(";", " ", temp).split())
            
        #temp is a temporary variable that is used to apply two regex expressions at once, and is reused for every packet that is processed
        #iterates through each grav list and acc list, and removes the text, colons and semi colons from them.
        # regex sub, substitutes any character for another, which is nothing in this case: https://stackoverflow.com/a/53229016
        # split is used to separate the strings where there are semi colons, which is between each data value for the packets. 
        # This then means we can classify the components of the packet individually, as floats or ints: https://stackoverflow.com/a/6181784

        gravPackets = []
        accPackets = []
        packetsCombined = np.zeros(3)

        for i in range(len(accPacketsTogether)):
            accPackets.append( [int( int(accPacketsTogether[i][0]) - int(accPacketsTogether[0][0]) ), np.array([float(accPacketsTogether[i][1]), float(accPacketsTogether[i][2]), float(accPacketsTogether[i][3] ) ]) ])
        for i in range(len(gravPacketsTogether)):
            gravPackets.append( [int( int(gravPacketsTogether[i][0]) - int(accPacketsTogether[0][0]) ), np.array([float(gravPacketsTogether[i][1]), float(gravPacketsTogether[i][2]), float(gravPacketsTogether[i][3] ) ]) ])

        for i in range(len(accPackets)):
            try:
                if accPackets[i][0] == accPackets[i+1][0]:
                    packetsCombined = ( accPackets[i][1] + accPackets[i+1][1] )/2 
                    accPackets[i] = [accPackets[i][0], packetsCombined]
                    accPackets.pop(i+1)
            except IndexError:
                pass
                #source for ignoring the index out of range error, so that you can remove elements from this list. It's not a concern
                # https://stackoverflow.com/a/26853522
        
        for i in range(len(gravPackets)):
            try:
                if gravPackets[i][0] == gravPackets[i+1][0]:
                    packetsCombined = ( gravPackets[i][1] + gravPackets[i+1][1] )/2 
                    gravPackets[i] = [gravPackets[i][0], packetsCombined]
                    gravPackets.pop(i+1)
            except IndexError:
                pass
                #source for ignoring the index out of range error, so that you can remove elements from this list. It's not a concern
                # https://stackoverflow.com/a/26853522

        packets = [gravPackets, accPackets]
        #classifies the strings of values: time, x value, y value, z value, as floats or ints, and stores them as a final list.
        np.save("Processed--%s"%(self.inputFile), packets)
        inputFile.close()


#okay, so the intention is, that we run this class on each of the data files that we plan on processing
#we run these classes in a main program, that generates these objects of the stripped data files
#and then this main program puts all of these stripped data files into lists, and saves those.
#as we're using np.array, we'll save that as a .npy file, which then the main program will use to do the data sync
#followed by the gravity sync
#and then the final integration and plotting of the data.

