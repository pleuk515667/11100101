Class RoboState(RoboCommunicate):

	def StartPassiveMode():
		super().SendCommand(128)

	def SafeMode():
		super().SendCommand(131)

	def PowerOff():
		super().SendCommand(133)

	def MoveForward():
		#Move Foward

	def MoveBackwards():	 
		#Move Backwards

	def RotateClockwise():
	
	def RotateCounterClockwise():

		