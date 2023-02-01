#include <Dynamixel2Arduino.h>
#include <HardwareSerial.h>
#include <Arduino.h>
#include <stdlib.h>

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
int ShoulderGoal = 0;
int ElbowGoal = 0;

String msg;

int pingMotors(int nbMot);
void getMsg();
String readSerialPort();
void sendData(int msg2send);

void setup() {
  
  DEBUG_SERIAL.begin(9600);
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
  //ServoMotor.writeControlTableItem(PROFILE_VELOCITY, motorElbow_ID, 50);

  
}

void loop() {

  /*if(DEBUG_SERIAL.available() > 0)
  {
      DEBUG_SERIAL.println("ok");
  }*/

  String AngleStr = readSerialPort();
  int Angle2int = AngleStr.toInt();

  //char msg = DEBUG_SERIAL.Read();
  //Serial.println(msg);

  //Serial2.write("MSG Received!");

  /*
  //For Motor1
  if(digitalRead(BDPIN_PUSH_SW_1))
  {
    ElbowGoal -= 25;
    if(ElbowGoal <= 0)
      ElbowGoal = 0;
    ShoulderGoal += 25;
    if(ShoulderGoal >= 4095)
      ShoulderGoal = 4095;
  }
  else
  {
    ShoulderGoal -= 20;
    if(ShoulderGoal <= 0)
      ShoulderGoal = 0;
  }
  */
  /*
  //For Motor 2
  if(digitalRead(BDPIN_PUSH_SW_2))
  {
    ElbowGoal += 25;
    if(ElbowGoal >= 4095)
      ElbowGoal = 4095;
  }
  else
  {
    ElbowGoal -= 20;
    if(ElbowGoal <= 0)
      ElbowGoal = 0;
  }
  */

  ServoMotor.setGoalPosition(motorShoulder_ID, Angle2int);
  //ServoMotor.setGoalPosition(motorElbow_ID, ElbowGoal);
  //while(ServoMotor.getPresentPosition(motorShoulder_ID) >= Angle2int);
  delay(500);
  sendData(Angle2int);
  
}

void psetIDMotors(int nbMot)
{
  DEBUG_SERIAL.println("In process");
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
    DEBUG_SERIAL.print("old id: ");
    DEBUG_SERIAL.print(MotorsID[i]);
    DEBUG_SERIAL.print(" - new id: ");
    ServoMotor.setID(MotorsID[i], i);
    DEBUG_SERIAL.println(i);
  }

  return;
}

String readSerialPort() {
 	msg = "";
 	if (Serial.available()) {
 			//delay(2);
 			while (Serial.available() > 0) {
 					msg += (char)Serial.read();
 			}
 			Serial.flush();
 	}
  return msg;
}

void sendData(int msg2send) {
 	//write data
 	//Serial.print(nom);
 	//Serial.print(" received : ");
 	//Serial.print(msg);
  //Serial.print(" + ");
  Serial.println(String(msg2send));
  //Serial.println(600);
  return;
}
