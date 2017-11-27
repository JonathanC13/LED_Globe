#define Hall_PIN 2
const int ledPinR = 10;
const int ledPinG = 11;

volatile int hallState = 0;

void setup() {
  // put your setup code here, to run once:

  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);


  // Interrupt pin
  attachInterrupt(digitalPinToInterrupt(2), pin_ISR, FALLING);
}

void loop() {
  // put your main code here, to run repeatedly:

}

void pin_ISR() {
  
  hallState = digitalRead(2);
  digitalWrite(ledPinR, HIGH);
  digitalWrite(ledPinG, HIGH);
  delay(3000);
  digitalWrite(ledPinR, LOW);
  digitalWrite(ledPinG, LOW);
}

