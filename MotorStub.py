from random import randint

class motorStub:
	def stubPWM(duty):
		print duty
		
	def changeRPS():
		rps = randint(0,100)
		return rps