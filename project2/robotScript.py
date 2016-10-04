import interfaceRobot
import time
import struct
import math
r = interfaceRobot.Robot()

def move(speed=0, radian=0, waitTime=1):
	r.go(speed,radian)
	time.sleep(waitTime)
	r.go(0,0)
	time.sleep(1)

turning = 27.5
pi = math.pi
dT = 2.5

degree  = math.radians(turning)
theTime = (pi / 2) / degree
time.sleep(2)
r.toStop()
time.sleep(2)
print "Starting robot..."
r.toStart()
time.sleep(2)
print "Entering Safe mode..."
r.toSafe()
time.sleep(2)
bit = 0
while bit != 1:
	r.writeCommand(142)
	r.writeCommand(18)
	bit = r.readStatus()
	print bit
time.sleep(2)
move(0,0,1)
move(10,0,dT)
move(0,30,theTime)
move(10,0,dT)
move(0,30,theTime)
move(10,0,dT)
move(0,30,theTime)
move(10,0,dT)
move(0,30,theTime)
r.portClose()

