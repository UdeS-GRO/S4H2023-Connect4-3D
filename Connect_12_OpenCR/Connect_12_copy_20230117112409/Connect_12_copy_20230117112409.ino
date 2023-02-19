#include <Dynamixel2Arduino.h>
#include <DynamixelSDK.h>
//#include <DynamixelWizard.h>
#include <HardwareSerial.h>
#include <Arduino.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// For OpenCR, there is a DXL Power Enable pin, so you must initialize and control it.
// Reference link : https://github.com/ROBOTIS-GIT/OpenCR/blob/master/arduino/opencr_arduino/opencr/libraries/DynamixelSDK/src/dynamixel_sdk/port_handler_arduino.cpp#L78
//#if defined(ARDUINO_OpenCR)
  #define motorShoulder_SERIAL Serial3
  #define Serial2 Serial2
  #define DEBUG_SERIAL Serial
//#endif

//#define DEBUG_SERIAL  Serial

#define BDPIN_PUSH_SW_1         34
#define BDPIN_PUSH_SW_2         35
#define ENCA                    2
#define ENCB                    4

const int motorShoulder_DIR_PIN = 84; // OpenCR Board's DIR PIN.
//const int motorElbow_DIR_PIN = 85; // OpenCR Board's DIR PIN.
//int myPins[] = {2, 4, 8, 3, 6};
int MotorsID[] = {1, 3};
uint8_t motorShoulder_ID = MotorsID[0];
uint8_t motorElbow_ID = MotorsID[1];
const float DXL_PROTOCOL_VERSION = 2.0;



Dynamixel2Arduino ServoMotor(motorShoulder_SERIAL, motorShoulder_DIR_PIN);

//This namespace is required to use Control table item names
using namespace ControlTableItem;

int max = 180;
int min = 0;
String msg = "";
String msg1 = "";
String msg2 = "";
String motorAngleShoulder = "";
int motorAngleShoulderInt = 0;
String motorAngleElbow = "";
int motorAngleElbowInt = 0;
String motorAngle = "";

int Count_pulses = 0;

int pingMotors(int nbMot);
void getMsg();
void readSerialPort();
void sendData(int msg2send);

void setup() {
  
  DEBUG_SERIAL.begin(9600);
  //DEBUG_SERIAL.println("Started");
  while(!DEBUG_SERIAL);

  //attachInterrupt(digitalPinToInterrupt(ENCA), void EncoderA(), RISING);
  //attachInterrupt(digitalPinToInterrupt(ENCB), void EncoderB(), RISING);

  pinMode(BDPIN_PUSH_SW_1, INPUT);
  pinMode(BDPIN_PUSH_SW_2, INPUT);

  //psetIDMotors(2);

  //motorShoulder Setup
  ServoMotor.begin(57600);
  ServoMotor.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  //ServoMotor.ping(motorShoulder_ID);

  // Turn off torque when configuring items in EEPROM area
  ServoMotor.torqueOff(motorShoulder_ID);
  ServoMotor.setOperatingMode(motorShoulder_ID, OP_POSITION);
  ServoMotor.torqueOn(motorShoulder_ID);
  ServoMotor.torqueOff(motorElbow_ID);
  ServoMotor.setOperatingMode(motorElbow_ID, OP_POSITION);
  ServoMotor.torqueOn(motorElbow_ID);

  // Limit the maximum velocity in Position Control Mode. Use 0 for Max speed
  ServoMotor.writeControlTableItem(PROFILE_VELOCITY, motorShoulder_ID, 50);
  ServoMotor.writeControlTableItem(PROFILE_VELOCITY, motorElbow_ID, 50);
  //ServoMotor.
  
}

void loop() {
  readSerialPort();
  if(Serial.available() < 1)
    sendData();

  ServoMotor.setGoalPosition(motorShoulder_ID, motorAngleShoulderInt);
  while(ServoMotor.getPresentPosition(motorShoulder_ID) == motorAngleShoulderInt){
    delay(1);
  }
  ServoMotor.setGoalPosition(motorElbow_ID, motorAngleElbowInt);
  while(ServoMotor.getPresentPosition(motorElbow_ID) == motorAngleElbowInt){
    delay(1);
  }
}

void psetIDMotors(int nbMot)
{
  //DEBUG_SERIAL.println("In process");
  int ID = 0;
  int nb = 0;
  //while(nb < nbMot && ID < 50)
  //{
      /*if(ServoMotor.ping(ID) == TRUE)
      {
        MotorsID[nb] = ID;
        DEBUG_SERIAL.print("nb: ");
        DEBUG_SERIAL.println(nb);
        nb += 1;
      }
      ID += 1;
      DEBUG_SERIAL.print("ID: ");
      DEBUG_SERIAL.println(ID);
      delay(500);
      */

      for(int i = 0; i < 255; i++){
        if(ServoMotor.ping(i) == TRUE){
          MotorsID[nb] = i;
          nb += 1;
          DEBUG_SERIAL.print("nB: ");
          DEBUG_SERIAL.println(nb);
        }
        DEBUG_SERIAL.print("ID: ");
        DEBUG_SERIAL.println(i);
      }
  //}
  for(int i = 0; i < nbMot; i++){
    DEBUG_SERIAL.print("old id: ");
    DEBUG_SERIAL.print(MotorsID[i]);
    DEBUG_SERIAL.print(" - new id: ");
    ServoMotor.setID(MotorsID[i], i);
    DEBUG_SERIAL.println(i);
  }

  return;
}

void readSerialPort() {
  
 	if (Serial.available()) {
 			//delay(2);
      
      while (Serial.available() == 0 );
 			while (Serial.available() > 0){
        motorAngle = Serial.readString();
      }
 			Serial.flush();
 	}

  int firstIndexDelimiter = motorAngle.indexOf('|');
  motorAngleShoulder = motorAngle.substring(0, firstIndexDelimiter);
  motorAngleShoulderInt = motorAngleShoulder.toInt();

  int lastIndexDelimiter = motorAngle.lastIndexOf('|');
  motorAngleElbow = motorAngle.substring(firstIndexDelimiter+1, lastIndexDelimiter);
  motorAngleElbowInt = motorAngleElbow.toInt();

  return;
}

void sendData(){
  /*msg = "";
  msg1 = "";
  msg2 = "";*/

  while(Serial.available()<1){
    float SendShoulderPosFloat = ServoMotor.getPresentPosition(motorShoulder_ID);
    int SendShoulderPos = round(SendShoulderPosFloat);
    String SendShoulderPosStr = String(SendShoulderPos);

    float SendElbowPosFloat = ServoMotor.getPresentPosition(motorElbow_ID);
    int SendElbowPos = round(SendElbowPosFloat);
    String SendElbowPosStr = String(SendElbowPos);
    
    if(SendShoulderPosStr.length() == 1){
      msg1 = "000" + SendShoulderPosStr;
    }
    if(SendShoulderPosStr.length() == 2){
      msg1 = "00" + SendShoulderPosStr;
    }
    if(SendShoulderPosStr.length() == 3){
      msg1 = "0" + SendShoulderPosStr;
    }
    else{
      msg1 = SendShoulderPosStr;
    }

    if(SendElbowPosStr.length() == 1){
      msg2 = "000" + SendElbowPosStr;
    }
    if(SendElbowPosStr.length() == 2){
      msg2 = "00" + SendElbowPosStr;
    }
    if(SendElbowPosStr.length() == 3){
      msg2 = "0" + SendElbowPosStr;
    }
    else{
      msg2 = SendElbowPosStr;
    }

    msg = msg1+msg2;
    //msg = "2000";
    Serial.print(msg);
  }

  return;
}

void EncoderA()
{
  int aRead = digitalRead(ENCA);
  if(aRead > 0){
    Count_pulses++;
  }
  else{
    Count_pulses--;
  }
  return;
}

void EncoderB()
{
  int bRead = digitalRead(ENCB);
  if(bRead > 0){
    Count_pulses--;
  }
  else{
    Count_pulses++;
  }
  return;
}

