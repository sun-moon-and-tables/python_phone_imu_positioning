import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import copy
import math

class integration_and_plot:
    """
    This class will contains two functions. First integrates linear accelation data. 
    Second function plots the integrated data.
    Input is the list of linear acceleration data with timestamps from
    data_processor_pandas.py .
    """
    
    def __init__(self, AccandTime):
        """
        """
        self.inputData = AccandTime
    
    def integration(self): 
        accelerationVector = []
        timesOfAcc = []
        velocityVector = []
        positionVector = []
        accelerationMean = np.array([-0.00089, 0.00118, 0.05586])
        #The mean of the static acceleration is subtracted from the acceleration arrays, and all is rounded to 5dp
        for i in range(len(self.inputData)):
            accelerationVector.append( np.around( np.array(self.inputData[i][1] - accelerationMean), decimals = 5) )
            timesOfAcc.append(self.inputData[i][0])
        
        # low pass filter to remove noise from the LiDAR sensor

        for i in range(len(self.inputData)):
            if abs(accelerationVector[i][0]) < 1.4:
                accelerationVector[i][0] = 0
            if abs(accelerationVector[i][1]) < 1.4:
                accelerationVector[i][1] = 0
            else:
                pass


        #integration of acceleration to velocity
        tempVelocity = np.zeros(3)
        for i in range(len(accelerationVector) - 1):
            tempVelocity = tempVelocity + (accelerationVector[i+1] + accelerationVector[i])*(timesOfAcc[i+1] - timesOfAcc[i])*0.5 
            velocityVector.append(tempVelocity)

        #need to pop the first timestamp so that lists match,
        #as we are using trapezium rule to integrate and with a short enough period between values
        #this has a negigible affect on precision
        timesOfVel = copy.deepcopy(timesOfAcc)
        timesOfVel.pop(0)

        #integration of velocity to position
        tempPosition = np.zeros(3)
        for i in range(len(velocityVector) - 1):
            tempPosition = tempPosition + (velocityVector[i+1] + velocityVector[i])*(timesOfVel[i+1] - timesOfVel[i])*0.5
            positionVector.append(tempPosition)

        timesOfPos = copy.deepcopy(timesOfVel)
        timesOfPos.pop(0)

        #provide the object new parameters so that the plotting method can use them
        self.timesOfPos = timesOfPos
        self.timesOfVel = timesOfVel
        self.timesOfAcc = timesOfAcc
        self.accelerationVector = accelerationVector
        self.velocityVector = velocityVector
        self.positionVector = positionVector

    def plotting(self, fileNameForSaving):
        # source for increasing the font size, default font size is 10: https://stackoverflow.com/a/3900167
        plt.rcParams.update({'font.size': 11})

        currentAccX = []
        currentAccY = []
        currentAccZ = []
        
        for i in range(len(self.accelerationVector)):
            currentAccX.append(self.accelerationVector[i][0])
            currentAccY.append(self.accelerationVector[i][1])
            currentAccZ.append(self.accelerationVector[i][2])

        #This line of code, if activated for a stationary data file, this will print the mean acceleration of the file. 
        #This can be used to find the bias acceleration for the inertial measurement unit.
        #print('The mean of the acceleration data is (in order of X,Y,Z):\n%f\n%f\n%f'%(np.mean(currentAccX), np.mean(currentAccY), np.mean(currentAccZ) ))
        
        plt.plot(self.timesOfAcc, currentAccZ, '-', label = 'Z Acceleration')
        plt.plot(self.timesOfAcc, currentAccY, '-', label = 'Y Acceleration')
        plt.plot(self.timesOfAcc, currentAccX, '-', label = 'X Acceleration')
        plt.xlabel('Time (s)')
        plt.ylabel('Linear Acceleration (ms$^{-2}$)')
        plt.minorticks_on()
        # plt.title('Acceleration over time of NGIMU')
        plt.legend(loc = 2)
        plt.savefig("%s_acceleration.jpg"%(fileNameForSaving), bbox_inches='tight')
        plt.show()
        
        currentVelX = []
        currentVelY = []
        currentVelZ = []
        
        for i in range(len(self.velocityVector)):
            currentVelX.append(self.velocityVector[i][0])
            currentVelY.append(self.velocityVector[i][1])
            currentVelZ.append(self.velocityVector[i][2])
            
        plt.plot(self.timesOfVel, currentVelX, '-', label = 'X Velocity')
        plt.plot(self.timesOfVel, currentVelY, '-', label = 'Y Velocity')
        plt.plot(self.timesOfVel, currentVelZ, '-', label = 'Z Velocity')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (ms$^{-1}$)')
        # plt.title('Velocity over time of NGIMU')
        plt.legend(loc = 2)
        plt.savefig("%s_velocity.jpg"%(fileNameForSaving), bbox_inches='tight')
        plt.show()
        
        currentPosX = []
        currentPosY = []
        currentPosZ = []
        
        for i in range(len(self.positionVector)):
            currentPosX.append(self.positionVector[i][0])
            currentPosY.append(-1 * self.positionVector[i][1]) # there is a minus one here because it seems the NGIMU was backwards the whole time
            currentPosZ.append(self.positionVector[i][2])
            
        plt.plot(self.timesOfPos, currentPosX, '-', label = 'X Position')
        plt.plot(self.timesOfPos, currentPosY, '-', label = 'Y Position')
        plt.plot(self.timesOfPos, currentPosZ, '-', label = 'Z Position')
        plt.xlabel('Time (s)')
        plt.ylabel('Position (m)')
        #plt.title('Position over time of NGIMU')
        plt.legend(loc = 2)
        plt.savefig("%s_position.jpg"%(fileNameForSaving), bbox_inches='tight')
        plt.show()
        
        # the following section of code will generate a 2d plot of position in x vs position in y.
        # It also contains a dummy plot, which will instead return the final magnitude of position 
        # of the sensor (since we won't be showing corner test diagrams). If we want to add corner
        # test diagrams, these won't really work, maybe instead calculate the difference in displacement?
        plt.plot(currentPosX, currentPosY, '-')
        # dummy plot
        plt.plot([], [], ' ', label="Vehicle moved %s m overall"%(np.around(
            np.sqrt(currentPosX[-1] * currentPosX[-1] + currentPosY[-1] * currentPosY[-1])
            , decimals=2)))
        plt.legend(frameon=False)
        plt.xlabel('Position over time in x (m)')
        plt.ylabel('Position over time in y (m)')
        plt.savefig("%s_2d_position.jpg"%(fileNameForSaving), bbox_inches='tight')
        plt.show()

        """at this point, we have the new 3D animation code.
        This has been cobbled together from various sources, but
        mainly from matplotlibanimator.py, after using matplotlibanimator_3.py 
        to understand the core concepts.
        """
        """
        fig = plt.figure()
        ax = p3.Axes3D(fig)

        
        This section of code will be used to try and reduce the animation and playing time. For example, the 30s of real data played out as closer to 
        2mins 30s of gif. As a result, we will try selecting fewer of the data points, 1 in 10, 1 in 5 for example, and pass this shortened list to
        the animation functions, like gen and FuncAnimation.
        
        #remainder/modulo operator: https://stackoverflow.com/a/5584604
        currentPosXShort = [currentPosX[0]]
        currentPosYShort = [currentPosY[0]]
        currentPosZShort = [currentPosZ[0]]
        timesOfPosShort = [self.timesOfPos[0]]
        
        for i in range(len(self.timesOfPos)):
            if i % 5 == 0:
                currentPosXShort.append(currentPosX[i])
                currentPosYShort.append(currentPosY[i])
                currentPosZShort.append(currentPosZ[i])
                timesOfPosShort.append(self.timesOfPos[i])

        def gen():
            i = 0
            while i < len(timesOfPosShort):
                yield np.array([currentPosXShort[i], currentPosYShort[i], currentPosZShort[i]])
                i += 1
        
        def update(num, data, line):
            line.set_data(data[:2, :num])
            line.set_3d_properties(data[2, :num])
        
        data = np.array(list(gen())).T
        line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1]) #nope, no error here.
        
        #Setting the axes properties
        ax.set_xlim3d([-2, 2])
        ax.set_xlabel('X Position (m)')
        
        ax.set_ylim3d([-2, 2])
        ax.set_ylabel('Y Position (m)')
        
        ax.set_zlim3d([-2, 2])
        ax.set_zlabel('Z Position (m)')
        
        ani = animation.FuncAnimation(fig, update, len(timesOfPosShort), fargs=(data, line), interval=1, blit=False)
        #ani.save('matplot003.mp4', writer='ffmpeg')
        plt.show()
        
        #source: https://stackoverflow.com/a/38121759

        #23/11 more animation guidance: https://stackoverflow.com/a/28077104
        #change of animation writer to ffmpeg, can only be done on machines that can install software: https://stackoverflow.com/a/31193532

        #and in the comments of that:
        
        If saving as video instead of .gif then ani.save('test.mp4', writer='ffmpeg', codec='h264') should replace the last line. 
        If you want to find out which codecs are available then run ffmpeg -codec in the terminal. 
        Given that you want to use ffmpeg as the writer. 
        
        """
        
        # This code will produce a 2d animation of the position x vs y. 
        fig = plt.figure()
        ax = plt.axes(xlim=(-0.01, 0.3), ylim=(-0.01, 0.15), xlabel= ('x Position over time (m)'), ylabel=('y Position over time (m)'))

        def gen():
            i = 0
            while i < len(currentPosX):
                yield np.array([currentPosX[i], currentPosY[i]])
                i += 1
        
        def update(num, data, line):
            line.set_data(data[:2, :num])
        
        data = np.array(list(gen())).T
        line, = ax.plot(data[0, 0:1], data[1, 0:1]) #nope, no error here.
        
        ani = animation.FuncAnimation(fig, update, len(currentPosX), fargs=(data, line), interval=1, blit=False)
        # ani.save('matplot003.gif')
        plt.show()




