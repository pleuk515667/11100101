import interfaceRobotPK
import time
import struct
import math
import random
import threading
r = interfaceRobotPK.Robot()

time.sleep(0.5)
r.toStop()
time.sleep(2)
r.toStart()
time.sleep(2)
r.toSafe()
time.sleep(2)

byte = 0
def running():
		#something
		a =1
def bumpCheck():
	while 1:
			time.sleep(0.2)
			byte = r.readingBumpWheel()
			b1 = byte[0]
			print byte
			if(b1 == 1): 
				print "bumb" 

t1 = threading.Thread(name='running', target = running)
t2 = threading.Thread(name='bumpCheck', target = bumpCheck)


t2.start()

