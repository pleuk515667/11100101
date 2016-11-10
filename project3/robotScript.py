import interfaceRobotPK
import time
import struct
import math
import random
import threading

GO = 1
STOP = 2
ADJUST = 3
ARC = 4
ROTATE = 5
HOLD = 99
r = interfaceRobotPK.Robot()
lock = threading.Lock()
check = HOLD
buttonState = 0
INIT_V = 5
u_t = 0
speed_left = 5
speed_right = 5
def running():
    global check
    global speed_left
    global speed_right
    global u_t
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
            print "---------------------"
            print "Adjusting..."
            if (u_t > 0.0):
                u_t = u_t/2
                speed_right = speed_right - u_t
                speed_left = speed_left + u_t
            else:
                change = math.fabs(u_t)/2
                speed_right = speed_right + change
                speed_left = speed_left - change
            lock.acquire()
            print "Left speed = "+str(speed_left) 
            print "Right speed = "+str(speed_right)
            r.driveDirect(int(speed_left), int(speed_right))
            lock.release()
            time.sleep(0.5)
            lock.acquire()
            speed_left = INIT_V
            speed_right = INIT_V
            lock.release()
            check = HOLD
        if(check == ARC):
            lock.acquire()
            speed_left = 10
            speed_right = 2
            r.driveDirect(speed_right, speed_left)
            time.sleep(0.2)
            lock.release()
            check = HOLD
        if (check == ROTATE):
            lock.acquire()
            wallFront = r.lightBumpCenterRight()
            while (wallFront > 5):
               r.driveDirect(5, -5)
               time.sleep(0.5)
               wallFront = r.lightBumpCenterRight()
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
            check = STOP
            time.sleep(1)
            buttonState = 0
        time.sleep(0.015)

def PID_Control():
    global u_t
    global check
    global buttonState
    Kp = 0.01
    Ki = 0.01
    Kd = 0.01
    dT = 0.15
    lock.acquire()
    setPoint = r.lightBumpRight()
    lock.release()
    x_1 = 0
    x_2 = 0
    x_3 = 0
    while 1:
    
        lock.acquire()
        wallDist = r.lightBumpRight()
        wallFront = r.lightBumpCenterRight()
        lock.release()
        x_1 = x_2
        x_2 = x_3
        x_3 = wallDist
        print "-------"
        print "Wall Dist = " +str(wallDist)
        if (x_1 != 0 and x_2 != 0 and x_3 != 0 and wallDist != 0):
            e_1 = x_1 - setPoint
            e_2 = x_2 - setPoint
            e_3 = x_3 - setPoint
            errorCheck = math.fabs(e_1)+math.fabs(e_2)+math.fabs(e_3)
            errorCheck = errorCheck/3
            u_t = 0
            if(errorCheck >5):              
                u_p = Kp*e_3
                u_i = Ki*(e_1 + e_2 + e_3)*dT
                u_d = Kd*(e_3-e_2)/dT
                u_t = u_p + u_i + u_d
        
        if (u_t != 0 and buttonState == 1):
            check = ADJUST
        if (wallDist <5):
            check = ARC
        difference = math.fabs(wallDist - wallFront)
        print difference
        if (difference < 60):
            check = ROTATE
        time.sleep(dT)
        


time.sleep(2)
print "Stop"
r.toStop()
time.sleep(2)
print "Start"
r.toStart()
time.sleep(2)
print "Full"
r.toSafe()
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
