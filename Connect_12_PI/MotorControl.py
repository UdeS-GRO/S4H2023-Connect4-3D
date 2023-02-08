#Alexandre Baril: Created: january 16 2023, Sherbrooke
#Alexandre Baril: Modified: february 8 2023, Sherbrooke

import struct
import numpy as np
import serial
import time
import sys
from PyQt5 import QtWidgets
app = QtWidgets.QApplication(sys.argv)
#from GameBoardRepresentation import gameboard
#game = gameboard()

theta = 0.001
phi = 0.001

class MotorMove:
    ### Math variable
    BicepLen = float(200)
    ForearmLen = float(200)

    ## Communication variables
    mssg1:str = "0000"
    mssg2:str = "0000"
    mssg:str = "0000"

    ## Motor control
    vari:int = 1
    vari2:int = 1

    #ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser = serial.Serial('COM5', 9600)

    ## Methods
    def __init__(self):
        self.init_motor(self)

    def sendMsg(self, Shouldermessage:int, Elbowmessage:int):
        Shoulderlength = len(str(Shouldermessage))
        if Shoulderlength == 1:
            mssg1 =  '000' + str(Shouldermessage) + '|'
        elif Shoulderlength == 2:
            mssg1 =  '00' + str(Shouldermessage) + '|'
        elif Shoulderlength == 3:
            mssg1 =  '0' + str(Shouldermessage) + '|'
        elif Shoulderlength == 4:
            mssg1 = str(Shouldermessage) + '|'

        Elbowlength = len(str(Elbowmessage))
        if Elbowlength == 1:
            mssg2 =  '000' + str(Elbowmessage) + '|'
        elif Elbowlength == 2:
            mssg2 =  '00' + str(Elbowmessage) + '|'
        elif Elbowlength == 3:
            mssg2 =  '0' + str(Elbowmessage) + '|'
        elif Elbowlength == 4:
            mssg2 = str(Elbowmessage) + '|'

        mssg = mssg1 + mssg2
        #print(mssg)
        if self.ser.isOpen():
            self.ser.write(mssg.encode().rstrip())
            print("msg Sent: " + mssg)
        #while(readMsg() != message): pass
        return

    def readMsg(self):
        answer:str = ""
        if self.ser.isOpen():
            
            while self.ser.inWaiting()==0: pass
            while  self.ser.inWaiting() > 0:
                answer = self.ser.readline(8).decode()
                print("Answer is : " + answer)
                self.ser.flushInput()
        return int(answer)

    def rad2Servo(self, angleRad:float):
        angleServo = angleRad * 4095 / (2*np.pi)
        print(angleServo)
        return angleServo

    def cart2cyl(self, cartX:int, cartY:int):
        '''
        C2:float = (cartX**2 + cartY**2 - self.BicepLen**2 - self.ForearmLen**2) / (2 * self.BicepLen * self.ForearmLen)
        S2:float = 1-C2**(0.5)  
        theta = np.arccos(C2)     ###cos-1
        phiX = (self.ForearmLen * S2 * cartX) + ((self.BicepLen + self.ForearmLen*C2)*cartY)
        phiY = ((self.BicepLen + self.ForearmLen*C2)*cartX)-(self.ForearmLen * S2 * cartY)
        phi = np.arctan2(((self.ForearmLen * S2 * cartX) + ((self.BicepLen + self.ForearmLen*C2)*cartY)), (((self.BicepLen + self.ForearmLen*C2)*cartX)-(self.ForearmLen * S2 * cartY)))
        '''

        #phi = np.arccos((cartX*cartX + cartY*cartY - self.BicepLen*self.BicepLen - self.ForearmLen*self.ForearmLen) / (2 * self.BicepLen * self.ForearmLen))
        #theta = np.arctan(cartX/cartY) - np.arctan((self.ForearmLen*np.sin(phi)) / (self.BicepLen + self.ForearmLen*np.cos(phi)))
        
        phi = np.arccos((pow(cartX, 2) + pow(cartY, 2) - pow(self.BicepLen, 2) - pow(self.ForearmLen, 2)) / (2 * self.BicepLen * self.ForearmLen))
        if cartX < 0 and cartY < 0:
            phi = (-1) * phi
        print(phi*1000000)
        theta = np.arctan(cartX / cartY) - np.arctan((self.ForearmLen * np.sin(phi)) / (self.BicepLen + self.ForearmLen * np.cos(phi)))
        print(theta*1000000)
        thetaInt:int = self.rad2Servo(self, theta) #round(self.rad2Servo(self, theta))
        #print(theta)
        #print(thetaInt)
        phiInt:int = self.rad2Servo(self, phi) #round(self.rad2Servo(self, phi))

        return thetaInt, phiInt

    def Interpolation(self, posXStart: int, posYStart: int, posXEnd: int, posYEnd: int):
        jointAngles = self.cart2cyl(self, posXStart, posYStart)
        increment = 100
        posx = posXStart
        posy = posYStart
        diffX = posXEnd - posXStart
        diffY = posYEnd - posYStart
        #print(str(diffX) + "\t" + str(diffY))
        stepX = diffX / increment
        stepY = diffY / increment
        
        positionsX = list()
        positionsY = list()
        jointAngles = list()
        for i in range(increment):
            positionsX.append(posXStart + (i+1)*stepX)
            positionsY.append(posYStart + (i+1)*stepY)
            #print("i: " + str(i) + "\tpositionX: " + str(positionsX[i]) + "  \tpositionY: " + str(positionsY[i]))
            jointAngles.append(self.cart2cyl(self, positionsX[i], positionsY[i]))
            #print("angle: " + str(jointAngles[i]))
        
        return positionsX, positionsY

    def moveZ(self, height):
        motorEncoder = 0
        while motorEncoder < height:
            #motor.movedown
            #ser.read()
            #print(motorEncoder)
            motorEncoder += 5
        while motorEncoder > 0:
            #motor.moveup
            #ser.read()
            #print(motorEncoder)
            motorEncoder -= 10
        
        return

    def pos2cart(self, letterPos: str, numberPos: str, floorLevel: str):
        match letterPos:
            case 'A':
                posx = -75
            case 'B':
                posx = -25
            case 'C':
                posx = 25
            case 'D':
                posx = 75

        match numberPos:
            case '1':
                posy = 0
            case '2':
                posy = 50
            case '3':
                posy = 100
            case '4':
                posy = 150

        match floorLevel:
            case 'f0':
                ztarget = 300
            case 'f1':
                ztarget = 250
            case 'f2':
                ztarget = 200
            case 'f3':
                ztarget = 150
            case 'f4':
                ztarget = 100
            case 'f5':
                ztarget = 50
        
        #print(str(posx) + "\t" + str(posy))
        return posx, posy, ztarget

    def moveCart(self, gameXpos, gameYpos, gameZpos):
        #gameXpos, gameYpos, gameZpos = game.submit_inputs_xyz()

        '''servoShoulderAngle, servoElbowAngle = self.cart2cyl(self, gameXpos, gameYpos)
        print(str(servoShoulderAngle) + str(servoElbowAngle))
        self.sendMsg(self, servoShoulderAngle, servoElbowAngle)
        msgReceived = self.readMsg(self)
        time.sleep(0.5)'''
    
    def moveJoint(self, J1, J2):
        MotorMove.sendMsg(MotorMove, J1, J2)
        msgReceived = MotorMove.readMsg(MotorMove)

'''while(True):
    vari = 1000
    vari2 = 500
    servoShoulderAngle, servoElbowAngle = MotorMove.cart2cyl(MotorMove, vari, vari2)
    MotorMove.sendMsg(MotorMove, vari, vari2)
    msgReceived = MotorMove.readMsg(MotorMove)
    time.sleep(2)

    vari = 2000
    vari2 = 1500
    servoShoulderAngle, servoElbowAngle = MotorMove.cart2cyl(MotorMove, vari, vari2)
    MotorMove.sendMsg(MotorMove, vari, vari2)
    msgReceived = MotorMove.readMsg(MotorMove)
    time.sleep(2)'''


