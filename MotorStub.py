from random import randint

class motorStub:
	def stubPWM(self, duty, RPS):
                # Could recalculate duty from RPS here and compare for testing.
		print ("Received duty cycle of: " + str(duty) + ", where the RPS was: " + str(RPS))
		expectedDuty = userRPStoDuty(RPS)
		
		
	def changeRPS(self):
                
		rps = randint(0,100)
		
		return rps
	    
	    
        def userRPStoDuty(self, RPS):

            #current DC motor: #:29DCM28 - 8500 RPM. 141 RPSec @9V (no load)
            rpsMAX = 141
            dcV = 9        
            
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

