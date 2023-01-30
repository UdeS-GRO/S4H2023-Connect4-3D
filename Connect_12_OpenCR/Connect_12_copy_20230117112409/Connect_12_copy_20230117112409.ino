#include <Dynamixel2Arduino.h>
#include <HardwareSerial.h>
#include <Arduino.h>
#include <stdlib.h>

// For OpenCR, there is a DXL Power Enable pin, so you must initialize and control it.
// Reference link : https://github.com/ROBOTIS-GIT/OpenCR/blob/master/arduino/opencr_arduino/opencr/libraries/DynamixelSDK/src/dynamixel_sdk/port_handler_arduino.cpp#L78
#if defined(ARDUINO_OpenCR)
  #define motorShoulder_SERIAL   Serial3
  #define Serial2   Serial2
  #define DEBUG_SERIAL Serial
#endif

#define BDPIN_PUSH_SW_1         34
#define BDPIN_PUSH_SW_2         35

const int motorShoulder_DIR_PIN = 84; // OpenCR Board's DIR PIN.
//const int motorElbow_DIR_PIN = 85; // OpenCR Board's DIR PIN.
const uint8_t motorShoulder_ID = 21;
const uint8_t motorElbow_ID = 23;
const float DXL_PROTOCOL_VERSION = 2.0;

char PYTHON_SERIAL;

//Dynamixel2Arduino motorShoulder(motorShoulder_SERIAL, motorShoulder_DIR_PIN);
//Dynamixel2Arduino motorElbow(motorElbow_SERIAL, motorElbow_DIR_PIN);
Dynamixel2Arduino ServoMotor(motorShoulder_SERIAL, motorShoulder_DIR_PIN);

//This namespace is required to use Control table item names
using namespace ControlTableItem;

int max = 180;
int min = 0;
int ShoulderGoal = 0;
int ElbowGoal = 0;

//int pingMotors(int nbMot);

void setup() {
  
  DEBUG_SERIAL.begin(115200);
  DEBUG_SERIAL.println("Started");
  while(!DEBUG_SERIAL);

  Serial2.begin(9600);

  pinMode(BDPIN_PUSH_SW_1, INPUT);
  pinMode(BDPIN_PUSH_SW_2, INPUT);

  pingMotors(1);

  /*//motorShoulder Setup
  motorShoulder.begin(57600);
  motorShoulder.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  motorShoulder.ping(motorShoulder_ID);

  // Turn off torque when configuring items in EEPROM area
  motorShoulder.torqueOff(motorShoulder_ID);
  motorShoulder.setOperatingMode(motorShoulder_ID, OP_POSITION);
  motorShoulder.torqueOn(motorShoulder_ID);

  // Limit the maximum velocity in Position Control Mode. Use 0 for Max speed
  motorShoulder.writeControlTableItem(PROFILE_VELOCITY, motorShoulder_ID, 100);
*/
 /* //motorElbow Setup
  motorElbow.begin(57600);
  motorElbow.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  motorElbow.ping(motorElbow_ID);

  // Turn off torque when configuring items in EEPROM area
  motorElbow.torqueOff(motorElbow_ID);
  motorElbow.setOperatingMode(motorElbow_ID, OP_POSITION);
  motorElbow.torqueOn(motorElbow_ID);

  // Limit the maximum velocity in Position Control Mode. Use 0 for Max speed
  motorElbow.writeControlTableItem(PROFILE_VELOCITY, motorElbow_ID, 50);*/

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
}

void loop() {

  if(Serial2.available() > 0)
  {
      PYTHON_SERIAL = Serial2.read();
      Serial2.println( PYTHON_SERIAL);
      if (PYTHON_SERIAL== 500)
      {
        Serial2.println("S recu");
      }
  }

  //Serial2.write("MSG Received!");

  ShoulderGoal = PYTHON_SERIAL;

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
  ServoMotor.setGoalPosition(motorShoulder_ID, ShoulderGoal);
  ServoMotor.setGoalPosition(motorElbow_ID, ElbowGoal);
  
}

int pingMotors(int nbMot)
{
  int ID = 1;
  int nb = 0;
  int ID_Motors[nbMot];
  while(nb < nbMot)
  {
      if(ServoMotor.ping(ID))
      {
        ID_Motors[nb] = ID;
        nb += 1;
        //Serial2.print("nbMot: ");
        //Serial2.println(nb);
      }
      //Serial2.print("ID: ");
      //Serial2.println(ID);
      ID += 1;
  }
  Serial2.println(ID_Motors[1]);
  return ID_Motors[1];
}
