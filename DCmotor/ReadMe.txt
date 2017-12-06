TFTP Server DC motor job request
1. write 0 to RPS.txt
2. execute runDC.py
3. poll for user input and then write it to RPS.txt
4. the runDC.py will read the value from RPS.txt and calculate the duty cycle to apply, loops constantly reading the file.
5. When TFTP connection severed, write -1 to RPS so runDC.py breaks loop

This program on the RPi controlling the motor.

runDC.py Sequence
1. Setup hardware outputs.
2. Read value from RPS.txt that represents the desired revolutions per second for the DC motor.
3. Convert the RPS to a duty cycle percentage.
4. Apply the duty cycle through the pwm output.
5. Repeat steps 2 to 4 until the value within RPS.txt is -1 indicating the end, so the program can break its infinite loop.
6. When -1 read, clean up hardware outputs so no errors for future executions using the ports.
