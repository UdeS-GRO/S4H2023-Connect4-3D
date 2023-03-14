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
#define PICK_90_POS_J1 2575
#define PICK_90_POS_J2 2968
#define PICK_90_POS_Z 675
#define PICK_45_POS_J1 2850
#define PICK_45_POS_J2 2350
#define PICK_45_POS_Z 675
#define PICK_45_ID 0
#define PICK_90_ID 1

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

void GoToPosition(PositionRegister pr);
void LowerEOAT(PositionRegister pr);
void RaiseEOAT();
void RestingEOAT();
void ReadEncoder();
bool IsLimitSwitchActivated();
void ActivateMagnet();
void DeactivateMagnet();
void readSerialPort();
void sendData(int msg2send);
void PosPick();

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

bool StartSequence = 0;

int pickPlace = 0;  //Choose wich position to pick (0 for 45 degree and 1 for 90 degree)
int pickReset = 0;  //Reset to 8 the number of pieces (0 = nothing, 1 = reset 45, 2 = reset 90)

void setup() {
  Serial.begin(BAUDRATE);

  pinMode(PIN_EMAGNET, OUTPUT);
  pinMode(PIN_LIMITSWITCH, INPUT);
  pinMode(DcDir, OUTPUT);
  pinMode(DcPWM, OUTPUT);
  pinMode(ENCA, INPUT);
  pinMode(ENCB, INPUT);
  pinMode(PIN_LIMITSWITCH, INPUT_PULLUP);
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(LED3_PIN, OUTPUT);
  pinMode(LED4_PIN, OUTPUT);
  pinMode(LED5_PIN, OUTPUT);
  pinMode(PIN_DEBUG, OUTPUT);

  digitalWrite(PIN_EMAGNET, LOW);
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);
  digitalWrite(LED3_PIN, LOW);
  digitalWrite(LED4_PIN, LOW);
  digitalWrite(LED5_PIN, LOW);
  digitalWrite(PIN_DEBUG, LOW);

  attachInterrupt(digitalPinToInterrupt(ENCA), ReadEncoder, RISING);

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

  //Positions
  pr_home.j1 = HOME_POS_J1;
  pr_home.j2 = HOME_POS_J2;
  pr_home.z = HOME_POS_Z;

  pr_pick_90.j1 = PICK_90_POS_J1;
  pr_pick_90.j2 = PICK_90_POS_J2;
  pr_pick_90.z = PICK_90_POS_Z;
  pr_pick_90.PieceLeft = 8;

  // pr_pick.j1 = PICK_45_POS_J1;
  // pr_pick.j2 = PICK_45_POS_J2;
  // pr_pick.z = PICK_45_POS_Z;
  // pr_pick.PieceLeft = 8;

  pr_pick_45.j1 = PICK_45_POS_J1;
  pr_pick_45.j2 = PICK_45_POS_J2;
  pr_pick_45.z = PICK_45_POS_Z;
  pr_pick_45.PieceLeft = 8;

  pr_place.j1 = 3000;
  pr_place.j2 = 1000;
  pr_place.z = 1000;

  STATE_AUTO = SA_GO_TO_HOME;
}

/*---------------------------- LOOP FUNCTION ----------------------------------*/

void loop() {

  switch (STATE_AUTO) {

    case SA_GO_TO_HOME:
      RaiseEOAT();
      if (IsLimitSwitchActivated()) {
        Count_pulses = 0;
        RestingEOAT();

        GoToPosition(pr_home);

        if (IsAtPosition(motorShoulder_ID, pr_home.j1, 6) && IsAtPosition(motorElbow_ID, pr_home.j2, 6)) {
          STATE_AUTO = SA_IDLE;
        }
      }
      break;

    case SA_IDLE:
      RestingEOAT();
      DeactivateMagnet();
      readSerialPort();

      if (StartSequence) {
        StartSequence = 0;
        STATE_AUTO = SA_GO_TO_PICK1;
      }
      break;

    case SA_GO_TO_PICK1:
      GoToPosition(pr_pick);
      if (IsAtPosition(motorShoulder_ID, pr_pick.j1, 10) && IsAtPosition(motorElbow_ID, pr_pick.j2, 10)) {
        STATE_AUTO = SA_GO_TO_PIECE;
      }
      break;

    case SA_GO_TO_PIECE:
      delay(500);
      LowerEOAT(pr_pick);

      if (Count_pulses >= pr_pick.z) {
        RestingEOAT();
        PosPick();
        timerPickPieceStart = millis();
        STATE_AUTO = SA_PICK_PIECE;
      }
      break;

    case SA_PICK_PIECE:
      ActivateMagnet();

      if ((millis() - timerPickPieceStart) >= delayPick) {
        STATE_AUTO = SA_GO_TO_LS1;
      }
      break;

    case SA_GO_TO_LS1:
      RaiseEOAT();

      if (IsLimitSwitchActivated()) {
        RestingEOAT();
        Count_pulses = 0;
        STATE_AUTO = SA_GO_TO_POS;
      }
      break;

    case SA_GO_TO_POS:
      GoToPosition(pr_place);

      if (IsAtPosition(motorShoulder_ID, pr_place.j1, 6) && IsAtPosition(motorElbow_ID, pr_place.j2, 6)) {
        STATE_AUTO = SA_GO_TO_FLOOR;
      }
      break;

    case SA_GO_TO_FLOOR:
      delay(500);
      LowerEOAT(pr_place);
      if (Count_pulses >= pr_place.z) {
        RestingEOAT();
        timerPlacePieceStart = millis();
        STATE_AUTO = SA_DROP_PIECE;
      }
      break;

    case SA_DROP_PIECE:
      DeactivateMagnet();
      if (millis() - timerPlacePieceStart >= delayPlace) {
        STATE_AUTO = SA_GO_TO_LS2;
      }
      break;

    case SA_GO_TO_LS2:
      RaiseEOAT();
      if (IsLimitSwitchActivated()) {
        RestingEOAT();
        Count_pulses = 0;
        STATE_AUTO = SA_GO_TO_HOME;
      }
      break;

    default:
      STATE_AUTO = SA_GO_TO_HOME;
      break;
  }
}

/*---------------------------- FUNCTIONS --------------------------------------*/

void GoToPosition(PositionRegister pr) {
  ServoMotor.setGoalPosition(motorShoulder_ID, pr.j1);
  ServoMotor.setGoalPosition(motorElbow_ID, pr.j2);
}

void LowerEOAT(PositionRegister pr) {
  digitalWrite(DcDir, HIGH);
  analogWrite(DcPWM, 200);
}

void RaiseEOAT() {
  digitalWrite(DcDir, LOW);
  analogWrite(DcPWM, 127);
}

void RestingEOAT() {
  analogWrite(DcPWM, 0);
}

void ReadEncoder() {
  int b = digitalRead(ENCB);
  if (b > 0) {
    Count_pulses++;
  } else {
    Count_pulses--;
  }
}

bool IsLimitSwitchActivated() {
  return !digitalRead(PIN_LIMITSWITCH);
}

void ActivateMagnet() {
  digitalWrite(PIN_EMAGNET, HIGH);
}

void DeactivateMagnet() {
  digitalWrite(PIN_EMAGNET, LOW);
}

void sendData() {

  while (Serial.available() < 1) {
    float SendShoulderPosFloat = ServoMotor.getPresentPosition(motorShoulder_ID);
    int SendShoulderPos = round(SendShoulderPosFloat);
    String SendShoulderPosStr = String(SendShoulderPos);

    float SendElbowPosFloat = ServoMotor.getPresentPosition(motorElbow_ID);
    int SendElbowPos = round(SendElbowPosFloat);
    String SendElbowPosStr = String(SendElbowPos);

    if (SendShoulderPosStr.length() == 0) {
      msg1 = "0000";
    } else if (SendShoulderPosStr.length() == 1) {
      msg1 = "000" + SendShoulderPosStr;
    } else if (SendShoulderPosStr.length() == 2) {
      msg1 = "00" + SendShoulderPosStr;
    } else if (SendShoulderPosStr.length() == 3) {
      msg1 = "0" + SendShoulderPosStr;
    } else {
      msg1 = SendShoulderPosStr;
    }

    if (SendElbowPosStr.length() == 0) {
      msg2 = "0000";
    } else if (SendElbowPosStr.length() == 1) {
      msg2 = "000" + SendElbowPosStr;
    } else if (SendElbowPosStr.length() == 2) {
      msg2 = "00" + SendElbowPosStr;
    } else if (SendElbowPosStr.length() == 3) {
      msg2 = "0" + SendElbowPosStr;
    } else {
      msg2 = SendElbowPosStr;
    }

    if (String(Count_pulses).length() == 0) {
      msg3 = "0000";
    } else if (String(Count_pulses).length() == 1) {
      msg3 = "000" + SendElbowPosStr;
    } else if (String(Count_pulses).length() == 2) {
      msg3 = "00" + SendElbowPosStr;
    } else if (String(Count_pulses).length() == 3) {
      msg3 = "0" + SendElbowPosStr;
    } else {
      msg3 = String(Count_pulses);
    }

    msg3 = "1234";

    //msg4 = String(fromPi_Mode);

    //msg5 = String(fromPi_State);

    msg = msg1 + msg2 + msg3 + msg4 + msg5;
  }
}

void readSerialPort() {

  /*communication order:  [j1 j1 j1 j1  --> int 0-9 times 4
                          j2 j2 j2 j2   --> int 0-9 times 4
                          z z z z       --> int 0-9 times 4
                          mode          --> int 0 = manual, 1 = automatic
                          etat          --> int 0-9: 0 = state no1, 1 = state no2, [...], 9 = state no10
                          ]*/

  if (Serial.available() == 0) {
  } else if (Serial.available() > 0) {

    StringFromPi = Serial.readString();

    String stringJ1 = String(StringFromPi.charAt(0)) + String(StringFromPi.charAt(1)) + String(StringFromPi.charAt(2)) + String(StringFromPi.charAt(3));
    String stringJ2 = String(StringFromPi.charAt(4)) + String(StringFromPi.charAt(5)) + String(StringFromPi.charAt(6)) + String(StringFromPi.charAt(7));
    String stringZ = String(StringFromPi.charAt(8)) + String(StringFromPi.charAt(9)) + String(StringFromPi.charAt(10)) + String(StringFromPi.charAt(11));
    String stringPickPlace = String(StringFromPi.charAt(12));
    pickPlace = stringPickPlace.toInt();
    String stringPickReset = String(StringFromPi.charAt(13));
    pickReset = stringPickReset.toInt();

    pr_place.j1 = stringJ1.toInt();
    pr_place.j2 = stringJ2.toInt();
    pr_place.z = stringZ.toInt();


    // Safety - Go to home if message is (0,0,0)
    if (pr_place.j1 <= 10)
      pr_place.j1 = pr_home.j1;
    if (pr_place.j2 <= 200)
      pr_place.j2 = pr_home.j2;
    if (pr_place.z == 0)
      pr_place.z = pr_home.z;


    // Reset PieceLeft
    if (pickReset == 1 || pickReset == 3) //First move of the match is 3, so reset all
    {
      pr_pick_45.PieceLeft = 8;
      pr_pick_45.z = PICK_45_POS_Z;
    }
    if (pickReset == 2 || pickReset == 3)
    {
      pr_pick_90.PieceLeft = 8;
      pr_pick_90.z = PICK_90_POS_Z;
    }
    


    // Detect if Pickplace is 45 or 90
    if (pickPlace == 0) 
    {
    pr_pick.j1 = pr_pick_45.j1;
    pr_pick.j2 = pr_pick_45.j2;
    pr_pick.z = pr_pick_45.z;
    pr_pick.PieceLeft = pr_pick_45.PieceLeft;
    }
    else 
    {
      pr_pick.j1 = pr_pick_90.j1;
      pr_pick.j2 = pr_pick_90.j2;
      pr_pick.z = pr_pick_90.z;
      pr_pick.PieceLeft = pr_pick_90.PieceLeft;
    }
    StartSequence = 1;
    Serial.flush();
  }

  return;
}

void PWMDebug(int Step) {
  analogWrite(PIN_DEBUG, 25 * Step);
}

bool IsAtPosition(int MotorID, int EndPos, int Treshold) {
  return (ServoMotor.getPresentPosition(MotorID) >= (EndPos - Treshold)) && (ServoMotor.getPresentPosition(MotorID) <= (EndPos + Treshold));
}

void PosPick() {
  if (pickPlace == PICK_45_ID && pr_pick_45.PieceLeft > 0) {
    pr_pick_45.z += 300;
    pr_pick_45.PieceLeft -= 1;
  } else if (pickPlace == PICK_90_ID && pr_pick_90.PieceLeft > 0) {
    pr_pick_90.z += 300;
    pr_pick_90.PieceLeft -= 1;
  }
}
