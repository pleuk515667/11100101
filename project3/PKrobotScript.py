import interfaceRobotPK
import time
import struct
import math
import random
import threading

GO = 1
STOP = 2
ADJUST = 3
HOLD = 99
r = interfaceRobotPK.Robot()
lock = threading.Lock()
check = HOLD
buttonState = 0
u_t = 0
speed_left = 10
speed_right = 10
def running():
    global check
    global speed_left
    global speed_right
    while 1:
        if (check == GO):
            lock.acquire()
            r.driveDirect(speed_left, speed_right)
            lock.release()
            check = HOLD
        if (check == STOP):
            print "running 0, 0"
            lock.acquire()
            r.driveDirect(0, 0)
            time.sleep(1)
            r.playWarningSong()
            time.sleep(3)
            lock.release()
            check = HOLD
        if (check == ADJUST):
            print "Adjust"
            if (u_t > 0):
                speed_left -= u_t/2
                speed_right += u_t/2
            else:
                speed_right -= u_t/2
                speed_left += u_t/2
            lock.acquire()
            r.driveDirect(speed_left, speed_right)
            lock.release()
            check = HOLD


def buttonPressCheck():
    global check
    global buttonState
    while 1:
        lock.acquire()
        byte = r.readingButton()
        lock.release()
        button = byte[3]
        if (button == '1' and buttonState == 0):
            check = 1
            time.sleep(1)
            buttonState = 1
            button = 0
        if (button == '1' and buttonState == 1):
            check = 0
            time.sleep(1)
            buttonState = 0
        time.sleep(0.015)

def PID_Control():
    global u_t
    global check
    Kp = 1
    Ki = 1
    Kd = 1
    dT = 1
    setPoint = 2
    x_1 = 0
    x_2 = 0
    x_3 = 0
    while 1:
        lock.acquire()
        wallDist = r.lightBumpLeft()
        lock.release()
        if (x1 != 0 or x2 != 0 or x3 != 0):
            e_1 = x_1 - setPoint
            e_2 = x_2 - setPoint
            e_3 = x_3 - setPoint
            u_p = Kp*e_3
            u_i = Ki*(e_1 + e_2 + e_3)*dT
            u_d = Kd*(e_3-e_2)/dT
            u_t = u_p + u_i + u_d
        x_1 = x_2
        x_2 = x_3
        x_3 = wallDist
        if (u_t != 0):
            check = ADJUST
        time.sleep(dt)



time.sleep(2)
print "Stop"
r.toStop()
time.sleep(2)
print "Start"
r.toStart()
time.sleep(2)
print "Full"
r.toFull()
time.sleep(2)
r.setStartSong()
time.sleep(1)
r.setWarningSong()
time.sleep(1)
#r.playStartSong()
#time.sleep(4)
t1 = threading.Thread(name='running', target=running)
t2 = threading.Thread(name='buttonPressCheck', target=buttonPressCheck)
t3 = threading.Thread(name='PID_Control', target=PID_Control)
t1.start()
t2.start()
t3.start()
