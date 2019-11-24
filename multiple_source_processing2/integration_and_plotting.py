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
        
        #print(self.inputData[0], 'gravMaster\n\n\n\n', self.inputData[1], 'accMaster\n\n\n\n')


        accWithoutGrav = []
        
        gravMaster = copy.deepcopy(self.inputData[0])
        accMaster = copy.deepcopy(self.inputData[1])
        #print(accMaster, '\n\n')
        #print(gravMaster)
        """
        currently we are seeing different lengths of accMaster and gravMaster, which SHOULD NOT BE ALLOWED, if they have been processed through grav sync.
        Is this the multiple packet error, or something similar? (multiple packet error in packet_processor)
        print(len(accMaster))
        print(len(gravMaster))
        """
        for i in range(len(accMaster)):
            accWithoutGrav.append(accMaster[i][1] - gravMaster[i][1])
            #print(accMaster[i][1], '\n', gravMaster[i][1], '\n', accWithoutGrav[i])
            #soure for correct np array!! https://stackoverflow.com/a/48343452
        
        velocityVector = []
        postionVector = []
        
        timesOfAcc = []
        
        for i in range(len(accMaster)):
            timesOfAcc.append( accMaster[i][0]/1000 )
        
        #print(timesOfAcc, 'times of acc')
        #print(accWithoutGrav, 'acc without grav')
        #print(accMaster, 'accMaster')
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
        
        currentaccX = []
        currentaccY = []
        currentaccZ = []
        
        for i in range(len(self.accWithoutGrav)):
            currentaccX.append(self.accWithoutGrav[i][0])
            currentaccY.append(self.accWithoutGrav[i][1])
            currentaccZ.append(self.accWithoutGrav[i][2])
            
        plt.plot(self.timesOfAcc, currentaccX, '-', label = 'the joyful x values')
        plt.plot(self.timesOfAcc, currentaccY, '-', label = 'the joyful y values')
        plt.plot(self.timesOfAcc, currentaccZ, '-', label = 'the joyful z values')
        plt.xlabel('time')
        plt.ylabel('acceleartion without grav')
        plt.title('Acceleration over time')
        plt.legend(loc = 1)
        plt.show()
        
        currentvelX = []
        currentvelY = []
        currentvelZ = []
        
        for i in range(len(self.velocityVector)):
            currentvelX.append(self.velocityVector[i][0])
            currentvelY.append(self.velocityVector[i][1])
            currentvelZ.append(self.velocityVector[i][2])
            
        plt.plot(self.timesOfVel, currentvelX, '-', label = 'the joyful x values')
        plt.plot(self.timesOfVel, currentvelY, '-', label = 'the joyful y values')
        plt.plot(self.timesOfVel, currentvelZ, '-', label = 'the joyful z values')
        plt.xlabel('time')
        plt.ylabel('velocity in xyz')
        plt.title('Velocity over time')
        plt.legend(loc =1)
        plt.show()
        
        currentposX = []
        currentposY = []
        currentposZ = []
        
        for i in range(len(self.postionVector)):
            currentposX.append(self.postionVector[i][0])
            currentposY.append(self.postionVector[i][1])
            currentposZ.append(self.postionVector[i][2])
            
        plt.plot(self.timesOfPos, currentposX, '-', label = 'the joyful x values')
        plt.plot(self.timesOfPos, currentposY, '-', label = 'the joyful y values')
        plt.plot(self.timesOfPos, currentposZ, '-', label = 'the joyful z values')
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
        
        def gen():
            i = 0
            while i < len(self.timesOfPos):
                yield np.array([currentposX[i], currentposY[i], currentposZ[i]])
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
        
        ani = animation.FuncAnimation(fig, update, len(self.timesOfPos), fargs=(data, line), interval=1, blit=False)
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