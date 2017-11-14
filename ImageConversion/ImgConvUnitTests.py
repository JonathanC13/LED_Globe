from ImageConversion import ImageConversion
from Cimpl import *

import PIL as pillow
import PIL.Image

class ImgConvUnitTests:
	
	# Each test a new intance of ImageConversion is created to maintain the independence of each 
	# test case with no effect from a previous test.
	
	#----- thumbNail(img) test cases START -----
	
	# Load image with valid file format and non empty
        # Input: created image with w = 200, h = 200
        # Expected: get height and width should equal w = 48 and h = 48
	def test_thumbNail_normal(self):
	
		conversion = ImageConversion()
		
		color = create_color(100,150,80)
                created = create_image(200,200,color)
                save_as(created, "testCreated.jpg")

                loadCreated = load_image("testCreated.jpg")

                thumbfile = conversion.thumbNail(loadCreated)
                thumb = load_image(str(thumbfile))
                print(str(thumb.get_height()))
                if (thumb.get_width() <= 48 and thumb.get_height() <= 48):
                        print(str(thumb.getheight))
                        print ("Pass")
                else:
                        print("Fail")
                
	
	# Load image with invalid file format
        # Input: Test.pdf
        # Expected: NameError from Cimpl, when attempting to call get_width
	def test_thumbNail_invalidFormat(self):
	
		conversion = ImageConversion()
		actual = ""
		try:
                        actual = conversion.thumbNail(Test.pdf)         # IO error
                except NameError:
                        print ("Pass")
                except:
                        print ("Unexpected error ", sys.exc_info()[0])
                

	# Load image with empty file
        # Input: created file with w=0 and h = 0
        # Expected: ValueError from Cimpl, image of (0,0) invalid. thumbNail with empty image gives an unboundedLocalError
	def test_thumbNail_emptyImg(self):
		conversion = ImageConversion()

		black = create_color(0,0,0)
		try:
                        testIMG = create_image(0,0,black)          # create test image. Error will be from this function call.
                        
                except ValueError:
                        print ("Pass | "),
                except:
                        print ("--1--, Unexpected error ", sys.exc_info()[0])

                try:    
                        actual = conversion.thumbNail(testIMG)
                except UnboundLocalError:
                        print ("Pass")
                except:
                        print ("--2--, Unexpected error ", sys.exc_info()[0])
                        
	# ----- thumbNail(img) test cases END -----
	
	# ----- calcHori(width, height) test cases START -----
	
	# Test invalid image width with valid height
	# INPUT: w=-5, h=10
	# EXPECTED: 0
	def test_calcHori_invalidW(self):
		expected = 0
	
		conversion = ImageConversion()
		hor = conversion.calcHori(-5, 10)
		
		if(hor == expected):
			print ('Acutal Result: ' + str(hor) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(hor) + ' Status: FAIL')
	
	# Test normal case, valid width and height
	# INPUT: w=100, h=200
	# EXPECTED: 24
	def test_calcHori_normal(self):
		expected = 24
	
		conversion = ImageConversion()
		hor = conversion.calcHori(100, 200)
		
		if(hor == expected):
			print ('Acutal Result: ' + str(hor) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(hor) + ' Status: FAIL')
	
	# Test very large width where; width/(h/48) < 250
	# INPUT: w=3000, h=1000
	# EXPECTED: 144
	def test_calcHori_largeW(self):
		expected = 144
		
		conversion = ImageConversion()
		hor = conversion.calcHori(3000, 1000)
		
		if(hor == expected):
			print ('Acutal Result: ' + str(hor) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(hor) + ' Status: FAIL')
	
	# Test invalid height with valid height	
	# INPUT: w=48, h=0
	# EXPECTED: 0
	def test_calcHori_invalidH(self):
		expected = 0
		
		conversion = ImageConversion()
		hor = conversion.calcHori(48, 0)
		
		if(hor == expected):
			print ('Acutal Result: ' + str(hor) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(hor) + ' Status: FAIL')
	
	# Test very large height with valid Width, where width/(h/48) < 250
	# INPUT: w=1500, h=4000
	# EXPECTED: 18
	def test_calcHori_largeH(self):
		expected = 18
		
		conversion = ImageConversion()
		hor = conversion.calcHori(1500, 4000)
		
		if(hor == expected):
			print ('Acutal Result: ' + str(hor) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(hor) + ' Status: FAIL')
	
	# Test a width and height, where width/(h/48) >= 250
	# INPUT: w=17000, h=3000
	# EXPECTED: 250
	def test_calcHori_spc(self):
		expected = 250
		
		conversion = ImageConversion()
		hor = conversion.calcHori(17000, 3000)
		
		if(hor == expected):
			print ('Acutal Result: ' + str(hor) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(hor) + ' Status: FAIL')
	
	# ----- calcHori(width, height) test cases END -----
	
        # ----- black_and_while(img) test cases START -----

        # Load image with valid file format and non empty
        # Input: created image with r,g,b that will all be converted to black (0). Valid file format due to creation.
        # Expected: Shows all black image
	def test_black_and_white_normal(self):

                NEARblack = create_color(80,50,80)
                NEARblackIMG = create_image(100,100,NEARblack)          # create test image , purplish
                
		conversion = ImageConversion()
		conversion.black_and_white(NEARblackIMG)

		binary = True
		#show(NEARblackIMG)
                for j in range (0,100):
                        for i in range(0,100):
                                chk = get_color(NEARblackIMG, i, j)
                                if( chk != (0,0,0) ):
                                        binary = False
                                        print("Fail, not converted to black. co-ord: " + str(i) +", " + str(j))
                                        break
                        if (binary == False):
                                break
                print("Converted image contains only black, Pass")
		

        # Load image with invalid file format
        # Input: Test.pdf
        # Expected: NameError from Cimpl
	def test_black_and_white_invalidFormat(self):
		conversion = ImageConversion()
		try:
                        conversion.black_and_white(Test.pdf)
                except NameError:
                        print ("Pass")
                except:
                        print ("Unexpected error ", sys.exc_info()[0])
                
        # Load image with empty file
        # Input: created image file with w =0 and h = 0
        # Expected: ValueError from Cimpl, image of (0,0) invalid.
	def test_black_and_white_emptyImg(self):
		conversion = ImageConversion()

                black = create_color(0,0,0)
                try:
                        testIMG = create_image(0,0,black)          # create test image. Error will be from this function call.
                except ValueError:
                        print("Pass | "),
                except:
                        print ("--1--, Unexpected error ", sys.exc_info()[0])  

                try:
                        conversion.black_and_white(testIMG)
                except UnboundLocalError:
                        print ("Pass")
                except:
                        print ("--2--, Unexpected error ", sys.exc_info()[0])
                        
                
	# ----- black_and_while(img) test cases END -----

	# ----- bitArray(matrix) test cases START -----

	# Load file with valid file format and non-zero width and height
	# INPUT: Created full black image with valid extension and w = 100 and h = 100. Cimpl created image has valid format
	# Expected: return bit array of all 0s
	def test_bitArray_normal(self):

                black = create_color(0,0,0)
                blackIMG = create_image(100,100,black)          # create test image
                
		conversion = ImageConversion()  

		actual = conversion.bitArray(blackIMG)          # stores returned bit array

                r, c = 100, 100

		bitMatrix = [[0 for h in range(r)] for w in range(c)]
                allBlack = True
		
		for j in range(0,r):
			for i in range(0, c):
				if (actual[i][j] != 0):
                                        allBlack =False
                                        print("Fail, not 0 at: " + str(i) +", " + str(j))
                                        break
                        if(allBlack == False):
                                break

                print("Pass")

	# Load file with invalid image file format
	# INPUT: Test.pdf
	# Expected: NameError. I think the error is thrown from Cimpl due to get_height in the first line, no height of a .pdf
	def test_bitArray_invalidFormat(self):
                
		conversion = ImageConversion()

		try:
                        testArray = conversion.bitArray(Test.pdf)
                except NameError:
                        print ("Pass")
                except:
                        print ("Unexpected error ", sys.exc_info()[0])

        # Load file with invalid image file format
	# INPUT: Create image with 0 width and 0 height
	# Expected: ValueError. I think the error is thrown from Cimpl due to create_image here in this case, image of (0,0) invalid.
	def test_bitArray_emptyImg(self):

                black = create_color(0,0,0)

                try:
                        testIMG = create_image(0,0,black)          # create test image. Error will be from this function call.
                except ValueError:
                        print ("Pass | "),
                except:
                        print ("--1--, Unexpected error ", sys.exc_info()[0])
                
		conversion = ImageConversion()

                try:
        		testArray = conversion.bitArray(testIMG)        
                except UnboundLocalError:
                        print("Pass")
                except:
                        print ("--2--, Unexpected error ", sys.exc_info()[0])
                        
	# ----- bitArray(matrix) test cases END -----
	
	# ----- printBitArray(matrix) test cases START -----
	# Honestly this method could be simply print a 2d array.
	# But we'll have it only print 0s and 1s

        # Load empty matrix
	# INPUT: Input empty matrix
	# Expected: prints nothing
	def test_printBitArray_empty(self):
		testMatrix =[[],[]]
                
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

        # Input non empty matrix fill with 0s
	# INPUT: Input 2x2 matrix filled with 0s
	# Expected: prints the array correctly
	def test_printBitArray_valid0(self):
		testMatrix =[[0,0],[0,0]]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

        # Input non empty matrix fill with 1s
	# INPUT: Input 4x4 matrix filled with 1s
	# Expected: prints the array correctly
	def test_printBitArray_valid1(self):
		testMatrix =[[1,1,1,1],[1,1,1,1]]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

        # Input non empty matrix with number of rows > 49 filled with 0s
	# INPUT: Input 49x2 matrix filled with 0s
	# Expected: prints the array correctly
	def test_printBitArray_largeRow(self):
		r, c = 49, 2
		testMatrix = [[0 for h in range(r)] for w in range(c)]

                for j in range(0,r):
                	for i in range(0, c):
                                testMatrix[i][j] = 0
                                
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

        # Input non empty matrix with number of columns > 251 filled with 1s
	# INPUT: Input 10x251 matrix filled with 1s
	# Expected: prints the array correctly
	def test_printBitArray_largeCol(self):
		r, c = 10, 251
		testMatrix = [[0 for h in range(r)] for w in range(c)]

                for j in range(0,r):
                	for i in range(0, c):
                                testMatrix[i][j] = 0
		
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

        # Input non empty matrix with integers other than 0 or 1
	# INPUT: Input 2x2 matrix [2,2],[3,4]
	# Expected: prints an error message indicating non binary values in matrix
	def test_printBitArray_invalidVal(self):
		testMatrix =[[2,2],[3,4]]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

        # Input non empty matrix with non integers
	# INPUT: Input 1x2 matrix ['h','i'],[]
	# Expected: prints an error message indicating non binary values in matrix
	def test_printBitArray_nonInt(self):
		testMatrix =[['h','i'],[]]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)
		
	# ----- printBitArray(matrix) test cases END -----

	# ----- signalInterval(width) test cases START -----

        # Invalid width.
	# INPUT: w=-5
	# EXPECTED: 3.7x10^-3
	def test_signalInterval_invalidW(self):
		expected = 3.7*10**-3
		w = -5
		conversion = ImageConversion()
		fresult = float(conversion.signalInterval(w))
		issued = round(fresult,4)
		if(expected == issued):
		
			print ('Acutal Result: ' + str(issued) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(issued) + ' Status: FAIL')

	# Invalid width.
	# INPUT: w=50
	# EXPECTED: 7.41*10^-5	
	def test_signalInterval_normal(self):
		expected = 7.407*10**-5
	
		conversion = ImageConversion()
		w = 50
		fresult = float(conversion.signalInterval(w))
		issued = round(fresult,8)
		if(expected == issued):
		
			print ('Acutal Result: ' + str(issued) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(issued) + ' Status: FAIL')
			
	# Invalid width.
	# INPUT: w=300
	# EXPECTED: 1.48*10^-5	
	def test_signalInterval_GmaxW(self):
		expected = 1.48*10**-5

		w= 300
		conversion = ImageConversion()
		fresult = float(conversion.signalInterval(w))
		issued = round(fresult,7)
		if(expected == issued):
		
			print ('Acutal Result: ' + str(issued) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(issued) + ' Status: FAIL')

	# ----- signalInterval(width) test cases END -----

TestCases = ImgConvUnitTests()

#TEST CASES
#print("Test case 1: "),
#TestCases.test_thumbNail_normal()
#print("\n");

print("Test case 2: "),
TestCases.test_thumbNail_invalidFormat()
print("\n");


print("Test case 3: "),
TestCases.test_thumbNail_emptyImg()
print("\n");

print("Test case 4: "),
TestCases.test_calcHori_invalidW()
print("\n");

print("Test case 5: "),
TestCases.test_calcHori_normal()
print("\n");

print("Test case 6: "),
TestCases.test_calcHori_largeW()
print("\n");

print("Test case 7: "),
TestCases.test_calcHori_invalidH()
print("\n");

print("Test case 8: "),
TestCases.test_calcHori_largeH()
print("\n");

print("Test case 9: "),
TestCases.test_calcHori_spc()
print("\n");

print("Test case 10: "),
TestCases.test_black_and_white_normal()
print("\n");

print("Test case 11: "),
TestCases.test_black_and_white_invalidFormat()
print("\n");

print("Test case 12: "),
TestCases.test_black_and_white_emptyImg()
print("\n");

print("Test case 13: "),
TestCases.test_bitArray_normal()
print("\n");

print("Test case 14: "),
TestCases.test_bitArray_invalidFormat()
print("\n");

print("Test case 15: "),
TestCases.test_bitArray_emptyImg()
print("\n");

print("Test case 16: "),
TestCases.test_printBitArray_empty()
print("\n");

print("Test case 17: "),
TestCases.test_printBitArray_valid0()
print("\n");

print("Test case 18: "),
TestCases.test_printBitArray_valid1()
print("\n");

print("Test case 19: "),
TestCases.test_printBitArray_largeRow()
print("\n");

print("Test case 20: "),
TestCases.test_printBitArray_largeCol()
print("\n");

print("Test case 21: "),
TestCases.test_printBitArray_invalidVal()
print("\n");

print("Test case 22: "),
TestCases.test_printBitArray_nonInt()
print("\n");

print("Test case 23: "),
TestCases.test_signalInterval_invalidW()
print("\n");

print("Test case 24: "),
TestCases.test_signalInterval_normal()
print("\n");

print("Test case 25: "),
TestCases.test_signalInterval_GmaxW()
print("\n");



        


