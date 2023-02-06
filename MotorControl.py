#Alexandre Baril, january 16 2023, Sherbrooke

import struct
import numpy as np
import serial
import time


### variables
BicepLen = float(150)
ForearmLen = float(150)
msg1:str = ""
msg2:str = ""
msg:str = ""

### parameters
#ser = serial.Serial('/dev/ttyUSB0', 9600)
ser = serial.Serial('COM5', 115200, timeout=1)

def sendMsg(Shouldermessage:int, Elbowmessage:int):
    Shoulderlength = len(str(Shouldermessage))
    if Shoulderlength == 3:
        msg1 =  '0' + str(Shouldermessage) + '|'
    elif Shoulderlength == 4:
        msg1 = str(Shouldermessage) + '|'

    Elbowlength = len(str(Elbowmessage))
    if Elbowlength == 3:
        msg2 =  '0' + str(Elbowmessage) + '|'
    elif Elbowlength == 4:
        msg2 = str(Elbowmessage) + '|'

    msg = msg1 + msg2
    #print(msg)
    if ser.isOpen():
        ser.write(msg.encode().rstrip())
        print("msg Sent: " + msg)
    #while(readMsg() != message): pass
    return

def readMsg():
    answer:str = ""
    if ser.isOpen():
        
        while ser.inWaiting()==0: pass
        while  ser.inWaiting() > 0:
            answer = ser.readline(4).decode()
            print("Answer is : " + answer)
        ser.flushInput()
    return int(answer)

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


vari:int = 0
##### SETUP #####
var = True
lastCoord = pos2cart('A', '1', 'f0')
sens:bool = True
##### MAIN #####

while var == True:
    
    vari += 100
    sendMsg(vari, vari+125)
    msgReceived = readMsg()
    #sendMsg(vari+500)
    #msgReceived = readMsg()
    
    #print(msgReceived)

    #time.sleep(0.01)

    '''
    print("next: send msg -")
    sendMsg(500, 5, 5)
    sendMsg(1250, 5, 5)
    readMsg()

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
