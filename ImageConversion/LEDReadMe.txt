Adruino sketch program for the LED ring is stored on the Raspberry Pi

Adruino Sketch configuration:
	Tools > Board > Arduino/Genuino Uno

ImageConversion.py populates 2 text files.
1. LEDpattern.txt is filled with the bit pattern of the image
2. SignalTime.txt is filled with the signal interval that the LED columns should fire.

LEDcontrol.ino
1. adruino program defines a variable, delayTime, with the value in SignalTime.txt and fills a 2d array with the values from LEDpattern.txt. IF the values in LEDpattern need a character to seperate the values, edit the "write" in ImageConversion.py. e.g. adding a "," after each value. 1,0,0,0 <<end
2. polling in loop for first interrupt from hall sensor
3. After interrupt it will execute the 2d array from the first column.
4. After every column it delays the delayTime then sends the next column

TO DO:
	1. Execute LEDcontrol.ino so that delayTime value is set from SignalTIme.txt and fills a 2d array with the values from LEDpattern.txt
	2. script to execute the arduino sketch program.
