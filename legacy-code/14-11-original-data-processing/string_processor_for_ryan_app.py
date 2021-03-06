import re as regex
import numpy as np
inputFile = open("stationery_14_11_james_GV1_1_T30.csv","r")
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
    else:
        raise ValueError("You have an unknown packet at %s"%(i))
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

accPackets = []
gravPackets = []
for i in range(len(accPacketsTogether)):
    accPackets.append([int(accPacketsTogether[i][0]), float(accPacketsTogether[i][1]), float(accPacketsTogether[i][2]), float(accPacketsTogether[i][3])] )
for i in range(len(gravPacketsTogether)):
    gravPackets.append([int(gravPacketsTogether[i][0]), float(gravPacketsTogether[i][1]), float(gravPacketsTogether[i][2]), float(gravPacketsTogether[i][3])] )

#classifies the strings of values: time, x value, y value, z value, as floats or ints, and stores them as a final list.