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
#define RED_LED_PIN 12         //LED USER 1
#define GREEN_LED_PIN 13         //LED USER 2
#define RESET_45 1
#define RESET_90 2
#define RESET_ALL 3
#define PICKPLACE_45 0
#define PICKPLACE_90 1
#define NO_VICTORY 0
#define HUMAN_VICTORY 1
#define ROBOT_VICTORY 2
#define START_NEW_GAME 3




//Delays
#define delayBetweenStates 1000
#define delayPick 1000
#define delayPlace 1000

//Positions
#define OFFSET_J1 190
#define OFFSET_J2 0
#define PIECE_OFFSET 300
#define HOME_POS_J1 4095 //+ OFFSET_J1 // TODO: hardcoder la valeur
#define HOME_POS_J2 3500 + OFFSET_J2 // TODO: hardcoder la valeur
#define HOME_POS_Z 0      // TODO: hardcoder la valeur
#define PICK_90_POS_J1 2318 + OFFSET_J1
#define PICK_90_POS_J2 3378 + OFFSET_J2
#define PICK_POS_Z 910
#define PICK_45_POS_J1 2600 + OFFSET_J1
#define PICK_45_POS_J2 2780 + OFFSET_J2
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
void PosPick();
void RobotTurnLED();
void HumanTurnLED();
void VictoryLED();

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
int ledState = LOW;  // ledState used to set the LED in Victory
unsigned long previousMillis = 0;  // will store last time LED was updated
const long interval = 200;  // interval at which to blink (milliseconds)

//States
int fromPi_posJ1 = 0;
int fromPi_posJ2 = 0;
int fromPi_posZ = 0;

bool StartSequence = 0;

int pickPlace = 0;  //Choose wich position to pick (0 for 45 degree and 1 for 90 degree)
int pickReset = 0;  //Reset to 8 the number of pieces (0 = nothing, 1 = reset 45, 2 = reset 90)
bool SequenceReset = 0;
int VictoryMsg = 0; //0 -> No victory, 1 -> Human Victory, 2 -> Robot Victory


void setup() {
  Serial.begin(BAUDRATE);

  pinMode(PIN_EMAGNET, OUTPUT);
  pinMode(PIN_LIMITSWITCH, INPUT);
  pinMode(DcDir, OUTPUT);
  pinMode(DcPWM, OUTPUT);
  pinMode(ENCA, INPUT);
  pinMode(ENCB, INPUT);
  pinMode(PIN_LIMITSWITCH, INPUT_PULLUP);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);


  digitalWrite(PIN_EMAGNET, LOW);
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, LOW);


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
  pr_pick_90.z = PICK_POS_Z;
  pr_pick_90.PieceLeft = 8;

  // pr_pick.j1 = PICK_45_POS_J1;
  // pr_pick.j2 = PICK_45_POS_J2;
  // pr_pick.z = PICK_POS_Z;
  // pr_pick.PieceLeft = 8;

  pr_pick_45.j1 = PICK_45_POS_J1;
  pr_pick_45.j2 = PICK_45_POS_J2;
  pr_pick_45.z = PICK_POS_Z;
  pr_pick_45.PieceLeft = 8;



  STATE_AUTO = SA_GO_TO_HOME;
}

/*---------------------------- LOOP FUNCTION ----------------------------------*/

void loop() {
  readSerialPort();
  if(SequenceReset)
  {
    STATE_AUTO = SA_GO_TO_HOME;
    SequenceReset = false;
  }

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
      HumanTurnLED();
      VictoryLED();
      // Serial.print("VictoryMsg");
      // Serial.println(VictoryMsg);

      if (StartSequence) {
        StartSequence = 0;
        STATE_AUTO = SA_GO_TO_PICK1;
        RobotTurnLED();
      }
      break;

    case SA_GO_TO_PICK1:
      GoToPosition(pr_pick);
      if (IsAtPosition(motorShoulder_ID, pr_pick.j1, 10) && IsAtPosition(motorElbow_ID, pr_pick.j2, 10)) {
        STATE_AUTO = SA_GO_TO_PIECE;
        delay(500);
      }
      break;

    case SA_GO_TO_PIECE:
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
        delay(500);
      }
      break;

    case SA_GO_TO_FLOOR:
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

void readSerialPort() {

  /*communication order:  [j1 j1 j1 j1  --> int 0-9 times 4
                          j2 j2 j2 j2   --> int 0-9 times 4
                          z z z z       --> int 0-9 times 4
                          msg4          --> PickPlace       0 for 45 degree or 1 for 90 degree
                          msg5          --> PickReset       1 to reset 45, 2 to reset 90 and 3 to reset all
                          msg6          --> SequenceReset   Not implemented in python
                          msg7          --> VictoryMessage  1 for human and 2 for robot
                          ]*/

    if (Serial.available() > 0) {

    StringFromPi = Serial.readString();

    String stringJ1 = String(StringFromPi.charAt(0)) + String(StringFromPi.charAt(1)) + String(StringFromPi.charAt(2)) + String(StringFromPi.charAt(3));
    String stringJ2 = String(StringFromPi.charAt(4)) + String(StringFromPi.charAt(5)) + String(StringFromPi.charAt(6)) + String(StringFromPi.charAt(7));
    String stringZ = String(StringFromPi.charAt(8)) + String(StringFromPi.charAt(9)) + String(StringFromPi.charAt(10)) + String(StringFromPi.charAt(11));
    String stringPickPlace = String(StringFromPi.charAt(12));
    pickPlace = stringPickPlace.toInt();
    String stringPickReset = String(StringFromPi.charAt(13));
    pickReset = stringPickReset.toInt();
    String stringSequenceReset = String(StringFromPi.charAt(14));
    SequenceReset = bool(stringSequenceReset);
    String stringVictoryMsg = String(StringFromPi.charAt(15));
    VictoryMsg = stringVictoryMsg.toInt();

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
    if (pickReset == RESET_45 || pickReset == RESET_ALL) //First move of the match is 3, so reset all
    {
      pr_pick_45.PieceLeft = 8;
      pr_pick_45.z = PICK_POS_Z;
    }
    if (pickReset == RESET_90 || pickReset == RESET_ALL)
    {
      pr_pick_90.PieceLeft = 8;
      pr_pick_90.z = PICK_POS_Z;
    }
    
    


    // Detect if Pickplace is 45 or 90
    if (pickPlace == PICKPLACE_45) 
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
    if(VictoryMsg != HUMAN_VICTORY && VictoryMsg != START_NEW_GAME) // Do not make a play if the human already won
      StartSequence = 1;

    if (VictoryMsg == START_NEW_GAME) //If a new game is started, disable the blinking LED
      {
        VictoryMsg = 0;
      }

    Serial.flush();
  }
  return;
}


bool IsAtPosition(int MotorID, int EndPos, int Treshold) {
  return (ServoMotor.getPresentPosition(MotorID) >= (EndPos - Treshold)) && (ServoMotor.getPresentPosition(MotorID) <= (EndPos + Treshold));
}

void PosPick() {
  if (pickPlace == PICK_45_ID && pr_pick_45.PieceLeft > 1) {
    pr_pick_45.z += PIECE_OFFSET;
    pr_pick_45.PieceLeft -= 1;
  } else if (pickPlace == PICK_45_ID && pr_pick_45.PieceLeft <= 1) {
    pr_pick_45.PieceLeft = 8;
    pr_pick_45.z = PICK_POS_Z;
  } else if (pickPlace == PICK_90_ID && pr_pick_90.PieceLeft > 1) {
    pr_pick_90.z += PIECE_OFFSET;
    pr_pick_90.PieceLeft -= 1;
  } else if (pickPlace == PICK_90_ID && pr_pick_90.PieceLeft <= 1) {
    pr_pick_90.PieceLeft = 8;
    pr_pick_90.z = PICK_POS_Z;
  }
}

void RobotTurnLED() {

  if(VictoryMsg == NO_VICTORY)
  {
    digitalWrite(RED_LED_PIN, true);
    digitalWrite(GREEN_LED_PIN, false);
  }

}
void HumanTurnLED() {
  if(VictoryMsg == NO_VICTORY)
  {
    digitalWrite(RED_LED_PIN, false);
    digitalWrite(GREEN_LED_PIN, true);
  }

}
void VictoryLED() {
  int LED_PIN;
  int Loser_LED_PIN;
  
  // Select LED to open
  if(VictoryMsg == HUMAN_VICTORY)
  {
    LED_PIN = GREEN_LED_PIN;
    Loser_LED_PIN = RED_LED_PIN; 
  }
  else if(VictoryMsg == ROBOT_VICTORY)
  {
    LED_PIN = RED_LED_PIN;
    Loser_LED_PIN = GREEN_LED_PIN;
  }
  
  // Flash the LED
  if(VictoryMsg != NO_VICTORY)
    {
    if (millis() - previousMillis >= interval) {
      // save the last time you blinked the LED
      previousMillis = millis();

      // if the LED is off turn it on and vice-versa:
      if (ledState == LOW) {
        ledState = HIGH;
      }
      else {
        ledState = LOW;
      }

    // set the LED with the ledState of the variable:
    digitalWrite(LED_PIN, ledState);
    digitalWrite(Loser_LED_PIN, false);
    }
  }
}


