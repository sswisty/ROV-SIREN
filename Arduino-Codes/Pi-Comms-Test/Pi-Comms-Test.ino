/* UNH ROV Python Communication Test Code




*/

#include <Wire.h>

// LED Pin to see if communication is functioning
int LEDPin = 13;
int OnOff, test;

// We will create fake data to send to the PI
int pitch;
int yaw;
int roll;

void setup() {
  // put your setup code here, to run once:

  pinMode(LEDPin, OUTPUT);
  
  Serial.begin(115200);
  Serial.setTimeout(100);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (Serial.available() > 0)
  {
    
    if (ReadValues() != -1){
    
      yaw = random(100);
      pitch = random(75);
      roll = random(82);
    
      SendValues();
    
    
      if (OnOff >= 5){
        digitalWrite(LEDPin, HIGH);
      }
      else{
        digitalWrite(LEDPin, LOW);
      }
    
      if (test >= 50){
        digitalWrite(11, HIGH);
      }
      else{
        digitalWrite(11, LOW);
      }
      
    }
    
    
  }
  

}
