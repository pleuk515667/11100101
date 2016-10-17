import interfaceRobotPK
import time
import struct
import math
import random
import threading

#  Initializing Instance Variables...
#Instance of the interface
r = interfaceRobotPK.Robot()

#Instance of the 'Lock' mechanism to control which thread has control of the robot at any time
lock = threading.Lock()

#Check has an arbitrary resting value, and is used to set the current action of the robot.
# This variable allows the threads to "communicate" with one another.
check = 99

#Primarily used by Thread3 (function "buttonPressCheck()")
buttonState = 0

'''
The following functions all correspond to a running thread.
  A lock variable is used to determine which thread has control of the robot at any
  given time, and the 'check' and 'buttonState' variables are both used in determining
  which action the robot should take for any given event.
'''

#Thread1 will be running the following function, whose purpose is to control any
# movement actions to be taken by the robot.
def running():
    global check
    while 1:
        if (check == 1):
            x = random.randint(5, 10) * 2
            y = random.randint(5, 10) * 2
            print "runing"
            print x
            print y
            lock.acquire()
            r.driveDirect(x, y)
            lock.release()
            check = 99
        if (check == 0):
            print "running 0, 0"
            lock.acquire()
            r.driveDirect(0, 0)
            time.sleep(1)
            r.playWarningSong()
            time.sleep(3)
            lock.release()
            check = 99
        if (check == 2):
            lock.acquire()
            r.driveDirect(0, 0)
            r.playWarningSong()
            time.sleep(0.3)
            r.go(-5, 0)
            time.sleep(1)
            x = random.randint(5, 10) * 2
            y = random.randint(3, 5) * 2
            r.driveDirect(x, y)
            lock.release()
            check = 99
        if (check == 3):
            lock.acquire()
            r.driveDirect(0, 0)
            r.playWarningSong()
            time.sleep(0.3)
            r.go(-5, 0)
            time.sleep(1)
            x = random.randint(3, 5) * 2
            y = random.randint(5, 10) * 2
            r.driveDirect(x, y)
            lock.release()
            check = 99
        if (check == 4):
            lock.aquire()
            r.driveDirect(0, 0)
            r.playWarningSong()
            lock.release()
            check = 99

#Thread2 will be running this function, whose purpose is to moniter the state of
# the front bumpers as well as the wheel drop sensors.
def sensorCheck():
    global check
    while 1:
        lock.acquire()
        byte = r.readingBumpWheel()
        lock.release()
        b1 = byte[3]
        b2 = byte[2]
        # b3 = byte[1]
        # b4 = byte[0]
        if (b1 == '1'):
            check = 2
        if (b2 == '1'):
            check = 3
        # if (b3 == '1' or b4 == '1'):
        #    check = 4
        time.sleep(0.015)

#Thread3 will be running this funtion, whose purpose is to moniter the state of
# the button presses and tell Thread1 to take the appropriate action.
def buttonPressCheck():
    global check
    global buttonState
    while 1:
        lock.acquire()
        byte = r.readingButton()
        lock.release()
        button = byte[3]
        print button
        if (button == 1 and buttonState == 0):
            print 'reached first if'
            # if(r.checkCliffs() == 1):
            #    check = 4
            # else:
            #    check = 1
            check = 1
            time.sleep(1)
            buttonState = 1
            button = 0
        if (button == 1 and buttonState == 1):
            print 'reached second if'
            # if(r.checkCliffs() == 1):
            #    check = 4
            # else:
            #    check = 0
            check = 0
            time.sleep(1)
            buttonState = 0
        print 'past ifs reached'
        time.sleep(0.015)

#Thread4 will be running this function, whose purpose is to moniter the cliff
# detection sensors.
def cliffWheelCheck():
    global check
    global buttonState
    while 1:

        lock.acquire()
        '''
        cliffLeft = r.readingCliffLeft()
        cliffRight = r.readingCliffRight()
        cliffLeftFront = r.readingCliffLeftFront()
        cliffRightFront = r.readingCliffRightFront()
        '''
        lock.release()
        anyCliff = cliffLeft + cliffRight + cliffLeftFront + cliffRightFront
        print anyCliff
        if (anyCliff > 0):
            check = 4

        time.sleep(0.015)

#The following are a series of "sleep" commands and commands that change the mode of the
# robot. After the robot is in the appropriate mode, the Start and Warning songs are set.
# Finally, the thread variables are initialized and the threads are started.
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
r.playStartSong()
time.sleep(4)
t1 = threading.Thread(name='running', target=running)
t2 = threading.Thread(name='sensorCheck', target=sensorCheck)
t3 = threading.Thread(name='buttonPressCheck', target=buttonPressCheck)
t4 = threading.Thread(name='cliffWheelCheck', target=cliffWheelCheck)
t1.start()
t2.start()
t3.start()
t4.start()
