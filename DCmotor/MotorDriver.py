from runDC import *
from MotorStub import *

class motorOracle:

        # ----- userRPStoDuty START -----

        def test_userRPStoDutyNeg(self):
                expected = 0
                
                DC = runDC()
                acutal = DC.userRPStoDuty(-50)

                if acutal == expected:
                        print("Pass")
                else:
                        print("Fail")
                
        def test_userRPStoDutyZero(self):
                expected = 0
                
                DC = runDC()
                acutal = DC.userRPStoDuty(0)

                if acutal == expected:
                        print("Pass")
                else:
                        print("Fail")
                
        def test_userRPStoDutyNorm(self):
                expected = 35.46
                
                DC = runDC()
                duty = DC.userRPStoDuty(50)
                rAct = round(duty,2)

                if rAct == expected:
                        print("Pass")
                else:
                        print("Fail")
                
        def test_userRPStoDutyMax(self):
                expected = 100
                
                DC = runDC()
                duty = DC.userRPStoDuty(141)

                if duty == expected:
                        print("Pass")
                else:
                        print("Fail")
                
        def test_userRPStoDutyLarge(self):
                expected = 100
                
                DC = runDC()
                duty = DC.userRPStoDuty(200)

                if duty == expected:
                        print("Pass")
                else:
                        print("Fail")
                
        def test_userRPStoDutyInvalid(self):
                
                DC = runDC()
                try:
                        duty = DC.userRPStoDuty(aaa)

                except NameError:
                        print ("Pass")
                except:
                        print("Fail")
                        print ("Unexpected error ", sys.exc_info()[0])


        # ----- userRPStoDuty END -----

         # ----- Stub Tests START -----

        def test_applyDutyNeg(self):
                a = -50
            
                mStub = motorStub()     #Stub

                DC = runDC()            # start motor program
                DC.applyDuty(a, mStub)

                actualDuty = mStub.getStubOutput()
               
                # Compares duty passed to expected based on RPS
                expectedDuty = 0.0
                if (expectedDuty == actualDuty):
                        #print "Duty from runDC, " + str(actualDuty) + ", is equal to calculated duty using RPS, "+ str(expectedDuty)
                        print "Pass"
                else:
                        print "Fail" 
                       # print "Duty from runDC, " + str(actualDuty) + ", is NOT equal to calculated duty using RPS, "+ str(expectedDuty)


        def test_applyDutyNegOne(self):
                a = -1
                mStub = motorStub()     #Stub

                DC = runDC()            # start motor program
                DC.applyDuty(a, mStub)

                actualDuty = mStub.getStubOutput()

                # Compares duty passed to expected based on RPS
                expectedDuty = 0.0
                if (expectedDuty == actualDuty):
                        #print "Duty from runDC, " + str(actualDuty) + ", is equal to calculated duty using RPS, "+ str(expectedDuty)
                        print "Pass"
                else:
                        print "Fail"
                        #print "Duty from runDC, " + str(actualDuty) + ", is NOT equal to calculated duty using RPS, "+ str(expectedDuty)

        def test_applyDutyZero(self):
                a = 0
                
                mStub = motorStub()     #Stub

                DC = runDC()            # start motor program
                DC.applyDuty(a, mStub)

                actualDuty = mStub.getStubOutput()

                # Compares duty passed to expected based on RPS
                expectedDuty = 0.0
                
                if (expectedDuty == actualDuty):
                    print "Pass"
                    #print "Duty from runDC, " + str(actualDuty) + ", is equal to calculated duty using RPS, "+ str(expectedDuty)
                else:
                    print "Fail"
                    #print "Duty from runDC, " + str(actualDuty) + ", is NOT equal to calculated duty using RPS, "+ str(expectedDuty)

        def test_applyDutyNorm(self):
                a = 75
            
                mStub = motorStub()     #Stub

                DC = runDC()            # start motor program
                DC.applyDuty(a, mStub)

                actualDuty = mStub.getStubOutput()

                rAct = round(actualDuty,2)
                
                # Compares duty passed to expected based on RPS
                expectedDuty = 53.19
                
                if (expectedDuty == rAct):
                        print "Pass"
                        #print "Duty from runDC, " + str(actualDuty) + ", is equal to calculated duty using RPS, "+ str(expectedDuty)
                else:
                        print "Fail"
                        #print "Duty from runDC, " + str(actualDuty) + ", is NOT equal to calculated duty using RPS, "+ str(expectedDuty)

        def test_applyDutyMax(self):
                a = 141
            
                mStub = motorStub()     #Stub

                DC = runDC()            # start motor program
                DC.applyDuty(a, mStub)

                actualDuty = mStub.getStubOutput()

                # Compares duty passed to expected based on RPS
                expectedDuty = 100.0
                if (expectedDuty == actualDuty):
                        print("Pass")
                        #print "Duty from runDC, " + str(actualDuty) + ", is equal to calculated duty using RPS, "+ str(expectedDuty)
                else:
                        print "Fail"
                        #print "Duty from runDC, " + str(actualDuty) + ", is NOT equal to calculated duty using RPS, "+ str(expectedDuty)

        def test_applyDutyLarge(self):
                a = 200
                mStub = motorStub()     #Stub

                DC = runDC()            # start motor program
                DC.applyDuty(a, mStub)

                actualDuty = mStub.getStubOutput()

                # Compares duty passed to expected based on RPS
                expectedDuty = 100.0
                if (expectedDuty == actualDuty):
                        print "Pass"
                        #print "Duty from runDC, " + str(actualDuty) + ", is equal to calculated duty using RPS, "+ str(expectedDuty)
                else:
                        print "Fail"
                        #print "Duty from runDC, " + str(actualDuty) + ", is NOT equal to calculated duty using RPS, "+ str(expectedDuty)

        # ----- Stub Tests END -----


TestCases = motorOracle()

#TEST CASES
# userRPStoDuty tests
print("Test case 1: "),
TestCases.test_userRPStoDutyNeg()
print("\n");

print("Test case 2: "),
TestCases.test_userRPStoDutyZero()
print("\n");

print("Test case 3: "),
TestCases.test_userRPStoDutyNorm()
print("\n");

print("Test case 4: "),
TestCases.test_userRPStoDutyMax()
print("\n");

print("Test case 5: "),
TestCases.test_userRPStoDutyLarge()
print("\n");

print("Test case 6: "),
TestCases.test_userRPStoDutyInvalid()
print("\n");

# stub tests
print("Test case 7: "),
TestCases.test_applyDutyNeg()
print("\n");

print("Test case 8: "),
TestCases.test_applyDutyNegOne()
print("\n");

print("Test case 9: "),
TestCases.test_applyDutyZero()
print("\n");

print("Test case 10: "),
TestCases.test_applyDutyNorm()
print("\n");

print("Test case 11: "),
TestCases.test_applyDutyMax()
print("\n");

print("Test case 12: "),
TestCases.test_applyDutyLarge()
print("\n");
