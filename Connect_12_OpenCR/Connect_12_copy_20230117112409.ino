#include <Dynamixel2Arduino.h>

// For OpenCR, there is a DXL Power Enable pin, so you must initialize and control it.
// Reference link : https://github.com/ROBOTIS-GIT/OpenCR/blob/master/arduino/opencr_arduino/opencr/libraries/DynamixelSDK/src/dynamixel_sdk/port_handler_arduino.cpp#L78
#define motorShoulder_SERIAL   Serial3
#define motorElbow_SERIAL   Serial2
#define DEBUG_SERIAL Serial
#define button1 34
#define button2 35

const int motorShoulder_DIR_PIN = 84; // OpenCR Board's DIR PIN.
const int motorElbow_DIR_PIN = 85; // OpenCR Board's DIR PIN.
const uint8_t motorShoulder_ID = 1;
const uint8_t motorElbow_ID = 2;
const float DXL_PROTOCOL_VERSION = 2.0;

Dynamixel2Arduino motorShoulder(motorShoulder_SERIAL, motorShoulder_DIR_PIN);
Dynamixel2Arduino motorElbow(motorElbow_SERIAL, motorElbow_DIR_PIN);

//This namespace is required to use Control table item names
using namespace ControlTableItem;

void setup() {
  
  DEBUG_SERIAL.begin(115200);

  //motorShoulder Setup
  motorShoulder.begin(57600);
  motorShoulder.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  motorShoulder.ping(motorShoulder_ID);

  // Turn off torque when configuring items in EEPROM area
  motorShoulder.torqueOff(motorShoulder_ID);
  motorShoulder.setOperatingMode(motorShoulder_ID, OP_POSITION);
  motorShoulder.torqueOn(motorShoulder_ID);

  // Limit the maximum velocity in Position Control Mode. Use 0 for Max speed
  motorShoulder.writeControlTableItem(PROFILE_VELOCITY, motorShoulder_ID, 30);

  //motorElbow Setup
  motorElbow.begin(57600);
  motorElbow.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  motorElbow.ping(motorElbow_ID);

  // Turn off torque when configuring items in EEPROM area
  motorElbow.torqueOff(motorElbow_ID);
  motorElbow.setOperatingMode(motorElbow_ID, OP_POSITION);
  motorElbow.torqueOn(motorElbow_ID);

  // Limit the maximum velocity in Position Control Mode. Use 0 for Max speed
  motorElbow.writeControlTableItem(PROFILE_VELOCITY, motorElbow_ID, 30);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(button1)){
    motorShoulder.setGoalPosition(motorShoulder_ID, 4000);
    delay(750);
    motorShoulder.setGoalPosition(motorShoulder_ID, 0);
  }
  if (digitalRead(button2)){
    motorElbow.setGoalPosition(motorElbow_ID, 4000);
    delay(750);
    motorElbow.setGoalPosition(motorElbow_ID, 0);
  }
}
