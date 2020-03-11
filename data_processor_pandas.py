import pandas as pd 
import numpy as np

class excel_processor:

    """
    Uses pandas (launch visual studio code through anaconda navigator to access or install it on your own device)
    to extract linear acceleration data from either a .csv or .xlsx file.
    """
    def __init__(self, inputFile):
            """
            Takes only the user input file as an argument.
            """
            self.inputFile = inputFile

    def csvProcessor(self):
        linearcsv = pd.read_csv(self.inputFile)

        timesOfAcc = pd.DataFrame(linearcsv, columns= ['Time (s)'])
        timesOfAcc = timesOfAcc['Time (s)'].tolist()

        AccX = pd.DataFrame(linearcsv, columns= ['X (g)'])
        AccX = AccX['X (g)'].tolist()

        AccY = pd.DataFrame(linearcsv, columns= ['Y (g)'])
        AccY = AccY['Y (g)'].tolist()

        AccZ = pd.DataFrame(linearcsv, columns= ['Z (g)'])
        AccZ = AccZ['Z (g)'].tolist()

        linearAcceleration = []
        for i in range(len(AccX)):
            linearAcceleration.append([timesOfAcc[i] - timesOfAcc[0], np.array([AccX[i] * 9.81, AccY[i] * 9.81, AccZ[i] * 9.81 ])])

        return linearAcceleration
    
    def xlsxProcessor(self):
        linearxlsx = pd.read_excel(self.inputFile)

        timesOfAcc = pd.DataFrame(linearxlsx, columns= ['Time (s)'])
        timesOfAcc = timesOfAcc['Time (s)'].tolist()

        AccX = pd.DataFrame(linearxlsx, columns= ['X (g)'])
        AccX = AccX['X (g)'].tolist()

        AccY = pd.DataFrame(linearxlsx, columns= ['Y (g)'])
        AccY = AccY['Y (g)'].tolist()

        AccZ = pd.DataFrame(linearxlsx, columns= ['Z (g)'])
        AccZ = AccZ['Z (g)'].tolist()

        linearAcceleration = []
        for i in range(len(AccX)):
            linearAcceleration.append([timesOfAcc[i] - timesOfAcc[0], np.array([AccX[i] * 9.81, AccY[i] * 9.81, AccZ[i] * 9.81 ])])

        return linearAcceleration