import serial
import time
import struct
import math

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
class Robot:
    # task1: open port write port and read port
    # initialize the robot class, connect the serial, and set the variable


    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
        self.currentMode = 0.0
        self.Wheel = 235.0
        self.diameter = 72.0

    # Opening serial port
    def portOpen(self):
        self.ser.open()

    # closing serial port
    def portClose(self):
        self.ser.close()

    # write command to the port
    def writeCommand(self, input):
        self.ser.write(chr(input))

    # read command from the port
    def readStatus(self):
        data = self.ser.read(1)
        byte = -1
        if (data != ''):
            byte = struct.unpack('B', data)[0]
        return byte

        # go to start mode

    def toStart(self):
        self.writeCommand(START)
        self.currentMode = START

    # go to safe mode
    def toSafe(self):
        self.writeCommand(SAFE)
        self.currentMode = SAFE

    # go to Full mode
    def toFull(self):
        self.writeCommand(FULL)
        self.currentMode = FULL

    # go to reset mode
    def toReset(self):
        self.writeCommand(RESET)
        self.currentMode = RESET

    # go to Stop mode
    def toStop(self):
        self.writeCommand(173)
        self.currentMode = 173

    # convert to bynay string
    def toBinaryString(self, input):
        s = ''.join([chr(input)])
        return s

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

    def setWarningSong(self):
        self.writeCommand(WRITE_SONG)
        self.writeCommand(1)
        self.writeCommand(4)
        self.writeCommand(40)
        self.writeCommand(32)
        self.writeCommand(39)
        self.writeCommand(32)
        self.writeCommand(38)
        self.writeCommand(32)
        self.writeCommand(37)
        self.writeCommand(64)

    def playWarningSong(self):
        self.writeCommand(PLAY_SONG)
        self.writeCommand(1)

    def setStartSong(self):
        self.writeCommand(WRITE_SONG)
        self.writeCommand(0)
        self.writeCommand(4)
        self.writeCommand(86)
        self.writeCommand(32)
        self.writeCommand(87)
        self.writeCommand(32)
        self.writeCommand(88)
        self.writeCommand(32)
        self.writeCommand(96)
        self.writeCommand(64)

    def playStartSong(self):
        self.writeCommand(PLAY_SONG)
        self.writeCommand(0)

    def lightBumpLeft(self):
        self.writeCommand(SENSOR)
        self.writeCommand(LB_LEFT)
        data = self.ser.read(2)
        2_byte = -1
        if (data != ''):
          2_byte = struct.unpack('>h', data)[0]
        return 2_byte

        
    def lightBumpRight(self):
        self.writeCommand(SENSOR)
        self.writeCommand(LB_RIGHT)
        data = self.ser.read(2)
        2_byte = -1
        if (data != ''):
          2_byte = struct.unpack('>h', data)[0]
        return 2_byte

    def lightBumper(self):
        self.writeCommand(SENSOR)
        self.writeCommand(LB)
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
