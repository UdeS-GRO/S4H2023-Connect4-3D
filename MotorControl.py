#Alexandre Baril: Created: january 16 2023, Sherbrooke
#Alexandre Baril: Modified: february 8 2023, Sherbrooke

import struct
import numpy as np
import serial
import time
import sys
from PyQt5 import QtWidgets
app = QtWidgets.QApplication(sys.argv)
from Connect_12_PI.GameBoardRepresentation import gameboard
game = gameboard()

### Math variables
BicepLen = float(150)
ForearmLen = float(150)

## Communication variables
mssg1:str = "0000"
mssg2:str = "0000"
mssg:str = "0000"

#ser = serial.Serial('/dev/ttyUSB0', 9600)
ser = serial.Serial('COM5', 9600)


## Functions

def sendMsg(Shouldermessage:int, Elbowmessage:int):
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
    if ser.isOpen():
        ser.write(mssg.encode().rstrip())
        print("msg Sent: " + mssg)
    #while(readMsg() != message): pass
    return

def readMsg():
    answer:str = ""
    if ser.isOpen():
        
        while ser.inWaiting()==0: pass
        while  ser.inWaiting() > 0:
            answer = ser.readline(8).decode()
            print("Answer is : " + answer)
            ser.flushInput()
    return int(answer)

def rad2Servo(angleRad):
    angleServo = angleRad * 4095 / (2*np.pi)
    return angleServo

def cart2cyl(cartX:int, cartY:int):
    C2:float = (cartx**2 + np.power(cartY, 2) - np.power(BicepLen, 2) - np.power(ForearmLen, 2)*1.0) / (2 * BicepLen * ForearmLen)
    S2:float = np.sqrt(1-C2)
    theta = np.arccos(C2)     ###cos-1
    phiX = (ForearmLen * S2 * cartX) + ((BicepLen + ForearmLen*C2)*cartY)
    phiY = ((BicepLen + ForearmLen*C2)*cartX)-(ForearmLen * S2 * cartY)
    phi = np.arctan2(((ForearmLen * S2 * cartX) + ((BicepLen + ForearmLen*C2)*cartY)), (((BicepLen + ForearmLen*C2)*cartX)-(ForearmLen * S2 * cartY)))

    thetaInt:int = round(rad2Servo(theta))
    phiInt:int = round(rad2Servo(phi))

    return thetaInt, phiInt

def Interpolation(posXStart: int, posYStart: int, posXEnd: int, posYEnd: int):
    jointAngles = cart2cyl(posXStart, posYStart)
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
        jointAngles.append(cart2cyl(positionsX[i], positionsY[i]))
        #print("angle: " + str(jointAngles[i]))
    
    return positionsX, positionsY

def moveZ(height):
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

def pos2cart(letterPos: str, numberPos: str, floorLevel: str):
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


vari:int = 1
vari2:int = 1
##### SETUP #####
var = True
lastCoord = pos2cart('A', '1', 'f0')
sens:bool = True
##### MAIN #####

while var == True:
    
    gameXpos, gameYpos, gameZpos = game.submit_inputs_xyz()

    servoShoulderAngle, ServoElbowAngle = cart2cyl(gameXpos, gameYpos)
    
    sendMsg(gameXpos, gameYpos)
    msgReceived = readMsg()
    

    '''vari = 2000
    vari2 = 2500
    sendMsg(vari, vari2)
    msgReceived = readMsg()
    time.sleep(2)

    vari = 4000
    vari2 = 1000
    sendMsg(vari, vari2)
    msgReceived = readMsg()
    time.sleep(2)
'''
    '''
    #receive from OpenCR card:
        #encodervalue, motorShoulderposition, motorElbowposition
    #dataPack = struct.pack('iii', encodervalue, motorShoulderPosition, motorElbowPosition)
    #data = struct.unpack('iii', dataPack)

    ###sends to OpenCR

    #position1
    coord = pos2cart('C', '3', 'f5') #coordonates = import from jacob
    cartPosX, cartPosY = Interpolation(lastCoord[0], lastCoord[1], coord[0], coord[1])
    for pos in range(0, len(cartPosY)):
        motorShoulder, motorElbow = cart2cyl(cartPosX[pos], cartPosY[pos])
        sendMsg(motorShoulder, motorElbow, 0)
        print("ShoulderAngle: " + str(motorShoulder) + "   \t ElbowAngle: " + str(motorElbow))
    lastCoord = coord
    #if other positions (to move out of the way of an object or something): copy-paste the 7 lines above
    

    moveZ(coord[2])
    
    #var = False
    '''
    
### Comm that functions below ###
'''
    #vari = 0

    #print('Running. Press CTRL-C to exit.')
    #with serial.Serial("COM5", 9600, timeout=1) as ser:
    #time.sleep(0.1) #wait for serial to open
    if ser.isOpen():
        #print("{} connected!".format(ser.port))
        #try:
        #while True:
        cmd= vari #input("Enter command : ")
        ser.write(str(vari).encode()) #.encode())
        #time.sleep(1) #wait for arduino to answer
        while ser.inWaiting()==0: pass
        if  ser.inWaiting()>0: 
            answer=ser.readline()
            print("Answer is : " + str(answer))
            ser.flushInput() #remove data after reading
            #time.sleep(5)
        
        #except KeyboardInterrupt:
        #    print("KeyboardInterrupt has been caught.")
'''
