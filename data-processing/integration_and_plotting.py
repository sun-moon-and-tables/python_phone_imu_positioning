import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import copy

class integration_and_plot:
    """
    This class will have two functions. First will sync all the grav data and acc data. 
    Second function will do the grav synced with the acceleration data.
    """
    
    def __init__(self, gravAndAccLists):
        """
        """
        self.inputData = gravAndAccLists
    
    def integration(self):

        accWithoutGrav = []
        
        gravMaster = copy.deepcopy(self.inputData[0])
        accMaster = copy.deepcopy(self.inputData[1])
        """
        currently we are seeing different lengths of accMaster and gravMaster, which SHOULD NOT BE ALLOWED, if they have been processed through grav sync.
        Is this the multiple packet error, or something similar? (multiple packet error in packet_processor)
        print(len(accMaster))
        print(len(gravMaster))
        """
        for i in range(len(accMaster)):
            accWithoutGrav.append(accMaster[i][1] - gravMaster[i][1])
            #soure for correct np array!! https://stackoverflow.com/a/48343452
        
        velocityVector = []
        postionVector = []
        
        timesOfAcc = []
        
        for i in range(len(accMaster)):
            timesOfAcc.append( accMaster[i][0]/1000 )
        
        tempVelocity = np.zeros(3)
        for i in range(len(accWithoutGrav) - 1):
            tempVelocity = tempVelocity + (accWithoutGrav[i+1] + accWithoutGrav[i])*(timesOfAcc[i+1] - timesOfAcc[i])*0.5
            velocityVector.append(tempVelocity)
        
        timesOfVel = copy.deepcopy(timesOfAcc)
        timesOfVel.pop(0)
            
        tempPosition = np.zeros(3)
        for i in range(len(velocityVector) - 1):
            tempPosition = tempPosition + (velocityVector[i+1] + velocityVector[i])*(timesOfVel[i+1] - timesOfVel[i])*0.5
            postionVector.append(tempPosition)
        
        timesOfPos = copy.deepcopy(timesOfVel)
        timesOfPos.pop(0)
        
        self.timesOfPos = timesOfPos
        self.timesOfVel = timesOfVel
        self.timesOfAcc = timesOfAcc
        self.accWithoutGrav = accWithoutGrav
        self.velocityVector = velocityVector
        self.postionVector = postionVector
        
        #source for calling variables: https://stackoverflow.com/a/10139935

    def plotting(self):
        
        currentAccX = []
        currentAccY = []
        currentAccZ = []
        
        for i in range(len(self.accWithoutGrav)):
            currentAccX.append(self.accWithoutGrav[i][0])
            currentAccY.append(self.accWithoutGrav[i][1])
            currentAccZ.append(self.accWithoutGrav[i][2])
            
        plt.plot(self.timesOfAcc, currentAccX, '-', label = 'x acceleration')
        plt.plot(self.timesOfAcc, currentAccY, '-', label = 'y acceleration')
        plt.plot(self.timesOfAcc, currentAccZ, '-', label = 'z acceleration')
        plt.xlabel('time')
        plt.ylabel('acceleartion without grav')
        plt.title('Acceleration over time')
        plt.legend(loc = 1)
        plt.show()
        
        currentVelX = []
        currentVelY = []
        currentVelZ = []
        
        for i in range(len(self.velocityVector)):
            currentVelX.append(self.velocityVector[i][0])
            currentVelY.append(self.velocityVector[i][1])
            currentVelZ.append(self.velocityVector[i][2])
            
        plt.plot(self.timesOfVel, currentVelX, '-', label = 'x velocity')
        plt.plot(self.timesOfVel, currentVelY, '-', label = 'y velocity')
        plt.plot(self.timesOfVel, currentVelZ, '-', label = 'z velocity')
        plt.xlabel('time')
        plt.ylabel('velocity in xyz')
        plt.title('Velocity over time')
        plt.legend(loc =1)
        plt.show()
        
        currentPosX = []
        currentPosY = []
        currentPosZ = []
        
        for i in range(len(self.postionVector)):
            currentPosX.append(self.postionVector[i][0])
            currentPosY.append(self.postionVector[i][1])
            currentPosZ.append(self.postionVector[i][2])
            
        plt.plot(self.timesOfPos, currentPosX, '-', label = 'x position')
        plt.plot(self.timesOfPos, currentPosY, '-', label = 'y position')
        plt.plot(self.timesOfPos, currentPosZ, '-', label = 'z position')
        plt.xlabel('time')
        plt.ylabel('position in xyz')
        plt.title('Position over time.')
        plt.legend(loc = 1)
        plt.show()
        
        """at this point, we have the new 3D animation code.
        This has been cobbled together from various sources, but
        mainly from matplotlibanimator.py, after using matplotlibanimator_3.py 
        to understand the core concepts.
        """
        
        fig = plt.figure()
        ax = p3.Axes3D(fig)

        """
        This section of code will be used to try and reduce the animation and playing time. For example, the 30s of real data played out as closer to 
        2mins 30s of gif. As a result, we will try selecting fewer of the data points, 1 in 10, 1 in 5 for example, and pass this shortened list to
        the animation functions, like gen and FuncAnimation.
        """
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
        ax.set_xlabel('X')
        
        ax.set_ylim3d([-2, 2])
        ax.set_ylabel('Y')
        
        ax.set_zlim3d([-2, 2])
        ax.set_zlabel('Z')
        
        ani = animation.FuncAnimation(fig, update, len(timesOfPosShort), fargs=(data, line), interval=1, blit=False)
        #ani.save('matplot003.mp4', writer='ffmpeg')
        plt.show()
        
        #source: https://stackoverflow.com/a/38121759

        #23/11 more animation guidance: https://stackoverflow.com/a/28077104
        #change of animation writer to ffmpeg, can only be done on machines that can install software: https://stackoverflow.com/a/31193532

        #and in the comments of that:
        """
        If saving as video instead of .gif then ani.save('test.mp4', writer='ffmpeg', codec='h264') should replace the last line. 
        If you want to find out which codecs are available then run ffmpeg -codec in the terminal. 
        Given that you want to use ffmpeg as the writer. 
        """