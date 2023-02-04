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
String ShoulderAngle;
String ElbowAngle;
String msg;
int AngleGoal[2];
int angles[2];
const int BUFFER_SIZE = 4;
char buf[BUFFER_SIZE];

int pingMotors(int nbMot);
void getMsg();
int readSerialPort();
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
  //ServoMotor.writeControlTableItem(PROFILE_VELOCITY, motorElbow_ID, 50);

  
}

void loop() {

  /*if(DEBUG_SERIAL.available() > 0)
  {
      DEBUG_SERIAL.println("ok");
  }*/

  //String ShoulderAngle = readSerialPort();
  //int ShoulderAngleint = ShoulderAngle.toInt();
  int Shoulder = readSerialPort();
  sendData(AngleGoal[0]);
  int Elbow = readSerialPort();
  sendData(AngleGoal[1]);
  //sendData(ElbowAngle.toInt());
  //sendData(AngleGoal[0]);
  //sendData(AngleGoal[1]);
  //sendData(ShoulderAngleint);
  //String ElbowAngle = readSerialPort();
  //int ElbowAngleint = ElbowAngle.toInt();
  //sendData(ElbowAngleint);

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

  ServoMotor.setGoalPosition(motorShoulder_ID, Shoulder);
  //ServoMotor.setGoalPosition(motorElbow_ID, ElbowGoal);
  while(ServoMotor.getPresentPosition(motorShoulder_ID) == Shoulder);
  //delay(10);
  //sendData(ServoMotor.getPresentPosition(motorShoulder_ID));
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

int readSerialPort() {
  msg = "";
  String motorAngle = "";
  //ShoulderAngle = "";
  //ElbowAngle = "";
  //char msgChar;
 	if (Serial.available()) {
 			//delay(2);
      
      while (Serial.available() == 0 );
 			while (Serial.available() > 0){
       /*
       
         for(int c = 0; c < 10; c++)
         {
           if(c == 0 || c == 5)
           {
             Serial.read();
           }
           else if (c >= 1 && c <= 4)
           {
             ShoulderAngle += Serial.read();
           }
           else if (c >= 6 && c <= 9)
           {
             ElbowAngle += Serial.read();
           }
         }
       }*/
        /*
 			  msg = Serial.read();
        if (msg == "S"){
          ShoulderAngle += Serial.read();
          ShoulderAngle += Serial.read();
          ShoulderAngle += Serial.read();
          ShoulderAngle += Serial.read();
        }
        else if (msg == "E"){
          ShoulderAngle += Serial.read();
          ShoulderAngle += Serial.read();
          ShoulderAngle += Serial.read();
          ShoulderAngle += Serial.read();
        }
 			*/
        Serial.read();
        motorAngle = Serial.readStringUntil('\n');

      }
 			Serial.flush();
 	}
  //AngleGoal[0] = ShoulderAngle.toInt();
  //AngleGoal[1] = ElbowAngle.toInt();
  return motorAngle.toInt();
}

void sendData(int msg2send) {
  String msg2sendStr = String(msg2send);
  //String msgWrite = String(msg2send);
  //buf[0] =msg2send;
  //Serial.write(buf, BUFFER_SIZE);
  if(msg2sendStr.length() == 3){
    msg = '0' + msg2sendStr;
  }
  else{
    msg = msg2sendStr;
  }
  Serial.print(msg);
  return;
}
