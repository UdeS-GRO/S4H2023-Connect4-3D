#include <Dynamixel2Arduino.h>

// For OpenCR, there is a DXL Power Enable pin, so you must initialize and control it.
// Reference link : https://github.com/ROBOTIS-GIT/OpenCR/blob/master/arduino/opencr_arduino/opencr/libraries/DynamixelSDK/src/dynamixel_sdk/port_handler_arduino.cpp#L78
#if defined(ARDUINO_OpenCR)
  #define motorShoulder_SERIAL   Serial3
  #define motorElbow_SERIAL   Serial2
  #define DEBUG_SERIAL Serial
#endif

#define BDPIN_PUSH_SW_1         34
#define BDPIN_PUSH_SW_2         35

const int motorShoulder_DIR_PIN = 84; // OpenCR Board's DIR PIN.
const int motorElbow_DIR_PIN = 85; // OpenCR Board's DIR PIN.
const uint8_t motorShoulder_ID = 23;
const uint8_t motorElbow_ID = 2;
const float DXL_PROTOCOL_VERSION = 2.0;

Dynamixel2Arduino motorShoulder(motorShoulder_SERIAL, motorShoulder_DIR_PIN);
Dynamixel2Arduino motorElbow(motorElbow_SERIAL, motorElbow_DIR_PIN);

//This namespace is required to use Control table item names
using namespace ControlTableItem;

int max = 180;
int min = 0;
int ShoulderGoal = 0;

void setup() {
  
  DEBUG_SERIAL.begin(115200);
  while(!DEBUG_SERIAL);

  pinMode(BDPIN_PUSH_SW_1, INPUT);
  pinMode(BDPIN_PUSH_SW_2, INPUT);


  //motorShoulder Setup
  motorShoulder.begin(57600);
  motorShoulder.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  motorShoulder.ping(motorShoulder_ID);

  // Turn off torque when configuring items in EEPROM area
  motorShoulder.torqueOff(motorShoulder_ID);
  motorShoulder.setOperatingMode(motorShoulder_ID, OP_POSITION);
  motorShoulder.torqueOn(motorShoulder_ID);

  // Limit the maximum velocity in Position Control Mode. Use 0 for Max speed
  motorShoulder.writeControlTableItem(PROFILE_VELOCITY, motorShoulder_ID, 100);

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
}

void loop() {
  if(digitalRead(BDPIN_PUSH_SW_1))
  {
    ShoulderGoal += 5;
    if(ShoulderGoal >= 4095)
      ShoulderGoal = 4095;
  }
  else
  {
    ShoulderGoal -= 2;
    if(ShoulderGoal <= 0)
      ShoulderGoal = 0;
  }

  motorShoulder.setGoalPosition(motorShoulder_ID, ShoulderGoal);
  
}
