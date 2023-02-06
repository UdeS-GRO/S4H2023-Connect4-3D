#include <Dynamixel2Arduino.h>
#include <HardwareSerial.h>
#include <Arduino.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// For OpenCR, there is a DXL Power Enable pin, so you must initialize and control it.
// Reference link : https://github.com/ROBOTIS-GIT/OpenCR/blob/master/arduino/opencr_arduino/opencr/libraries/DynamixelSDK/src/dynamixel_sdk/port_handler_arduino.cpp#L78
#if defined(ARDUINO_OpenCR)
  #define motorShoulder_SERIAL   Serial3
  //#define Serial2   Serial2
  #define DEBUG_SERIAL Serial
#endif

#define BDPIN_PUSH_SW_1         34
#define BDPIN_PUSH_SW_2         35

const int motorShoulder_DIR_PIN = 84; // OpenCR Board's DIR PIN.
//const int motorElbow_DIR_PIN = 85; // OpenCR Board's DIR PIN.
//int myPins[] = {2, 4, 8, 3, 6};
int MotorsID[] = {0, 0};
uint8_t motorShoulder_ID;
uint8_t motorElbow_ID;
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

int pingMotors(int nbMot);
void getMsg();
void readSerialPort();
void sendData(int msg2send);

void setup() {
  
  DEBUG_SERIAL.begin(115200);
  //DEBUG_SERIAL.println("Started");
  while(!DEBUG_SERIAL);

  pinMode(BDPIN_PUSH_SW_1, INPUT);
  pinMode(BDPIN_PUSH_SW_2, INPUT);

  psetIDMotors(1);
  motorShoulder_ID = MotorsID[0];
  motorElbow_ID = MotorsID[1];

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
  ServoMotor.writeControlTableItem(PROFILE_VELOCITY, motorShoulder_ID, 100);
  ServoMotor.writeControlTableItem(PROFILE_VELOCITY, motorElbow_ID, 100);

  
}

void loop() {
  readSerialPort();
  sendData();


  ServoMotor.setGoalPosition(motorShoulder_ID, motorAngleShoulderInt);
  
  while(ServoMotor.getPresentPosition(motorShoulder_ID) == motorAngleShoulderInt);
}

void psetIDMotors(int nbMot)
{
  //DEBUG_SERIAL.println("In process");
  int ID = 0;
  int nb = 0;
  while(nb < nbMot && ID < 50)
  {
      if(ServoMotor.ping(ID))
      {
        MotorsID[nb] = ID;
        nb += 1;
      }
      ID += 1;
  }
  for(int i = 0; i < nb; i++){
    //DEBUG_SERIAL.print("old id: ");
    //DEBUG_SERIAL.print(MotorsID[i]);
    //DEBUG_SERIAL.print(" - new id: ");
    ServoMotor.setID(MotorsID[i], i);
    //DEBUG_SERIAL.println(i);
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

  int SendShoulderPos = abs(ServoMotor.getPresentPosition(motorShoulder_ID));
  String SendShoulderPosStr = String(SendShoulderPos);

  int SendElbowPos = abs(ServoMotor.getPresentPosition(motorElbow_ID));
  String SendElbowPosStr = String(SendElbowPos);
  
  if(SendShoulderPosStr.length() == 3){
    msg1 = '0' + SendShoulderPosStr;
  }
  else{
    msg1 = SendShoulderPosStr;
  }

  if(SendElbowPosStr.length() == 3){
    msg2 = '0' + SendElbowPosStr;
  }
  else{
    msg2 = SendElbowPosStr;
  }

  msg = msg1+msg2;

  Serial.print(msg);

  return;
}
