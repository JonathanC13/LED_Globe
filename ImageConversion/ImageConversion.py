#Jonathan Chan
#Sysc3010
#Bit array generation for LEDs

import argparse

import os, sys
import PIL as pillow
import PIL.Image

from Cimpl import *
   
def thumbNail(img):
	
	# May add an option to not expand an image if h < 48.

	hori = calcHori(get_width(img), get_height(img))
	#if (hori == -1):
		#print ("Error convering image to thumbnail. See error above."
		
		#return img
	size = hori, 48

	infile = img
	
	for infile in sys.argv[1:]:
		file = os.path.splitext(infile)[0]
		file = file + "thumbnail.jpg"
		try:
			im = PIL.Image.open(infile)
			
			im.thumbnail(size, PIL.Image.LANCZOS)
			im.save(file, "JPEG")
		except IOError:
			print ("cannot create thumbnail for '%s'" % infile)
			
	return file

def calcHori(width, height):
	if(width <= 0 or height <= 0):
		print ("calcHori; 0 or negative parameter. Width: " + str(width) + " height: " + str(height))
		return -1
	else:
		ratio = int(height)/48
		hor = width/ratio

		#6 bytes in 6 micro seconds
		#1000000 changes in a second
		# set upper bound to squeeze image horizontal is larger
		#Arbitrary 250 , 20 micro second intervals
		if(hor >= 250):
			hor = 250
		elif (hor < 1):
			hor = -1

		return hor
			
def black_and_white(img):
	
	black = create_color(0, 0, 0)
	white = create_color(255, 255, 255)

	for x, y, col in img:
		red, green, blue = col

		brightness = (red + green + blue) / 2
		if brightness < 128:
			set_color(img, x, y, black)
		else:     
			set_color(img, x, y, white)
			
def bitArray(img):
	
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
												# 
			else:
				#print 0,
				bitMatrix[i][j] = 0
	return bitMatrix

	
	# add checks for type, values
	# pre condition: black and white image
def printBitArray(matrix):		
	numrows = len(matrix[0])
	numcols = len(matrix)	
	validBit = True
	
	for y in range(0,numrows):
		print (' ')
		for x in range(0, numcols):
			if (matrix[x][y] != 0 or matrix[x][y] != 1):
				validBit = False
				break
			print (matrix[x][y],)
		if(validBit == False):
			print ("Contains invalid value that is not a 0 or 1: " + matrix[x][y])
			break
	
# Uno r3 clock 16MHz
# recommneded Revolutions per second is 30
# Need to determine interval for the signals to the LEDs
def signalInterval(width):
	if( width >= 250):
		fwidth = float(250)
	else:
		fwidth = float(width)
	clock = 16000000
	freq = float(clock/2)
	changeTime = float(8/freq)	# each byte requires changTime to change
	ledArray = 48
	rps = 30
	
	#print changeTime
	
	# 30 RPS and 48xwidth
	#records per second
	recPS = float(fwidth*rps)
	
	# 48/8 = 6 bytes
	#bytes per second
	bps = float(recPS*6)
	
	#byte issued every X seconds
	issued = float(1/bps)
	
	#w > 925
	# faster than changeTime x (48/6). 6x10^-6 micro seconds.
	lowerB = 6*(10. **-6)
	defaultIssue = 20*(10. **-6)
	
	if(issued < lowerB):
		issued = lowerB
	elif fwidth < 1:
		issued = defaultIssue
		
	
	#print issued
	return issued
	
		
def swap_black_white(img):
    
	
	
    black = create_color(0, 0, 0)
    white = create_color(255, 255, 255)

    for x, y, col in img:
        red, green, blue = col

        
        if red == 0 and green == 0 and blue == 0:

            
            set_color(img, x, y, white)

        
        elif red == 255 and green == 255 and blue == 255:

            
            set_color(img, x, y, black) 

def commandInput():			
	#-- cmd line arg
	parser = argparse.ArgumentParser(description = 'Enter a filename, have the file in the same directory/folder.')
	parser.add_argument("-s", "--string", type=str, required=True,
								help='filename of the image to be used. Ex. python ImageConversion.py -s test.jpg')
	
	#parser.add_argument("-i", "--integer", type=int, default=0)
	
	parser.print_help()
	args = parser.parse_args()
	
	print("Opening:")
	print (args.string)
	#print args.integer
	userArg = args.string
	
	return userArg

#if isinstance(userArg, str):
#   print("true")

#---
#-- main

img = load_image(commandInput())	#load initial image

thumb = load_image(thumbNail(img)) #shrink image
#Need to check if converting t othumbnail was succesful or not
# Cimpl Compare images
# if true execute next		       
black_and_white(thumb)			#convert to black and white
save_as(thumb, "test_BW.jpg")	#save black and white conversion
show(thumb)

issueRate = signalInterval(thumb.get_width())		# this value sent with bitArray to Arduino 
												# so it will know the interval to issue the next pattern
bits = bitArray(thumb)					#convert black white to bit array
printBitArray(bits)
