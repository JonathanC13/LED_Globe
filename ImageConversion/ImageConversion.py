#Jonathan Chan
#Sysc3010
#Bit array generation for LEDs
from __future__ import print_function
import argparse

import os, sys
import PIL as pillow
import PIL.Image

from Cimpl import *

led = 48#number of LEDs, Actual is 13 LEDs

class ImageConversion:

	global led

	def thumbNail(self,img):

		hori = self.calcHori(get_width(img), get_height(img))
                # hori of 0 will result in an ValueError down the line

		size = hori, int(led)
		infile = img.get_filename()

		#for infile in sys.argv[1:]:
		file = os.path.splitext(os.path.basename(infile))[0]
		file = file + "thumbnail.jpg"
		try:
			im = PIL.Image.open(infile)

			im.thumbnail(size, PIL.Image.LANCZOS)
                                # hori of 0 will result in an Type error

			im.save(file, "JPEG")
		except:
			print ("Unexpected error ", sys.exc_info()[0])
			#print ("cannot create thumbnail for '%s'" % infile)

		return file

	def calcHori(self, width, height):
		if(width <= 0 or height <= 0):
			#print ("calcHori: 0 or negative parameter. Width: " + str(width) + " height: " + str(height))
			return 0
		else:
			ratio = float(float(height)/int(led))

			fhor = float(width/ratio)

			hor = int(fhor)

			#6 bytes in 6 micro seconds
			#1000000 changes in a second
			# set upper bound to squeeze image horizontal is larger
			#Arbitrary 250 , 20 micro second intervals
			if(hor >= 250):
				hor = 250
			elif (hor < 1):
				hor = -1

		return hor

	def black_and_white(self, img):

		black = create_color(0, 0, 0)
		white = create_color(255, 255, 255)

		for x, y, col in img:
			red, green, blue = col

			brightness = (red + green + blue) / 2
			if brightness < 128:
				set_color(img, x, y, black)
			else:
				set_color(img, x, y, white)

	# fill bitArray AND write to file
	def bitArray(self, img):
		# empty the file
		open("LEDpattern.txt", "w").close()

		f = open("LEDpattern.txt","a")
		r, c = get_height(img), get_width(img);

		# example: w, h = 8, 5.
		# 5 lists with 8 items each
		#Matrix = [[0 for x in range(w)] for y in range(h)]
		bitMatrix = [[0 for h in range(r)] for w in range(c)]

		for j in range(0,r):
			#print ' '
			for i in range(0, c):
				(r,g,b) = get_color(img, i, j) # x, y. origin top left
				sum = r+g+b								# left to right, top to bottom

				if sum != 0:
					#print 1,
					bitMatrix[i][j] = 1	# x, y. origin top left
					f.write("1,")								#
				else:
					#print 0,
					bitMatrix[i][j] = 0
					f.write("0,")

			f.write("/")
		f.close()
		return bitMatrix


		# add checks for type, values
		# pre condition: black and white image

	# Honestly this method could be simply print a 2d array.
	# But we'll have it only print 0s and 1s
	def printBitArray(self, matrix):
		numrows = len(matrix[0])
		numcols = len(matrix)
		validBit = True

		for y in range(0,numrows):
			print (' ')
			for x in range(0, numcols):
				chk = matrix[x][y]
				if (chk != 0 and chk !=1):
					validBit = False
					break

				print (matrix[x][y] , end="")
			if(validBit == False):
				print ("Contains invalid value that is not a 0 or 1: " + str(matrix[x][y]) + ", Pass")
				break

		print ("\n\n")

	# Uno r3 clock 16MHz
	# recommended Revolutions per second is 45 (unloaded) so loaded can be approx 30.

	# Can add read user desired RPS from a text file if have time. Storing the value in a variable is giving me trouble.
	# Need to determine interval for the signals to the LEDs
	def signalInterval(self,width):
		if( width >= 250):
			fwidth = float(250)
		elif (width <= 0):
			fwidth = float(1)
		else:
			fwidth = float(width)
		clock = 16000000
		freq = float(clock/2)
		changeTime = float(8/freq)	# each byte requires changTime to change
		#ledArray = 48
		rps = 45                        # Figure out what unload RPS translates to this project loaded rps.

		# Attempt to store read value
		#path = 'C:\\Users\\Jonathan\\Documents\\LED_Globe\\DCmotor\\RPS.txt'

		#with open(path, 'r') as f:
		#	rps = f.read()
		#print("aaa")
		#print (str(rps))

		# RPS and led x width
		#records per second
		recPS = float(fwidth*rps)

		# ex, 48/8 = 6 bytes
		#bytes per second
		bps = float(recPS*6)

		#byte issued every X seconds
		issued = float(1/bps)

		#w > 925
		# faster than ex, changeTime x (48/6). 6x10^-6 seconds. If faster than lower bound, set to a time near it.
		lowerB = changeTime*(int(led)/2)

		defaultIssue = 20*(10. **-6)

		if(issued < lowerB):
			issued = lowerB
		elif fwidth < 1:
			issued = defaultIssue

		f = open("SignalTime.txt", "w")
		f.write(str(issued))
		f.close()

		#print issued
		return float(issued)


	def swap_black_white(self,img):



		black = create_color(0, 0, 0)
		white = create_color(255, 255, 255)

		for x, y, col in img:
			red, green, blue = col


			if red == 0 and green == 0 and blue == 0:


				set_color(img, x, y, white)


			elif red == 255 and green == 255 and blue == 255:


				set_color(img, x, y, black)
