#include <Servo.h>

// This file was used to control the froather
/* The El Potato does not have pulse width modulation
   so amperage was sent out to be recieved by the ardunio to 
   know when to lower and turn on the frother
*/

Servo servo;
int servo_analogVal = 0;
int enA = 9;
int in1 = 8;
int in2 = 7;

int froth = 2;



int val;
int val2;

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  Serial.begin(9600);
  pinMode(froth, OUTPUT);
  digitalWrite(in1, LOW);	// Turn off motors - Initial state
  digitalWrite(in2, LOW);
  servo.attach(11);


}

void loop() {
 // make();
  val2 = analogRead(5);
  val = analogRead(3);
  //Serial.println(val);
  servo.write(1500);
  Serial.println(val2);
  if (val > 100){
    spin();
    
  } 
  if (val2 > 100){
    make();
  }


}

void make(){
  analogWrite(enA, 255);
  digitalWrite(in1, LOW);	// Now change motor directions
  digitalWrite(in2, HIGH);
  delay(2500);

  digitalWrite(froth, HIGH);
  delay(5000);
  digitalWrite(froth, LOW);
  delay(500);

  digitalWrite(in1, HIGH);	 // Turn on motor A
  digitalWrite(in2, LOW); // Moves motor backward
  delay(3000);

  digitalWrite(in1, LOW);	// Turn off motor
  digitalWrite(in2, LOW);
 
}

void spin(){
  servo.write(1400);delay(20);
}
