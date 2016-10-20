import interfaceRobotPK
import time
import struct
import math
import random
import threading

#  Initializing Variables...
#Instance of the interface
r = interfaceRobotPK.Robot()
r.toStop()
time.sleep(1)
r.toStart()
time.sleep(1)
r.toFull()

#reads a single byte from the robot and prints it out in 8bit binary form
"""while 1:
    time.sleep(0.15)
    r.writeCommand(142)
    r.writeCommand(18)
    print "-----------------"
    raw = r.ser.read(1)
    #formatted = struct.unpack("B", raw)[0]
    #binary = "{0:08b}".format(formatted)

    #print formatted

'''
while 1:
    time.sleep(1.1)
    r.writeCommand(149)
    r.writeCommand(2)
    r.writeCommand(18)
    r.writeCommand(35)

    print "-----------------"
    raw = r.ser.read(1)
    formatted = struct.unpack('B', raw)[0]
    binary = "{0:08b}".format(formatted)

    print formatted
    print binary
'''"""
while 1:
    time.sleep(2)
    print "---------------------["
    r.writeCommand(142)
    r.writeCommand(20)
    data = r.ser.read(2)
    #print data.decode("utf-8")
    byte = -1
    if (data != ''):
        byte = struct.unpack('>h', data)[0]

    print byte
    r.driveDirect(-5, 5)
    time.sleep(3)