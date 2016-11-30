import serial
import time
import struct
import math
import array

#These lists are used in the setting of songs.
startSong = [0,4,86,32,87,32,88,32,96,64]
warningSong = [1,4,40,32,39,32,38,32,37,64]

#The following variables are OPCodes or PacketIDs associated with the OI of the robot.
START = 128
SAFE = 131
RESET = 7
FULL = 132
SENSOR = 142
WRITE_SONG = 140
PLAY_SONG = 141
LB = 45
LB_LEFT = 46
LB_RIGHT = 51
LB_CR = 48
DOCK_OMNI = 17
DOCK_LEFT = 52
DOCK_RIGHT = 53
CHARGING = 21

class Robot:

    #The initialization function, which begins the serial
    # communication with the robot and initializes particular values.
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
        self.currentMode = 0.0
        time.sleep(1)
        self.portClose()
        time.sleep(1)
        self.portOpen()
        #These two variables are physical properties of the robot and are used in
        # the functions that control movement.
        self.Wheel = 235.0
        self.diameter = 72.0

    #Opens the serial communication port
    def portOpen(self):
        self.ser.open()

    #Closes the port
    def portClose(self):
        self.ser.close()

    #Used to send Interface Commands to the robot
    def writeCommand(self, input):
        self.ser.write(chr(input))

    #Returns one byte of data read from the robot
    def readStatus(self):
        data = self.ser.read(1)
        byte = -1
        if (data != ''):
            byte = struct.unpack('B', data)[0]
        return byte

    #Changes mode to "Passive"
    def toStart(self):
        self.writeCommand(START)
        self.currentMode = START

    #Changes mode to "Safe"
    def toSafe(self):
        self.writeCommand(SAFE)
        self.currentMode = SAFE

    #Changes mode to "Full"
    def toFull(self):
        self.writeCommand(FULL)
        self.currentMode = FULL

    #Resets the robot, as if the battery had been removed and reinserted.
    # Changes mode to "Off". Start command must be sent to re-enter Open Interface mode.
    def toReset(self):
        self.writeCommand(RESET)
        self.currentMode = RESET

    #Changes mode to "Off"
    def toStop(self):
        self.writeCommand(173)
        self.currentMode = 173

    #Converts the input to a binary string
    def toBinaryString(self, input):
        s = ''.join([chr(input)])
        return s

    #The following functions read sensor data from the robot, then return that
    # data in byte form.
    def readingBumpWheel(self):
        self.writeCommand(SENSOR)
        self.writeCommand(7)
        byte = self.readStatus()
        byte = "{0:04b}".format(byte)
        return byte

    def readingButton(self):
        self.writeCommand(SENSOR)
        self.writeCommand(18)
        byte = self.readStatus()
        byte = "{0:04b}".format(byte)
        return byte

    def readingCliffLeft(self):
        self.writeCommand(SENSOR)
        self.writeCommand(9)
        byte = self.readStatus()
        return byte

    def readingCliffRight(self):
        self.writeCommand(SENSOR)
        self.writeCommand(12)
        byte = self.readStatus()
        return byte

    def readingCliffLeftFront(self):
        self.writeCommand(SENSOR)
        self.writeCommand(10)
        byte = self.readStatus()
        return byte

    def readingCliffRightFront(self):
        self.writeCommand(SENSOR)
        self.writeCommand(11)
        byte = self.readStatus()
        return byte

    def checkCliffs(self):
        status = 0
        status = self.readingCliffLeft() + self.readingCliffRight() + self.readingCliffLeftFront() + self.readingCliffRightFront()

        if (status > 0):
            return 1

        return 0

    # This function will drive the robot by calling the drive function
    # set speed and radius and turn clockwise and counter clockwise
    def drive(self, speed, radius, turn):
        if type(speed) != type(42):
            speed = int(speed)
        if type(radius) != type(42):
            speed = int(speed)
        if speed < -500:
            speed = -500
        if speed > 500:
            speed = 500
        if radius > 2000:
            radius = 32768
        if radius < -2000:
            radius = 32768
        speedHi, speedLow = self.splitTo2Byte(speed)

        if radius == 0:
            if turn == 'CW':
                radius = -1
            else:
                radius = 1
        radiusHi, radiusLow = self.splitTo2Byte(radius)
        self.writeCommand(137)
        self.writeCommand(speedHi)
        self.writeCommand(speedLow)
        self.writeCommand(radiusHi)
        self.writeCommand(radiusLow)

    # calling drive and sending data to drive which is a speed of the wheel and degree
    def go(self, speed=0, deg=0):
        if speed == 0:
            dirst = None
            rad = math.radians(deg)
            if rad >= 0:
                dirst = 'CCW'
            else:
                dirst = 'CW'
            finalSpeed = math.fabs(rad) * (self.Wheel / 2.0)
            self.drive(finalSpeed, 0, dirst)
        elif deg == 0:
            finalSpeed = 10.0 * speed
            rad = 32767
            self.drive(finalSpeed, rad, "CW")
        else:
            dirst = None
            radSpeed = math.radians(deg)
            finalSpeed = 10 * speed
            rad = finalSpeed / radSpeed
            if rad > 32767:
                rad = 32767
            if rad < -32767:
                rad = -32767
            if rad >= 0:
                dirst = 'CCW'
            else:
                dirst = 'CW'
            self.drive(finalSpeed, rad, dirst)
        return

    #This function sends a simple drive function to the robot.
    # The two input values are associated with the speed of a wheel.
    def driveDirect(self, speedRight, speedLeft):
        speedRight = speedRight * 10
        speedLeft = speedLeft * 10
        if speedRight < -500:
            speedRight = -500
        if speedRight > 500:
            speedRight = 500
        if speedLeft < -500:
            speedLeft = -500
        if speedLeft > 500:
            speedLeft = 500
        speedRightHi, speedRightLow = self.splitTo2Byte(speedRight)
        speedLeftHi, speedLeftLow = self.splitTo2Byte(speedLeft)
        self.writeCommand(145)
        self.writeCommand(speedRightHi)
        self.writeCommand(speedRightLow)
        self.writeCommand(speedLeftHi)
        self.writeCommand(speedLeftLow)

    #Several of the following function set a song or play a song
    def setWarningSong(self):
        self.writeCommand(WRITE_SONG)
        for i in warningSong:
            self.writeCommand(i)

    def playWarningSong(self):
        self.writeCommand(PLAY_SONG)
        self.writeCommand(1)

    def setStartSong(self):
        self.writeCommand(WRITE_SONG)
        for i in startSong:
            self.writeCommand(i)

    def playStartSong(self):
        self.writeCommand(PLAY_SONG)
        self.writeCommand(0)

    #Several of the following function are used to read sensor data from the light sensors on the robot.
    def lightBumpLeft(self):
        self.writeCommand(SENSOR)
        self.writeCommand(LB_LEFT)
        data = self.ser.read(2)
        byte = -1
        if (data != ''):
          byte = struct.unpack('>h', data)[0]
          byte = math.sqrt(byte)
        return byte

        
    def lightBumpRight(self):
        self.writeCommand(SENSOR)
        self.writeCommand(LB_RIGHT)
        data = self.ser.read(2)
        byte = -1
        if (data != ''):
          byte = struct.unpack('>h', data)[0]
          byte = math.fabs(byte)
          byte = math.sqrt(byte)   
        return byte
        
    def lightBumpCenterRight(self):
        self.writeCommand(SENSOR)
        self.writeCommand(LB_CR)
        data = self.ser.read(2)
        byte = -1
        if (data != ''):
          byte = struct.unpack('>h', data)[0]
          byte = math.sqrt(byte)
        return byte
        
    def lightBumper(self):
        self.writeCommand(SENSOR)
        self.writeCommand(LB)
        byte = self.readStatus()
        return byte

    def dockOmni(self):
        self.writeCommand(SENSOR)
        self.writeCommand(DOCK_OMNI)
        byte = self.readStatus()
        return byte
    def dockRight(self):
        self.writeCommand(SENSOR)
        self.writeCommand(DOCK_RIGHT)
        byte = self.readStatus()
        return byte

    def dockLeft(self):
        self.writeCommand(SENSOR)
        self.writeCommand(DOCK_LEFT)
        byte = self.readStatus()
        return byte   
    def chargingState(self):
        self.writeCommand(SENSOR)
        self.writeCommand(CHARGING)
        byte = self.readStatus()
        return byte 
    # spit value in to high and low bitwise
    def splitTo2Byte(self, value):
        bitValue = 0
        if value >= 0:
            bitValue = value
        else:
            bitValue = (1 << 16) + value
        return ((bitValue >> 8) & 0xFF, bitValue & 0xFF)
        
