#Stub
class motorStub:
    global output
    output = 0
        
    def stubPWM(self, duty):
        global output
        output = float(duty)
		
    def getStubOutput(self):
            
        return output

