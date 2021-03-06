import serial
import time
import thread
import math
ser;
#task 1
#initialize the serial and open port
def portConnect ():
    try:
        ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
        ser.open();
    except serialError:
        print "Port Connection Error"

#closing serial port
def portClose():
    ser.close()
    if ser.is_open() == ture:
        print "ERROR Port is not close"
    else:
        print "Port is close"

#write command to the port
def writeCommand(input):
    ser.write(chr(input))

#read command from the port
def readStatus():
    while ser.inWaiting() > 0:
        print ser.read(1)

#task2
class robot:
    #initialize global variable
    powerButton = 0.0
    currentMode = 0.0
    Wheel = 235.0
    diameter = 72.0
    
    #go to start mode
    def toStart():
        writeCommand(128)
        currentMode = 128
        
    #go to safe mode
    def toSafe():
        toStart()
        time.sleep(0.05)
        writeCommand(131)
        currentMode = 131
        
    #go to Full mode
    def toFull():
        writeCommand(132)
        currentMode = 132
    
    #go to reset mode
    def toReset():
        toStart()
        time.sleep(0.05)
        writeCommand(7)
        currentMode = 7
    
    #go to Stop mode
    def toStop():
        toStart()
        time.sleep(0.05)
        writeCommand(173)
        currentMode = 173
    
    #initialize the robot class, First thing to call
    def initialize():
        print "initialize Roomba....Connect to Port"
        portConnect()
        currentMode = 0
        powerButton = 0
    
    #convert to bynay string
    def toBinaryString(input):
        s = ''.join([chr(input)])
        return s
    
    #read button state
    def readButton():
        #todo
        
    #this fuction will drive the robot by calling the drive function
    #set spped and radius and turn clockwise and couter clockwise
    def drive(speed, radius, turn):
        if type(speed) != type 42:
            speed = int(speed)
        if type(radius) != type 42:
            speed = int(speed)
        if speed < -500:
            speed = -500
        if speed > 500:
            speed = 500
        if radius > 2000:
            radius = 32768
        if radius < -2000:
            radius = 32768
        speedHi, speedLow = splitTo2Byte(speed)

        if radius == 0:
            if turn == 'right':
                radius = -1
            else:
                radius = 1
        radiusHi, radiusLow =  splitTo2Byte(radius)
        writeCommand(137)
        writeCommand(speedHi)
        writeCommand(speedLow)
        writeCommand(radiusHi)
        writeCommand(radiusLow)
#calling drive and sending data to drive
    def go(speed=0,deg=0):
        if speed == 0:
            rad = math.radians(deg_per_sec)
            if rad >= 0:
                dirstr = 'CCW'
            else:
                dirst = 'CW'
            finalSpeed = math.fabs(rad) * (Wheel/2.0)
            drive(finalSpeed,0,dirst)
        elif deg == 0:
            finalSpeed = 10.0*speed
            rad = 32767
            drive(finalSpeed,rad)
        else:
            radSpeed = math.radians(deg)
            finalSpeed = 10*speed
            rad = finalSpeed/radSpeed
            if rad > 32767:
                rad = 32767
            if rad < -32767:
                rad = -32767
            drive(finalSpeed, rad)
        return
    
#spit value in to high and low
    def splitTo2Byte(value):
        bitValue;
        if value >= 0:
            bitValue = value
        else:
            bitValue = (1<<16) + value
        return ((bitValue >> 8) & 0xFF, bitValue & 0xFF)
