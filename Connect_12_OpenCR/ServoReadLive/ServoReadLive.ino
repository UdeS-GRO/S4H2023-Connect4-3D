#include <Arduino.h>
#include <Dynamixel2Arduino.h>
#include <HardwareSerial.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/*---------------------------- DEFINES ---------------------------------------*/
//Serial
#define BAUDRATE 9600
#define motorShoulder_SERIAL Serial3
//#define Serial2                 Serial2
#define Serial Serial

//Servos
#define motorShoulder_DIR_PIN 84
#define motorShoulder_ID 8
#define motorElbow_ID 3

//DcMotor
#define ENCA 2   //External Interrupt 1
#define ENCB 3   //External Interrupt 2
#define DcDir 4  //Digital I/O
#define DcPWM 5  //Digital I/O and PWM

//Carte OpenCR
#define DXL_PROTOCOL_VERSION 2.0

#define BDPIN_PUSH_SW_1 34  //Button 1
#define BDPIN_PUSH_SW_2 35  //Button 2
#define PIN_EMAGNET 9       //Digital I/O
#define PIN_LIMITSWITCH 6   //Digital I/O
#define LED1_PIN 22         //LED USER 1
#define LED2_PIN 23         //LED USER 2
#define LED3_PIN 24         //LED USER 3
#define LED4_PIN 25         //LED USER 4
#define LED5_PIN 13         //Arduino, LED built in
#define PIN_DEBUG 11

//Delays
#define delayBetweenStates 1000
#define delayPick 1000
#define delayPlace 1000

//Positions
#define HOME_POS_J1 4050  // TODO: hardcoder la valeur
#define HOME_POS_J2 3000  // TODO: hardcoder la valeur
#define HOME_POS_Z 0      // TODO: hardcoder la valeur
#define PICK_90_POS_J1 2472
#define PICK_90_POS_J2 3350
#define PICK_90_POS_Z 3050
#define PICK_45_POS_J1 2712
#define PICK_45_POS_J2 2776
#define PICK_45_POS_Z 3050

/*---------------------------- ENUM AND STRUCT --------------------------------*/

enum FSM_AUTO { SA_GO_TO_HOME,
                SA_IDLE,
                SA_GO_TO_PICK1,
                SA_GO_TO_PIECE,
                SA_PICK_PIECE,
                SA_GO_TO_LS1,
                SA_GO_TO_POS,
                SA_GO_TO_FLOOR,
                SA_DROP_PIECE,
                SA_GO_TO_LS2
};
FSM_AUTO STATE_AUTO;

struct PositionRegister {
  int j1;
  int j2;
  int z;
  int PieceLeft;
};
PositionRegister pr_home;
PositionRegister pr_pick;
PositionRegister pr_pick_90;
PositionRegister pr_pick_45;
PositionRegister pr_place;


/*---------------------------- FUNCTIONS DEFINITIONS --------------------------*/


/*---------------------------- VARIABLES DEFINITIONS --------------------------*/

//Serial
String msg = "";
String msg1 = "";
String msg2 = "";
String msg3 = "";
String msg4 = "";
String msg5 = "";

//Servo
Dynamixel2Arduino ServoMotor(motorShoulder_SERIAL, motorShoulder_DIR_PIN);
using namespace ControlTableItem;
int motorAngleShoulderInt = 0;
int motorAngleElbowInt = 0;
String motorAngleShoulder = "";
String motorAngleElbow = "";
String StringFromPi = "";
int positionTreshold = 10;

//DcMotor
long Count_pulses = 0;
int DcDirection = 0;

//Timers
unsigned long timerPickPieceStart;
unsigned long timerPlacePieceStart;
unsigned long timerBetweenStates;

//States
int fromPi_posJ1 = 0;
int fromPi_posJ2 = 0;
int fromPi_posZ = 0;

bool fromPi_Mode = true;  //Auto by default
int fromPi_State = 0;     //0 = idle, 1 = start, 2 = reset

// bool fromPi_auto_startSequence = false;
// bool fromPi_auto_resetSequence = false;

void setup() {
  Serial.begin(BAUDRATE);

  //motorShoulder Setup
  ServoMotor.begin(57600);
  ServoMotor.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  //ServoMotor.ping(motorShoulder_ID);

  // Turn off torque when configuring items in EEPROM area
  ServoMotor.torqueOff(motorShoulder_ID);
  ServoMotor.setOperatingMode(motorShoulder_ID, OP_POSITION);
  //ServoMotor.torqueOn(motorShoulder_ID);
  ServoMotor.torqueOff(motorElbow_ID);
  ServoMotor.setOperatingMode(motorElbow_ID, OP_POSITION);
  //ServoMotor.torqueOn(motorElbow_ID);

  // Limit the maximum velocity in Position Control Mode. Use 0 for Max speed
  ServoMotor.writeControlTableItem(PROFILE_VELOCITY, motorShoulder_ID, 50);
  ServoMotor.writeControlTableItem(PROFILE_VELOCITY, motorElbow_ID, 50);
}

void loop() {
  Serial.print(ServoMotor.getPresentPosition(motorShoulder_ID));
  Serial.print("\t");
  Serial.println(ServoMotor.getPresentPosition(motorElbow_ID));

}
