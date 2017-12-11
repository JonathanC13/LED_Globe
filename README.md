# LED_Globe

## Nomenclature (according to our final report) ----------------
    
RPi1 --> Raspberry Pi v3

RPi2 --> Raspberry Pi v1

## Overview of Subdirectories ----------------------------------


**3d_model_design:**		Contains PDF rendered images of the LED ring aparatus that we 3D-printed.


**DCmotor:**			All files related to the DC motor componenet of the system. Refer to the README file under this folder.


**ImageConversion:**		All files related to converting an image to a bit pattern. Refer to the README under this folder.


**Server_It4:**			Incomplete implementation of TFTP server/client.


**UIApplication:**		Android Studio project of the user interface for the system. Execution instructions are:
      			
	-	App was built using Android Studio 2 to be able to work on it in the labs. 
		If using an updated version some libraries might have to be updated.
	-	To test the Bluetooth functionality of the app, the script BtServiceScript.py
		must be running *first* on RPi1 before running the application (see 
		instructions for this script below).
	-	An Android mobile device must be used to test the app since an emulator cannot 
		provide Bluetooth functionality. The device must also be paired to RPi1 (check
		for device name "RPI_Carleton").
	-	Once the device is connected to your machine, run the app from Android Studio.


**Videos_and_Pictures:**		Contains demos of working components and pictures of the system.


**hallTest:**			Contains an Arduino sketch file used for testing the Hall effect sensor.


**ledTest:**			Refer to README.


**BtServiceScript.py:**		A python script providing Bluetooth service for the user interface. Execution instructions are:
			
	-	This script executes on RPi1.
	-	Make sure python bluetooth library is installed by executing the following commands in terminal:
					
					sudo apt-get install bluetooth
					
					sudo apt-get install bluez
			
	-	Use python 2 to call the script with:
					
					python BtServiceScript.py

	-	As seen on  line 27, logging for this script outputs to "/var/log/raspibtsrv.log" by default.


**OperationNoNetwork:**		Instructions on running a new bit pattern on the LED ring.


**README.md:**			This file.


**TestingDesignPhase.docx:**	Test plan document.


**hall.py:**			Python file for testing the Hall effect sensor on RPi1.
