import interfaceRobot
import time
import struct
import math
r = interfaceRobot.Robot()

#r.initialize()
#
"""degree  = math.radians(34.445)
theTime = (3.1415 / 2) / degree
r.toSafe()
r.go(0,0)
time.sleep(5)
r.go(15,0)
time.sleep(6)
r.go(0,0)
r.go(0,30)
time.sleep(theTime)
r.go(0,0)
r.go(15,0)
time.sleep(6)
r.go(0,0)
r.go(0,30)
time.sleep(theTime)
r.go(0,0)
r.go(15,0)
time.sleep(6)
r.go(0,0)
r.go(0,30)
time.sleep(theTime)
r.go(0,0)
r.go(15,0)
time.sleep(6)
r.go(0,30)
time.sleep(theTime)
r.go(0,0)"""
r.writeCommand(7)
r.writeCommand(128)
r.toSafe()
time.sleep(5)
r.writeCommand(142)
time.sleep(0.5)
r.writeCommand(18)
time.sleep(0.5)
r.readStatus()