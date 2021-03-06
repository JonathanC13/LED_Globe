#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#       Hall Effect Sensor
#
# This script tests the sensor on GPIO17.
#
# Author : Matt Hawkins (modified by Eliab Woldeyes)
# Date   : 11/26/2017
#
# http://www.raspberrypi-spy.co.uk/
#
# Original script found at:
#     https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/hall.py
#
#--------------------------------------

# Import required libraries
import time
import datetime
import RPi.GPIO as GPIO

# Called if sensor output changes.
def sensorCallback(channel):

  # Generate a time stamp.
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  
  if GPIO.input(channel):
    # No magnet
    print("Sensor HIGH " + stamp)
  else:
    # Magnet
    print("Sensor LOW " + stamp)

def main():

  # Wrap main content in a try block so we can
  # catch the user pressing CTRL-C and run the
  # GPIO cleanup function. This will also prevent
  # the user seeing lots of unnecessary error
  # messages.
  try:

    # Loop until users quits with CTRL-C.
    while True :
      time.sleep(0.1)

  except KeyboardInterrupt:
    # Reset GPIO settings.
    GPIO.cleanup()

# Tell GPIO library to use GPIO references.
GPIO.setmode(GPIO.BCM)

print("Setup GPIO pin as input on GPIO17")

# Set Switch GPIO17 (pin 17) as input.
# Pull high by default.
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set GPIO17 to execute callback function once rising or falling
# edge detected.
GPIO.add_event_detect(17, GPIO.BOTH, callback=sensorCallback, bouncetime=100)

print("Setup done and event detection added. Now sensing...")

if __name__=="__main__":
   main()
