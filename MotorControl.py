#Alexandre Baril, 17 janvier 2023, Sherbrooke

import struct
#import numpy as np

dataPack = struct.pack('iii', 0, 5, 10)
data = struct.unpack('iii', dataPack)

def cart2cyl(cartX, cartY):
    cylX = cartX
    cylY = cartY
    print([cylX, cylY])
    return [cylX, cylY]

def Interpolation(posStart, posEnd):
    print("interpolation")
    return posStart + posEnd

def goDown(height):
    print("height = " + height)
    return

#sends the 3 motor positions to the openCR board

print(cart2cyl(data[0], data[1]))

print("hello")