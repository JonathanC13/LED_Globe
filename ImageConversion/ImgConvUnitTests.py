import ImageConversion import ImageConversion

class ImgConvUnitTests:
	
	# Each test a new intance of ImageConversion is created to maintain the independence of each 
	# test case with no effect from a previous test.
	
	#----- thumbNail(img) test cases START -----
	
	#
	def test_thumbNail_normal():
	
		conversion = ImageConversion()
	
	
	def test_thumbNail_invaldFormat():
	
		conversion = ImageConversion()
	
	def test_thumbNail_emptyImg():
		conversion = ImageConversion()
	
	# ----- thumbNail(img) test cases END -----
	
	# ----- calcHori(width, height) test cases START -----
	
	# Test invalid image width with valid height
	# INPUT: w=-5, h=10
	# EXPECTED: 
	def test_calcHori_invalidW():
		expected = -1
	
		conversion = ImageConversion()
		acutal = conversion.calcHori(-5, 10)
		
		if(actual == expected):
			print ('Acutal Result: ' + str(actual) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(actual) + ' Status: FAIL')
	
	# Test normal case, valid width and height
	# INPUT: w=100, h=200
	# EXPECTED: 
	def test_calcHori_normal():
		expected = 24
	
		conversion = ImageConversion():
		acutal = conversion.calcHori(100, 200)
		
		if(actual == expected):
			print ('Acutal Result: ' + str(actual) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(actual) + ' Status: FAIL')
	
	# Test very large width where; width/(h/48) < 250
	# INPUT: w=3000, h=1000
	# EXPECTED: 
	def test_calcHori_largeW():
		expected = 144
		
		conversion = ImageConversion()
		acutal = conversion.calcHori(3000, 1000)
		
		if(actual == expected):
			print ('Acutal Result: ' + str(actual) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(actual) + ' Status: FAIL')
	
	# Test invalid height with valid height	
	# INPUT: w=48, h=0
	# EXPECTED: 
	def test_calcHori_invalidH():
		expected = -1
		
		conversion = ImageConversion()
		acutal = conversion.calcHori(48, 0)
		
		if(actual == expected):
			print ('Acutal Result: ' + str(actual) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(actual) + ' Status: FAIL')
	
	# Test very large height with valid Width, where width/(h/48) < 250
	# INPUT: w=1500, h=4000
	# EXPECTED: 
	def test_calcHori_largeH():
		expected = 18
		
		conversion = ImageConversion()
		acutal = conversion.calcHori(1500, 4000)
		
		if(actual == expected):
			print ('Acutal Result: ' + str(actual) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(actual) + ' Status: FAIL')
	
	# Test a width and height, where width/(h/48) >= 250
	# INPUT: w=17000, h=3000
	# EXPECTED: 
	def test_calcHori_spc():
		expected = 250
		
		conversion = ImageConversion()
		acutal = conversion.calcHori(17000, 3000)
		
		if(actual == expected):
			print ('Acutal Result: ' + str(actual) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(actual) + ' Status: FAIL')
	
	# ----- calcHori(width, height) test cases END -----
	
	
	def test_black_and_white_normal():
		conversion = ImageConversion()

	def test_black_and_white_invalidFormat():
		conversion = ImageConversion()

	def test_black_and_white_emptyImg():
		conversion = ImageConversion()

	# ----- bitArray(matrix) test cases START -----
		
	def test_bitArray_normal():		
		conversion = ImageConversion()
		
		
		
	def test_bitArray_invalidFormat():
		conversion = ImageConversion()

	def test_bitArray_emptyImg():
		conversion = ImageConversion()
		
	# ----- bitArray(matrix) test cases END -----
	
	# ----- printBitArray(matrix) test cases START -----

	def test_printBitArray_empty():
		testMatrix =[[],[]]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

	def test_printBitArray_valid0():
		testMatrix =[[0,0],[0,0]]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

	def test_printBitArray_valid1():
		testMatrix =[[1,1,1,1],[1,1,1,1]]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

	def test_printBitArray_largeRow():
		r, c = 49, 2
		testMatrix = [[0 for h in range(r)] for w in range(c)]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

	def test_printBitArray_largeCol():
		r, c = 10, 251
		testMatrix = [[0 for h in range(r)] for w in range(c)]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

	def test_printBitArray_invalidVal():
		testMatrix =[[2,2],[3,4]]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)

	def test_printBitArray_empty():
		testMatrix =[['h','i'],[]]
		conversion = ImageConversion()
		conversion.printBitArray(testMatrix)
		
	# ----- printBitArray(matrix) test cases END -----

	def test_signalInterval_invalidW():
		expected = 3.7*10**-3
		
		conversion = ImageConversion()
		fresult = float(conversion.signalInterval(-5))
		actual = round(fresult,4)
		if(expected == actual):
		
			print ('Acutal Result: ' + str(actual) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(actual) + ' Status: FAIL')
		
	def test_signalInterval_normal():
		expected = 7.74*10**-5
	
		conversion = ImageConversion()
		fresult = float(conversion.signalInterval(-5))
		actual = round(fresult,7)
		if(expected == actual):
		
			print ('Acutal Result: ' + str(actual) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(actual) + ' Status: FAIL')
	
	def test_signalInterval_GmaxW():
		expected = 1.48*10**-5
		
		conversion = ImageConversion()
		actual = round(fresult,7)
		if(expected == actual):
		
			print ('Acutal Result: ' + str(actual) + ' Status: PASS')
		else: 
			print ('Acutal Result: ' + str(actual) + ' Status: FAIL')

