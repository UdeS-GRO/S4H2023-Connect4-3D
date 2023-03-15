#Alexandre Baril: Created: january 16 2023, Sherbrooke
#Alexandre Baril: Modified: february 8 2023, Sherbrooke

import struct
import numpy as np
import serial
import time
import sys
import serial.tools.list_ports
from PyQt5 import QtWidgets
app = QtWidgets.QApplication(sys.argv)
#from GameBoardRepresentation import gameboard
#game = gameboard()

theta = 0.001
phi = 0.001

class MotorMove:
    ### Math variable
    BicepLen:float = 0.1425
    ForearmLen:float = 0.1425
    J1Offset:int = 0
    J2Offset:int = 0

    ## Communication variables
    mssg1:str = "0000"
    mssg2:str = "0000"
    mssg3:str = "0000"
    mssg4:str = "0"             #default is go to 45deg
    mssg5:str = "0"             #default is no reset of magazines
    mssg6:str = "0"             #default is not reset
    mssg7:str = "0"             #default is no victory
    mssg:str = "0000000000000000"

    Zpos:int = 0 #zposition

    #serOpenCR = serial.Serial('/dev/ttyUSB0', 9600)        #Linux or Pi
    serOpenCR = serial.Serial('COM3', baudrate= 9600, timeout=2.0)  #Windows

    ## Methods
    def __init__(self):
        self.init_motor(self)

    def sendMsg(self, Shouldermessage:int, Elbowmessage:int):
        '''
        communication order:    [j1 j1 j1 j1  --> int 0-9 times 4
                                j2 j2 j2 j2   --> int 0-9 times 4
                                z z z z       --> int 0-9 times 4
                                Pos to go     --> int 0 = 45deg, 1 = 90deg
                                Pos to reset  --> int 0 = nothing, 1 = 45deg, 2 = 90deg
                                ]
        ex: 01230123012300
        '''
        
        ### First Joint Position
        Shoulderlength = len(str(Shouldermessage))
        if Shoulderlength == 1:
            mssg1 =  "000" + str(Shouldermessage)
        elif Shoulderlength == 2:
            mssg1 =  "00" + str(Shouldermessage)
        elif Shoulderlength == 3:
            mssg1 =  '0' + str(Shouldermessage)
        elif Shoulderlength == 4:
            mssg1 = str(Shouldermessage)
        if mssg1 == "":
            mssg1 = "0000"

        ### Second Joint Position
        Elbowlength = len(str(Elbowmessage))
        if Elbowlength == 1:
            mssg2 =  "000" + str(Elbowmessage)# + '|'
        elif Elbowlength == 2:
            mssg2 =  "00" + str(Elbowmessage)# + '|'
        elif Elbowlength == 3:
            mssg2 =  '0' + str(Elbowmessage)# + '|'
        elif Elbowlength == 4:
            mssg2 = str(Elbowmessage)# + '|'
        if mssg2 == "":
            mssg2 = "0000"
        
        ### Z Position
        '''
        floor0 = 2750
        floor1 = 2450
        floor2 = 2150
        floor3 = 1850
        floor4 = 1550
        floor5 = 1250
        '''
        Zlength = len(str(self.Zpos))
        if Zlength == 1:
            mssg3 =  "000" + str(self.Zpos)# + '|'
        elif Zlength == 2:
            mssg3 =  "00" + str(self.Zpos)# + '|'
        elif Zlength == 3:
            mssg3 =  '0' + str(self.Zpos)# + '|'
        elif Zlength == 4:
            mssg3 = str(self.Zpos)# + '|'
        if mssg3 == "":
            mssg3 = "0000"

        ### Pick to go to, 0 = 45deg, 1 = 90deg
        #self.mssg4 = "1"

        ### Reset of magazines, 0 = nothing, 1 = 45deg, 2 = 90deg
        #self.mssg5 = "1"

        mssg = mssg1 + mssg2 + mssg3 + self.mssg4 + self.mssg5 + self.mssg6 + self.mssg7
        print(mssg)
        if self.serOpenCR.isOpen():
            self.serOpenCR.write(mssg.encode().rstrip())
            print("msg Sent: " + mssg)
        
        self.mssg5 = "0"
        self.mssg7 = "0"
        return

    def readMsg(self):
        answer:str = ""
        if self.serOpenCR.isOpen():
            StartTime = time.time()
            while self.serOpenCR.inWaiting()==0:
                pass
            while  self.serOpenCR.inWaiting() > 0:
                answer = self.serOpenCR.readline().decode()
                print("Answer is : " + answer)
                self.serOpenCR.flushInput()
        return int(answer)

    def rad2Servo(self, angleRad:float):
        angleServo = angleRad * 4095 / (2*np.pi)
        return angleServo

    def lawOfCos(self, a, b, c):
        modulus = np.power(a, 2) + np.power(b, 2) - np.power(c, 2)
        return np.arccos(modulus / (2*a*b))

    def cart2cyl(self, cartX:float, cartY:float):

        t2:float = (cartX**2 + cartY**2 - self.BicepLen**2 - self.ForearmLen**2) / (2 * self.BicepLen * self.ForearmLen)
        theta2:float = np.arccos(t2)
        t1 = (self.ForearmLen*np.sin(theta2)) / (self.BicepLen*np.cos(theta2))
        theta1:float = np.arctan(cartX/cartY) + np.arctan(t1)

        theta = theta1
        phi = theta2

        J1:int = round(self.rad2Servo(self, theta) * 2) + self.J1Offset
        J2:int = round(self.rad2Servo(self, phi)) + self.J2Offset

        if J1 > 4095:
            J1 = 4095
        if J2 > 4095:
            J2 = 4095

        print("phi: " + str(J1))
        print("theta: " + str(J2))

        return J1, J2

    def moveCart(self, gameXpos, gameYpos, gameZpos):

        servoShoulderAngle, servoElbowAngle = self.cart2cyl(self, gameXpos, gameYpos)
        self.sendMsg(self, servoShoulderAngle, servoElbowAngle)
    
    def moveJoint(self, J1, J2):
        self.sendMsg(self, J1, J2)

    def sendVictory(self, winner):
        if winner == 0:
            self.mssg5 = "3"
            self.mssg7 = "1"
            self.sendMsg(self, 0, 0)
        elif winner == 1:
            self.mssg5 = "3"
            self.mssg7 = "2"
            self.sendMsg(self, 0, 0)


