import serial

class RoboCommunicate():
	def SerialContact():
		RoboCon = serial.Serial(‘/dev/ttyUSB0’, baudrate=115200, timeout=1)
		print(RoboCon.name)

	def SerialCloseContact():
		RoboCon.close()

	def SendCommand(int command):
		RoboCon.write(chr(command))

	def ReadData():
		RoboCon.read()
		//TODO Convert the data received