import serial

class RoboCommunicate():
	def SerialContact():
		RoboCon = serial.Serial(‘/dev/ttyUSB0’, baudrate=115200, timeout=1)
		print(RoboCon.name)

	def SerialCloseContact():
		RoboCon.close()
	#I am not sure about int, python should not have type
	def SendCommand(command):
		RoboCon.write(chr(command))

	def ReadData():
		RoboCon.read()
		//TODO Convert the data received
