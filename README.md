# LED_Globe - September 2017 – December 2017 
https://github.com/JonathanC13/LED_Globe

## Description

- Developed the system architecture, raspberry and Arduino programs, 3D model design for the globe’s ring, and the unit tests.<br/> 
- The programs were to control the motor, LED pattern, and converting an image to the correct size and output pattern.<br/>
- The test method used was Functionality-Based Input Domain modeling for each function.<br/>
- Regrettably unfinished due to 3d printed model defective.<br/>

## Updates after course finished<br />
03/14/19 - Videos (mp4) in Videos_and_pictures have become unavailable, therefore:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - HallSensor_Video.mp4 now on Youtube: https://youtu.be/QEPRrl4xu5o<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -> In this project, when the hall sensor detects the magnet the LED image pattern is reset to indicate the beginning of the pattern.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - LEDcheck_video.mp4 now on Youtube: https://youtu.be/COrFFD_RpA8<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -> This is just to demo the LEDs working to validate that the (whacky) wiring was all connected.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Pattern.mp4 now on Youtube: https://youtu.be/dGLgj0t9ru0<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -> This is the demo of the LED image pattern being executed. Each vertical array in the binary image pattern is executed in quick succession to match the LED ring rotation speed.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - No video for completed LED POV Globe due to female connector on the 3D printed ring meant to connect the motor to was defective due to 3D printing problem (While printing the connector was mostly filled with supporting material to build the hollow cylinder). Even if the connection could be made, I doubt the small motor could support the ring's weight and spin it fast enough for the POV effect to be present. 

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

## End Remark

I'm sorry I couldn't complete the project to a functional state, not being able to get the motor into the LED ring component was embarrassing. Thank you to my teammates for tolerating me.

Denis Chupin <br/>
Eliab Woldeyes

Sincerely, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;Jonathan
