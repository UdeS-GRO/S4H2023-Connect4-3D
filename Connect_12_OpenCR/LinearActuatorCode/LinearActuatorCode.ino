#include <Arduino.h>

//fonctions
void ElectromagnetOn();
void ElectromagnetOff();
void DC_Motor_UP();
void DC_Motor_DOWN();
void DC_Motor_STOP();

#define MAGNET_PIN 9
#define DIR_PIN 4
#define PWM_PIN 5
#define LMT_PIN 6
#define Encoder_output_A 2 // pin2 of the Arduino
#define Encoder_output_B 3 // pin 3 of the Arduino

int Count_pulses = 0;

void setup() {
  //Setup electromagnet
  Serial.begin(9600);
  pinMode(MAGNET_PIN, OUTPUT);  
  digitalWrite(MAGNET_PIN, LOW);

  //Setup Cytron motor driver
  pinMode(DIR_PIN, OUTPUT);
  pinMode(PWM_PIN, OUTPUT);
  pinMode(Encoder_output_A,INPUT); // sets the Encoder_output_A pin as the input
  pinMode(Encoder_output_B,INPUT); // sets the Encoder_output_B pin as the input
  pinMode(LMT_PIN, INPUT_PULLUP); // sets the Limit switch pin as input
  attachInterrupt(digitalPinToInterrupt(Encoder_output_A),DC_Motor_Encoder,RISING);
  Serial.print("Debut du code");
}

void loop() {

  DC_Motor_DOWN();
  while(Count_pulses < 1200)
  {
    Serial.println("Descend");
    Serial.println(Count_pulses);
  }
  DC_Motor_STOP();

  ElectromagnetOn();
  delay(1000);

  DC_Motor_UP();
  while(digitalRead(LMT_PIN) == HIGH)
  {
    Serial.println("Remonte");
    Serial.println(Count_pulses);
  }
  DC_Motor_STOP();
  ElectromagnetOff();
  Serial.println("END");
  Count_pulses = 0;
  while(1){}  
}


void ElectromagnetOn(){
  digitalWrite(MAGNET_PIN, HIGH);
}

void ElectromagnetOff(){
  digitalWrite(MAGNET_PIN, LOW);
}

void DC_Motor_Encoder(){
  int b = digitalRead(Encoder_output_B);
  if(b > 0){
    Count_pulses++;
  }
  else{
    Count_pulses--;
  }
}

void DC_Motor_UP(){
  digitalWrite(DIR_PIN, LOW);
  analogWrite(PWM_PIN, 150);
}

void DC_Motor_DOWN(){
  digitalWrite(DIR_PIN, HIGH);
  analogWrite(PWM_PIN, 255);
}

void DC_Motor_STOP(){
  analogWrite(PWM_PIN, 0);
}
