"""
this is the original string processor, written for the old, bad app. This is just here as a momument.
"""
import re as regex
#import function brings in regex
inputFile = open("john_joe_short_test_for_formatting.csv","r")
fileContents = inputFile.read()
#we need to read in the file contents.


delimiters = [',']

separatedListOfPackets = []
separatedListOfPackets = regex.split('|'.join(delimiters), fileContents)
#this bit of code just splits the csv file into many small strings based on the commas between them.
#https://stackoverflow.com/a/19720443
#note, the items have now all been converted into strings now. We'll later need to convert them back into floats and integers.
#this conversion process can be what also helps with determining what is a packet identifier and similar.

strippedListOfPackets = []

for i in range(len(separatedListOfPackets)):
    strippedListOfPackets.append(separatedListOfPackets[i].strip())
#this little for loop just removes the whitespace from each of these strings so that they can be considered as floats or ints.
#https://jakevdp.github.io/WhirlwindTourOfPython/14-strings-and-regular-expressions.html

containsATimestamp = '.*\..*\..*'
slicedListOfPackets = []
#containsATimeStamp is a regex expression for identifying if a string has 2 .s in it.
#https://stackoverflow.com/a/22199919

for i in range(len(strippedListOfPackets)):
    
    if regex.match(containsATimestamp, strippedListOfPackets[i]):
        indexToMakeSlice = strippedListOfPackets[i].index('.') + 3
        slicedListOfPackets.append(strippedListOfPackets[i][0:indexToMakeSlice])
        slicedListOfPackets.append(strippedListOfPackets[i][indexToMakeSlice + 1:])
    else:
        slicedListOfPackets.append(strippedListOfPackets[i])

#this final loop just cuts apart badly sent strings into two packets, and makes sure that they output in the correct order!
#https://www.programiz.com/python-programming/regex
#https://www.digitalocean.com/community/tutorials/how-to-index-and-slice-strings-in-python-3
#https://stackoverflow.com/a/48959881

intsAndFloatsListOfPackets = []
for i in range(len(slicedListOfPackets)):
    try:
        int(slicedListOfPackets[i])
        intsAndFloatsListOfPackets.append(int(slicedListOfPackets[i]))
    except:
        intsAndFloatsListOfPackets.append(float(slicedListOfPackets[i]))

#this loop now converts the whole list into either floats or ints, so now we can identify if a value in the string is either a packet
#identifier or if it is a part of a packet.

print(fileContents, '\n\n')
print(intsAndFloatsListOfPackets)
print(separatedListOfPackets)
