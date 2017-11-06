TFTP DC motor job request
1. write 0 to RPS.txt
2. execute runDC.py
3. poll for user input and then write it to RPS.txt
4. the runDC.py will read the value from RPS.txt and calculate the duty cycle to apply, loops constantly reading the file.
5. When TFTP connection severed, write -1 to RPS so it breaks loop

This program on the RPi controlling the motor.
