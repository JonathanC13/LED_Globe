import RPi.GPIO as GPIO
import time
import argparse

from MotorStub import motorStub

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)

pwm = GPIO.PWM(12, 1000) # Arbitrary

pwm.start(0) 

class runDC:



    # gets user desired RPSec then converts to duty cycle
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

    # @param: dutyLim - Calculated duty cycle from user chosen RPS (revolutions per second
    def applyDuty(self):
        
		#Stub
		#mStub = motorStub()
		
        try:
            while True:
                #RPS read from a text file that is written to by the TFTP server.
                f = open('/home/pi/Desktop/RPS','r')
                RPS = f.read()
                if (RPS == -1):
                    break
		else if (RPS >= 141):
			RPS = 141
		
                print(RPS)
                f.close()
				
				#Stub
				#RPS changes
				#RPS = mStub.changeRPS()
                
                dutyCalc = self.userRPStoDuty(RPS)
                
				#Stub
				#mStub.stubPWM(dutyCalc, RPS)
				
                pwm.ChangeDutyCycle(dutyCalc)
                time.sleep(0.1)

                #break and end after 10 seconds
                time.sleep(10)
                break
                
        except KeyboardInterrupt:
            pass
        pwm.stop()

        GPIO.cleanup()
        return;
        

    #def __init__(self, userRPS):
        #self.RPS = userRPS
    
#-- cmd line args
#parser = argparse.ArgumentParser(description = 'Enter a integer for 0 to 141.')
#parser.add_argument('integers', metavar='N', type=int, nargs='?', default='0',
#                            help='an integer for RPS.')
#args = parser.parse_args()

#print (args.integers)
#userArg = args.integers

#if isinstance(userArg, int):
 #   print("true")

#---
#-- main
run = runDC()
#applyD = run.userRPStoDuty(userArg)

run.applyDuty()
