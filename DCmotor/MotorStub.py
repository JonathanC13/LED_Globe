
class motorStub:
	def stubPWM(self, duty, RPS):
        
		print ("Received duty cycle of: " + str(duty) + ", where the RPS was: " + str(RPS))
		
		# Compares duty passed to expected based on RPS
		expectedDuty = userRPStoDuty(RPS)
		if (expectedDuty == duty):
			print "Duty from runDC, " + str(duty) + ", is equal to calculated duty using RPS, "+ str(expectedDuty) 
		else:
			print "Duty from runDC, " + str(duty) + ", is NOT equal to calculated duty using RPS, "+ str(expectedDuty) 
	    
	    
	def userRPStoDuty(self, RPS):

		#current DC motor: #:29DCM28 - 8500 RPM. 141 RPSec @9V (no load)
		rpsMAX = 141
		dcV = 9        
		
		if(RPS < 0):
			RPS = 0
		else if (RPS >= 141):
			RPS = 141
			
		#(Theo aV/Vmax) x rpsMAX = desired rps
		
		
		#RPS to duty cycle (%)
		duty = (float(RPS)*100.0/float(rpsMAX))
		
		
		print ("DC motor will reach " + str(RPS) + " RPS momentarily")
		print ("Duty cycle applied: " + str(duty) + "%")
		
		#Theo average V = Vmax x duty
		Tav = float(dcV * (duty/100.0))
		

		print ("Theoretical aveage voltage applied: " + str(Tav) + "V, of max " + str(dcV) + "V")

		#duty-pwm relation equation. duty = (pwm x 100)/T

		return duty

class motorInputs:
	input = 0
	
	def changeRPS(self):     
		
		return input
	
	def setInput(self, testInput):
		input = float(testInput)
		
#JUnit example assertEquals()