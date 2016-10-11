import interfaceRobotPK
import time
import struct
import math
import random
import threading
r = interfaceRobotPK.Robot()


check = 0
left = 0
right = 0
def running():
		global check
		while 1:
			if(check == 1):
				print left
				print right
				r.driveDirect(left,right)
			if(check == 0):
				r.driveDirect(0,0)
		
def sensorCheck():
		global check
		global left
		global right
		while 1:
			left = random.randint(-5,5)
			right = random.randint(-5,5)
			check = 1
			time.sleep(5)
			check = 0;
			time.sleep(5)
		


def Main():
	r.toStop()
	time.sleep(2)
	r.toReset()
	time.sleep(2)
	r.toStart()
	time.sleep(2)
	r.toSafe()
	time.sleep(2)
	print "about to start"
	time.sleep(2)
	t1 = threading.Thread(name='running', target = running)
	t2 = threading.Thread(name='sensorCheck', target = sensorCheck)
	t1.start()
	t2.start()
	r.toStop()
if __name__ == '__main__':
	Main()
