from Cimpl import *
import argparse

from ImageConversion import ImageConversion

import os, sys
import PIL as pillow
import PIL.Image

# Receive image file from command line. Ex: python ImageConversion.py -s test.jpg
#def commandInput():			
#-- cmd line arg --
parser = argparse.ArgumentParser(description = 'Enter a filename, have the file in the same directory/folder.')
parser.add_argument("-s", "--string", type=str, required=True,
							help='filename of the image to be used. Ex. python ImageConversion.py -s test.jpg')

#parser.add_argument("-i", "--integer", type=int, default=0)

parser.print_help()
args = parser.parse_args()

print("Opening:")
print (args.string)

userArg = args.string

#return userArg
#---------

#---
#-- main --

Convert = ImageConversion()     # Create instance

img = load_image(userArg)	# load image that was specified in args
thumbFile = Convert.thumbNail(img) # If image height > 48, shrink image to a specified size, then save in a seperate image file. Ex: testthumbnail.jpg
thumb = load_image(thumbFile)   # load the shrunken image file 

if get_height(thumb) <= 48:
		       
        Convert.black_and_white(thumb)	#convert to black and white
        save_as(thumb, "test_BW.jpg")	#save black and white conversion to as an image file.
        #show(thumb)                     #just show image, close the pop up to conitnue program.

        issueRate = Convert.signalInterval(thumb.get_width())		# issue rate is the interval to send each column to the LEDs
                                                                                                                                       
        bits = Convert.bitArray(thumb)					#convert black white to bit array
        Convert.printBitArray(bits)                                     # just printing the bit array for visualization to compare to what is being presented on the globe.

        print("Column interval of " + str(issueRate) + " seconds. When motor is spinning 45 (unload) Revolutions per second.")
else:
        print("Adjusting size of image failed.")
