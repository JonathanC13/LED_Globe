const int Hall_PIN = 2;

boolean update = false;  // 
int delayTime = 1000;      // This value is from SignalTime.txt
const int x = 2;              // rows
const int y = 6;              // cols
byte pattern [x][y] = {
{1,0,0,0,0,0},
{1,0,0,0,0,0} 
}; // Fill 2d array with split values from LEDpattern.txt

int current_col = 0;

void setup() {
  // put your setup code here, to run once:
  
  // Setup all output pins, first LED is at top. 13 pins, pin 2 is for INT0
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  
  digitalWrite(0, LOW);
  digitalWrite(1, LOW);
 
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
  digitalWrite(12, LOW);
  digitalWrite(13, LOW);

   // Interrupt pin
  attachInterrupt(digitalPinToInterrupt(Hall_PIN), pin_ISR, FALLING);
}

void loop() {
  // put your main code here, to run repeatedly:
  /*if(update == true){
    update = false;
    if(current_col ++ >= (y)){  // reset column
      current_col = 0;
    }
  }*/
    next_column(current_col);     // output rows of that column
    current_col++;
    if(current_col >= y){
      current_col = 0;
    }
    delay(delayTime);
  
}

void next_column(int col){
 for (int row = 0; row < x; row++){
        if(pattern[row][col] == 1){
          digitalWrite(0, HIGH);
          
          digitalWrite(1, HIGH);
          
          digitalWrite(3, HIGH);
          
          digitalWrite(4, HIGH);
          
          digitalWrite(5, HIGH);
          
        
          digitalWrite(6, HIGH);
          
          digitalWrite(7, HIGH);
          
          digitalWrite(8, HIGH);
          
          digitalWrite(9, HIGH);
          
          digitalWrite(10, HIGH);
          
          digitalWrite(11, HIGH);
          
          digitalWrite(12, HIGH);
          
          digitalWrite(13, HIGH);
          
  

 
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
         }
         else {
          digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
          digitalWrite(0, LOW);
          digitalWrite(1, LOW);
          
          digitalWrite(3, LOW);
          digitalWrite(4, LOW);
          digitalWrite(5, LOW);
          digitalWrite(6, LOW);
          digitalWrite(7, LOW);
          digitalWrite(8, LOW);
          digitalWrite(9, LOW);
          digitalWrite(10, LOW);
          digitalWrite(11, LOW);
          digitalWrite(12, LOW);
          digitalWrite(13, LOW);
         }
      }
}

// Interrupt -----
/*
void configure_interrupts(void){
  cli();  // disable interrupts

  // configure hall sensor interrupt (pin 2)
  EICRA = _BV(ISC01); // Interrupt triggered by falling edge.
  EIMSK |= _BV(INT0); // enable hardware interrupt.

  sei();  // enable all interrupts
}

// Interrupt trigger for each rotation
ISR(INT0_vect){
  update = true;
}*/

void pin_ISR(){
  current_col = 0;

}
