'''
Class: CSCE 274-002 Group 2
Assignment: Project 3
Date: Nov 15, 2016
Authors: Nicholas Belegrinos, Bradley Follet, Nattapon Donratanapat
'''

import interfaceRobotPK
import time
import struct
import math
import random
import threading

#The following variables are values that allow the threads to "communicate" with eachother.
# The 'running' thread takes a particular action based on the value of the variable 'check'.
GO = 1
STOP = 2
ADJUST = 3
ARC = 4
ROTATE = 5
HAZARD = 6
WHEEL_DROP = 7
DOCK_FORWARD = 8
DOCK_FRONT_LEFT = 9
DOCK_FRONT_RIGHT = 10
DOCK_LEFT = 11
DOCK_RIGHT = 12
HOLD = 99
check = HOLD

#Initialization of several global variables.
r = interfaceRobotPK.Robot()
lock = threading.Lock()
setPoint = 0;
buttonState = 0
INIT_V = 5
u_t = 0
speed_left = 5
speed_right = 5
dockStatus = 0


#Function associated with 'thread1'. This function is directly responsible for movement actions taken by the robot.
# Based of the check value, this function will tell the robot to take a particular action.
def running():
    global check
    global speed_left
    global speed_right
    global u_t
    global setPoint
    while 1:
        if (check == WHEEL_DROP):
            print "Wheel drop detected!"
            buttonState = 0
            check = STOP
        if (check == HAZARD):
            lock.acquire()
            r.driveDirect(0, 0)
            r.playWarningSong()
            time.sleep(0.3)
            r.go(-5, 0)
            time.sleep(0.5)
            lock.release()
            check = HOLD            
        if (check == GO):
            lock.acquire()
            r.driveDirect(int(speed_left), int(speed_right))
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
        if (check == ADJUST && dockStatus = 0):
            lock.acquire()
            speed_left = INIT_V
            speed_right = INIT_V
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
            
            print "Left speed = "+str(speed_left) 
            print "Right speed = "+str(speed_right)
            r.driveDirect(int(speed_left), int(speed_right))
            lock.release()
            check = HOLD
        if(check == ARC && dockStatus = 0):
            lock.acquire()
            wallDist= r.lightBumpRight()
            lock.release()
            while (wallDist < 2):
              speed_left = int(setPoint) 
              speed_right = 2
              lock.acquire()
              r.driveDirect(speed_right, speed_left)
              wallDist= r.lightBumpRight()
              lock.release()
              time.sleep(0.2)
            check = HOLD
        if (check == ROTATE && dockStatus = 0):
            lock.acquire()
            wallFront = r.lightBumpCenterRight()
            while (wallFront > 3):
               r.driveDirect(10, -10)
               time.sleep(0.2)
               wallFront = r.lightBumpCenterRight()
            lock.release()
            check = HOLD
        if (check == DOCK_FORWARD):
            #TODO pick up the front both
        if (check == DOCK_FRONT_LEFT):
            #TODO pick up the front GREEN
        if (check == DOCK_FRONT_RIGHT):
            #TODO pick up the front RED
        if (check == DOCK_LEFT):
            #TODO NOT pick up the front LEFT got something
        if (check == DOCK_RIGHT):
            #TODO pick up the front RIGHT got something
         

#Function associated with 'thread2'. The function keeps track of the button presses and sets the robot
# to the appropriate state when a button press is detected.
def buttonPressCheck():
    global check
    global buttonState
    while 1:
        lock.acquire()
        byte = r.readingButton()
        lock.release()
        button = byte[3]
        if (button == '1' and buttonState == 0):
            check = GO
            time.sleep(1)
            buttonState = 1
            button = 0
        if (button == '1' and buttonState == 1):
            check = STOP
            time.sleep(1)
            buttonState = 0
        time.sleep(0.015)

#This function is associated with 'thread3'. It controls how the robot moves and corrects itself.
def PID_Control():
    global u_t
    global check
    global buttonState
    global speed_left
    global speed_right
    global setPoint
    
    #These are our gain values.
    Kp = 0.8
    Ki = 0.3
    Kd = 0.05
    dT = 0.2
    
    #Here is our predetermined distance value.
    lock.acquire()
    setPoint = 8
    lock.release()
    
    #These variables are used in the PID controller equation.
    x_1 = 0
    x_2 = 0
    x_3 = 0
    while dockStatus == 0:    
        lock.acquire()
        wallDist = r.lightBumpRight()
        wallFront = r.lightBumpCenterRight()
        lock.release()
        x_1 = x_2
        x_2 = x_3
        x_3 = wallDist
        print "-------"
        print "Wall Dist = " +str(wallDist)
        print "Wall Front = " +str(wallFront)
        if (x_1 > 1 and x_2 > 1 and x_3 > 1 and wallDist > 1):
            e_1 = x_1 - setPoint
            e_2 = x_2 - setPoint
            e_3 = x_3 - setPoint
            u_p = Kp*e_3
            u_i = Ki*(e_1 + e_2 + e_3)*dT
            u_d = Kd*(e_3-e_2)/dT
            u_t = u_p + u_i + u_d
        
        print "U_T = " +str(math.fabs(u_t))
        if (math.fabs(u_t) > 0.5 and buttonState == 1):
            check = ADJUST
        elif (wallDist < 1):
            check = ARC
        if (wallFront > 10):
            check = ROTATE
        time.sleep(dT)
        
#This function is associated with 'thread4'. It is responsible for checking if the wheel drop or bumper sensors go off.
def sensorCheck():
    global check
    while 1:
        lock.acquire()
        byte = r.readingBumpWheel()
        lock.release()
        b1 = byte[3]
        b2 = byte[2]
        b3 = byte[1]
        b4 = byte[0]
        if (b1 == '1'):
            check = HAZARD
        if (b2 == '1'):
            check = HAZARD
        if (b3 == '1' or b4 == '1'):
            check = WHEEL_DROP
        time.sleep(0.015)
        
#This function is associated with 'thread5'. It is responsible for checking if the cliff sensors go off.
def dock():
    global check
    global dockStatus
    while 1:
      both = r.dockOmni()
      time.sleep(0.25)
      right = r.dockRight()
      time.sleep(0.25)
      left = r.dockLeft()
      time.sleep(0.25)
      check = HOLD
      if(both != 0 or right!= 0 or left != 0):
        dockStatus = 1
      if(both == 172 or both == 161 or both == 173):
        check = DOCK_FORWARD
      elif(both == 164 or both == 165):
        check = DOCK_FRONT_LEFT
      elif(both == 168 or both == 169):
        check = DOCK_FRONT_RIGHT
      elif(both == 0):
        if(right != 0):
          check = DOCK_RIGHT
        elif(left != 0):
          check = DOCK_LEFT




     

#Here, the robot is set to the appropriate mode and all the threads are started.
r.toStop()
time.sleep(1.5)
r.toStart()
time.sleep(1.5)
r.toSafe()
time.sleep(1.5)
r.setWarningSong()
r.setStartSong()
time.sleep(1)
r.playStartSong()
time.sleep(4)
print "start"
t1 = threading.Thread(name='running', target=running)
t2 = threading.Thread(name='buttonPressCheck', target=buttonPressCheck)
t3 = threading.Thread(name='PID_Control', target=PID_Control)
t4 = threading.Thread(name='sensorCheck', target=sensorCheck)
t5 = threading.Thread(name='dock', target=dock)
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
