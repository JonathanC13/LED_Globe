#Jonathan Chan
#SYSC3010
# When testing with stub, comment GPIO.
import RPi.GPIO as GPIO

import time
import argparse
import os, sys

#from MotorStub import *

# When testing with stub, comment GPIO and pwm functions.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT) # GPIO pin 12
pwm = GPIO.PWM(12, 1000) # Arbitrary 1000 for frequency
pwm.start(0)

# -----

class runDC:



    # gets user desired Revolutions per second then converts to duty cycle
    def userRPStoDuty(self, RPS):

        # Alternate DC motor: #:29DCM28 - 8500 RPM. 141 RPSec @9V (no load)
        # rpsMAX = 141

        #current DC motor: - 13800 RPM. 230 RPSec @3V (no load)
        rpsMAX = 230
        dcV = 3     # DC voltage

        # Check lower and upper bounds
        if(RPS < 0):
            RPS = 0
        elif (RPS >= rpsMAX):
            RPS = rpsMAX

        #(Theo aV/Vmax) x rpsMAX = desired rps

        #RPS to duty cycle (%)
        duty = (float(RPS)*100.0/float(rpsMAX))

        #Theo average V = Vmax x duty
        print(str(duty))

        #duty-pwm relation equation. duty = (pwm x 100)/T

        return duty

    # For testing added parameters: inRPS and stub instance
    # def applyDuty(self, inRPS, stubInst):

    # This function reads the desired revolutions per second from a text file, sends it to be converted to the duty cycle, and then applies it to the pwm pin
    def applyDuty(self):
        #stub = stubInst
        #UpperLim = 141     9 DC motor, 8500 RPM = 141 RPS
        UpperLim = 230    # 3 DC motor, 13800 RPM = 230 revolutions per second
        try:
            while True:
			#RPS read from a text file that is written to by the TFTP server.

                #Input RPS Tests ----
                #RPS = inRPS
                # ---

                # Actual Inputs ---
                f = open('//home//pi/Desktop//LED_Globe//DCmotor//RPS.txt','r')

                RPS = f.read()

		        # -----

                # End condition, if the file contains a value of -1
                if (int(RPS) == -1): # If file has -1, end motor
                    fRPS = 0

                    dutyCalc = self.userRPStoDuty(fRPS)

                    #Stub for motor ---
                    #stub.stubPWM(dutyCalc)
                    # ---

                    # Actual motor control ---
                    pwm.ChangeDutyCycle(dutyCalc)
                    # ---

                    break
                elif(int(RPS) < 0): #Cannot have rps of less than 0
                    RPS = 0
                elif (int(RPS) > UpperLim):
                    RPS = UpperLim

                fRPS = float(RPS)


		        # -----
                f.close()
                # ----
                dutyCalc = self.userRPStoDuty(fRPS)

				#Stub for motor ---
                #stub.stubPWM(dutyCalc)
				# ---

				# Actual motor control ---
                pwm.ChangeDutyCycle(dutyCalc)
                # ---
                time.sleep(2)   #Wait 2 seconds then read the speed file again

                #break and end after 10 seconds
                #time.sleep(10)

                # for testing, break after one input
                #break

        # Can end the program and end safely with Ctrl+c
        except KeyboardInterrupt:
            pass
        # handle invalid value in text file, this error would be expected
        except ValueError:
            print ("Could not convert data to an integer.")
        # unexpected error
        except:
            print ("Unexpected error:", sys.exc_info()[0])

	# When testing with stub, comment GPIO and pwm functions.
        print("Ending")
        pwm.stop()

        GPIO.cleanup()

        # -----
        return;



    #def __init__(self, userRPS):

#-- cmd line args for direct control of RPS input
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
run = runDC()
#---

# --- if receive input from command line
#applyD = run.userRPStoDuty(userArg)

# -- When testing comment out ---
run.applyDuty()
# ---
