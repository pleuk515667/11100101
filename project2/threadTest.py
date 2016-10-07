import threading
import time
import Queue

check = 1
def loop1():
		a = time.clock()
		while 1:
			if check == 1:
				time.sleep(1)
				print a
				#change value of a from loop 2?
			else:
				break
		print "off loop"

def loop2():
		b = 0
		global check 
		while b < 10:
		 	time.sleep(1)
		 	b += 1
		 	print b
		check = 2


def Main():
	t1 = threading.Thread(name="loop1", target=loop1)
	t2 = threading.Thread(name="loop2", target=loop2)
	t1.start()
	t2.start()
	print("Main complete")

if __name__ == '__main__':
	Main()

