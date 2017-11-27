#define Hall_PIN 2
const int ledPin = 10;

volatile int hallState = 0;

void setup() {
  // put your setup code here, to run once:

  // Setup all output pins, first LED is at top. 13 pins, pin 2 is for INT0
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

  // Interrupt pin
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), pin_ISR, FALLING);
}

void loop() {
  // put your main code here, to run repeatedly:

}

void pin_ISR() {
  
  hallState = digitalRead(HALL_PIN);
  digitalWrite(ledPin, hallState);
}

