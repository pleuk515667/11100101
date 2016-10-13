import interfaceRobotPK
import time
import struct
import math
import random
import threading
r = interfaceRobotPK.Robot()
lock = threading.Lock()
check = 99
buttonState = 0
def running():
		global check
		while 1:
			if(check == 1):
				
				x = random.randint(5,10) *2
				y = random.randint(5,10) *2
				print "runing"
				print x
				print y
				lock.acquire()
				r.driveDirect(x,y)
				lock.release()
				check = 99
			if(check == 0):
				print "running 0, 0"
				lock.acquire()
				r.driveDirect(0,0)
				time.sleep(1)
				r.playWarningSong()
				time.sleep(3)
				lock.release()
				check = 99
			if (check ==2):
				lock.acquire()
				r.driveDirect(0,0)
				time.sleep(0.3)
				r.go(-5,0)
				time.sleep(1)
				x = random.randint(5,10) *2
				y = random.randint(3,5) *2
				r.driveDirect(x,y)
				lock.release()
				check = 99
			if (check == 3):
				lock.acquire()
				r.driveDirect(0,0)
				time.sleep(0.3)
				r.go(-5,0)
				time.sleep(1)
				x = random.randint(3,5) *2
				y = random.randint(5,10) *2
				r.driveDirect(x,y)
				lock.release()
				check = 99
		
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
			if(b1 == '1'):  
				check = 2
			if(b2 == '1'):
				check = 3
			time.sleep(0.015)

def buttonPressCheck(): 
		global check
		global buttonState
		while 1:
			lock.acquire()
			byte = r.readingButton()
			lock.release()
			button = byte[3]
			print button
			if(button == '1' and buttonState == 0): 
				check = 1
				time.sleep(1)
				buttonState = 1
				button = 0
			if(button == '1' and buttonState == 1): 
				check = 0
				time.sleep(1)
				buttonState = 0
			time.sleep(0.015)


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
t1 = threading.Thread(name='running', target = running)
t2 = threading.Thread(name='sensorCheck', target = sensorCheck)
t3 = threading.Thread(name='buttonPressCheck', target = buttonPressCheck)
t1.start()
t2.start()
t3.start()



 
