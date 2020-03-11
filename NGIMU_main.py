from data_processor_pandas import excel_processor
from NGIMU_integration_and_plotting import integration_and_plot


print('Enter the filename of the Linear Acceleration csv file that you wish to process. \nFile can be saved as a .csv or .xlsx')   

while True:
    inputFile = input('List the file to be processed: ')

    try:
        testIfExists = open(inputFile, 'r')
        testIfExists.close()
        print('File exists.')
        break
    except FileNotFoundError:
        print('File does not exist. Please try again: \n')
        continue


userinput = input('xlsx or csv? (0)/(1) ')
if userinput == '0':
    process = excel_processor(inputFile)
    outputLinAcc = process.xlsxProcessor()
elif userinput == '1':
    process = excel_processor(inputFile)
    outputLinAcc = process.csvProcessor()
else:
    print('error.')

plot = integration_and_plot(outputLinAcc) 
plot.integration()
plot.plotting(inputFile)


