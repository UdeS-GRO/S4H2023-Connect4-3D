#Alexandre Baril, january 16 2023, Sherbrooke

import struct
import numpy as np
import serial
import time


### variables
BicepLen = float(150)
ForearmLen = float(150)

### parameters
#ser = serial.Serial('/dev/ttyUSB0', 9600)
ser = serial.Serial('COM5', 9600)

def sendMsg(shoulderAngle:int, elbowAngle:int, Zheight:int):
    #ser.write(shoulderAngle)
    #ser.write(elbowAngle)
    #ser.write(moveZ(Zheight))

    #ardu= serial.Serial('COM5',9600, timeout=.1)
    time.sleep(1)
    ser.write(shoulderAngle)
    time.sleep(1)
    #ardu.close()
        
    print("msg Sent: " + str(ser.write(shoulderAngle)))
    return

def readMsg():
    msgRead = ser.read()
        
    print(msgRead)
    return

def rad2Servo(angleRad):
    angleServo = angleRad * 360 / (2*np.pi)
    return angleServo

def cart2cyl(cartX, cartY):
    C2 = (cartX**2 + cartY**2 - BicepLen**2 - ForearmLen**2) / (2 * BicepLen * ForearmLen)
    S2 = (1-C2) ** 0.5
    theta = np.arccos(C2)     ###cos-1
    phiX = (ForearmLen * S2 * cartX) + ((BicepLen + ForearmLen*C2)*cartY)
    phiY = ((BicepLen + ForearmLen*C2)*cartX)-(ForearmLen * S2 * cartY)
    phi = np.arctan2(((ForearmLen * S2 * cartX) + ((BicepLen + ForearmLen*C2)*cartY)), (((BicepLen + ForearmLen*C2)*cartX)-(ForearmLen * S2 * cartY)))

    theta = rad2Servo(theta)
    phi = rad2Servo(phi)

    return theta, phi

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



##### SETUP #####
var = True
lastCoord = pos2cart('A', '1', 'f0')

##### MAIN #####
while var == True:
    print("next: send msg -")
    sendMsg(500, 5, 5)
    sendMsg(1250, 5, 5)
    readMsg()

    #receive from OpenCR card:
        #encodervalue, motorShoulderposition, motorElbowposition
    #dataPack = struct.pack('iii', encodervalue, motorShoulderPosition, motorElbowPosition)
    #data = struct.unpack('iii', dataPack)

    ###sends to OpenCR
'''
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
'''    
    #var = False
    