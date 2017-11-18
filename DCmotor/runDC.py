# When testing with stub, comment GPIO.
#import RPi.GPIO as GPIO

import time
import argparse
import os, sys

from MotorStub import *

# When testing with stub, comment GPIO and pwm functions.
#GPIO.setmode(GPIO.BOARD)

#GPIO.setup(12, GPIO.OUT)

#pwm = GPIO.PWM(12, 1000) # Arbitrary

#pwm.start(0) 

# -----

class runDC:



    # gets user desired RPSec then converts to duty cycle
    def userRPStoDuty(self, RPS):

        #current DC motor: #:29DCM28 - 8500 RPM. 141 RPSec @9V (no load)
        rpsMAX = 141
        dcV = 9        
        if(RPS < 0):
            RPS = 0
        elif (RPS >= 141):
            RPS = 141
		
        #(Theo aV/Vmax) x rpsMAX = desired rps
        
        
        #RPS to duty cycle (%)
        duty = (float(RPS)*100.0/float(rpsMAX))
        
        
        #print ("DC motor will reach " + str(RPS) + " RPS momentarily")
        #print ("Duty cycle applied: " + str(duty) + "%")
        
        #Theo average V = Vmax x duty
        Tav = float(dcV * (duty/100.0))
        

        #print ("Theoretical aveage voltage applied: " + str(Tav) + "V, of max " + str(dcV) + "V")

        #duty-pwm relation equation. duty = (pwm x 100)/T

        return duty

    # For testing added parameters: inRPS and stub instance
    def applyDuty(self, inRPS, stubInst):

        stub = stubInst
        try:
            while True:
			#RPS read from a text file that is written to by the TFTP server.
	
		#Input Tests ----
		#RPS changes
                RPS = inRPS
                # ---

		# Actual Inputs ---	
		#f = open('/home/pi/Desktop/RPS','r')
		#RPS = f.read()
		# -----
		
                if (RPS == -1):
                    fRPS = 0

                    dutyCalc = self.userRPStoDuty(fRPS)
                    
                    #Stub for motor ---
                    stub.stubPWM(dutyCalc)
                    # ---

                    # Actual motor control ---
                    #pwm.ChangeDutyCycle(dutyCalc)
                    # ---
                    
                    break
                elif(RPS < 0):
                    RPS = 0
                elif (RPS >= 141):
                    RPS = 141

                fRPS = float(RPS)
				
		# -----
                #f.close()
                # ----
                dutyCalc = self.userRPStoDuty(fRPS)

				#Stub for motor ---
                stub.stubPWM(dutyCalc)
						# ---
						
				# Actual motor control ---
						#pwm.ChangeDutyCycle(dutyCalc)
						# ---
                time.sleep(2)

                #break and end after 10 seconds
                #time.sleep(10)
                
                # for testing, break after one input
                break
                
        except KeyboardInterrupt:
            pass
        except ValueError:
            print ("Could not convert data to an integer.")
        except:
            print ("Unexpected error:", sys.exc_info()[0])

	# When testing with stub, comment GPIO and pwm functions.
        #pwm.stop()

        #GPIO.cleanup()

        # -----
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
#-- main -- When testing comment out ---
#run = runDC()
#---

# --- if receive input from command line
#applyD = run.userRPStoDuty(userArg)

# -- When testing comment out ---
#run.applyDuty()
# ---
