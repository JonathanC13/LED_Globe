This program is stored on the central RPi that communicates with the RPi controlling the motor and Arduino controlling the LED ring.

Required files:
Pillow library:
	up to date pip: $ python3 -m pip install -U pip
	$ python3 -m pip install Pillow
	
Cimpl.py (No tests, file from Sysc1005 lab, Prof. Bailey)
	Using some functions.
	$ sudo apt-get install python-imaging-tk
	$ sudo apt-get install python-imaging
	
ImageConversion.py
	from Cimpl import * (Dependency to Cimpl)

	functions

	1. Get image as parameter, and tile toggle	blackWhite
	2. shrink image to 48 x X pixels		blackWhite
		2.1 Shrunk image. Save as, then re input for filtering.
		2.2 Original Y/48 = ratio. X = Org X / ratio	
	3. Get signal interval for LEDs based on 30 RPS recommended. signalInterval
	4. Filter to black and white			blackWhite
	5. Fill arrays for each LEDs			blackWhite

UserInputScript.py
	Sequence to get bit array of user specificied image

Python Imaging Library, for your version of Python
	1. python -m pip install --upgrade pip
	2. python -m pip install Pillow


To RUN
1. Go to directory of ImageConversion.py
2. python3 UserInputScript.py -s test.jpg
