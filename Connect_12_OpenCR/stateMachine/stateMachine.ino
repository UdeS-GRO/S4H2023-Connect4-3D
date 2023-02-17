#include <Arduino.h>
#include <Dynamixel2Arduino.h>
#include <HardwareSerial.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/*---------------------------- DEFINES ---------------------------------------*/
//Serial
#define BAUDRATE 9600
#define motorShoulder_SERIAL    Serial3
#define Serial2                 Serial2
#define DEBUG_SERIAL            Serial

//Servos
#define motorShoulder_DIR_PIN   84
#define motorShoulder_ID        1
#define motorElbow_ID           3

//DcMotor
#define ENCA                    2       //External Interrupt 1
#define ENCB                    3       //External Interrupt 2
#define DcDir                   4       //Digital I/O
#define DcPWM                   5       //Digital I/O and PWM

//Carte OpenCR
#define DXL_PROTOCOL_VERSION    2.0

#define BDPIN_PUSH_SW_1         34      //Button 1
#define BDPIN_PUSH_SW_2         35      //Button 2
#define PIN_EMAGNET             9       //Digital I/O
#define PIN_LIMITSWITCH         6       //Digital I/O
#define LED1_PIN                22      //LED USER 1
#define LED2_PIN                23      //LED USER 2
#define LED3_PIN                24      //LED USER 3
#define LED4_PIN                25      //LED USER 4
#define LED5_PIN                13      //Arduino, LED built in

//Positions
#define HOME_POS_J1             0       // TODO: hardcoder la valeur
#define HOME_POS_J2             0       // TODO: hardcoder la valeur
#define HOME_POS_Z              0       // TODO: hardcoder la valeur
#define PICK_POS_J1             1000    // TODO: hardcoder la valeur
#define PICK_POS_J2             1000    // TODO: hardcoder la valeur
#define PICK_POS_Z              0       // TODO: hardcoder la valeur

/*---------------------------- ENUM AND STRUCT --------------------------------*/

enum FSM { S_MANUAL,
           S_AUTOMATIC
          };
FSM STATE;

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

enum FSM_MAN { SM_IDLE,
               SM_GO_TO_HOME,
               SM_GO_TO_PICK,
               SM_GO_TO_PLACE,
               SM_GO_DOWN_PLACE,
               SM_GO_DOWN_PICK,
               SM_GO_TO_LS,
               SM_GRIP, 
               SM_DROP
              };
FSM_MAN STATE_MAN;

struct PositionRegister { int j1;
                          int j2;
                          int z;
                        };
PositionRegister pr_home;
PositionRegister pr_pick;
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
void LED_DEBUG(int caseNumber);

/*---------------------------- VARIABLES DEFINITIONS --------------------------*/

//Serial
String  msg = "";
String  msg1 = "";
String  msg2 = "";
String  msg3   = "";
String  msg4 = "";
String  msg5 = "";

//Servo
Dynamixel2Arduino ServoMotor(motorShoulder_SERIAL, motorShoulder_DIR_PIN);
using namespace ControlTableItem;
int     motorAngleShoulderInt = 0;
int     motorAngleElbowInt = 0;
String  motorAngleShoulder = "";
String  motorAngleElbow = "";
String  motorAngle = "";

//DcMotor
unsigned long Count_pulses = 0;
int DcDirection = 0;

//States
int  fromPi_posJ1 = 0;
int  fromPi_posJ2 = 0;
int  fromPi_posZ = 0;

//bool fromPi_manual = true;
//bool fromPi_automatic = false;
int fromPi_Mode = 0;
int fromPi_Step = 0;

bool fromPi_auto_startSequence = false;
bool fromPi_auto_resetSequence = false;

bool fromPi_man_goToHome = false;
bool fromPi_man_goToPick = false;
bool fromPi_man_goToPlace = false;
bool fromPi_man_goDown = false;
bool fromPi_man_goToLS = false;
bool fromPi_man_grip = false;
bool fromPi_man_drop = false;

bool toPi_sequenceDone = false;

void setup() 
{
  Serial.begin(BAUDRATE);

  pinMode(PIN_EMAGNET, OUTPUT);
  pinMode(PIN_LIMITSWITCH, INPUT);
  pinMode(DcDir, OUTPUT);
  pinMode(DcPWM, OUTPUT);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
  pinMode(PIN_LIMITSWITCH, INPUT_PULLUP);

  digitalWrite(PIN_EMAGNET, LOW);

  attachInterrupt(digitalPinToInterrupt(ENCA), ReadEncoder, RISING);

  STATE = S_MANUAL;
  STATE_MAN = SM_IDLE;  
  STATE_AUTO = SA_GO_TO_HOME;
}

/*---------------------------- LOOP FUNCTION ----------------------------------*/

void loop() 
{
  readSerialPort();

  switch (STATE)
  {
    ////////// MANUAL SEQUENCE BELOW //////////
    case S_MANUAL:

      switch (STATE_MAN)
      {
        case SM_IDLE:
          
          if (fromPi_man_goToHome)
            STATE_MAN = SM_GO_TO_HOME;
          else if (fromPi_man_goToPick)
            STATE_MAN = SM_GO_TO_PICK;
          else if (fromPi_man_goToPlace)
            STATE_MAN = SM_GO_TO_PLACE;
          else if (fromPi_man_goDown)
            STATE_MAN = SM_GO_DOWN_PLACE;
          else if (fromPi_man_goToLS)
            STATE_MAN = SM_GO_TO_LS;
          else if (fromPi_man_grip)
            STATE_MAN = SM_GRIP;
          else if (fromPi_man_drop)
            STATE_MAN = SM_DROP;
          else
            break;
          break;

        case SM_GO_TO_HOME:
          LED_DEBUG(1);
          GoToPosition(pr_home);

          if (true)
          {
            STATE_MAN = SM_IDLE;
          }
          break;

        case SM_GO_TO_PICK:
          LED_DEBUG(2);
          GoToPosition(pr_pick);

          if (true)
          {
            STATE_MAN = SM_GO_DOWN_PICK;
          }
          break;

        case SM_GO_TO_PLACE:
          LED_DEBUG(3);
          GoToPosition(pr_place);

          if (true)
          {
            STATE_MAN = SM_IDLE;
          }
          break;

        case SM_GO_DOWN_PICK:
          LED_DEBUG(4);
          LowerEOAT(pr_place);
          
          if (Count_pulses >= pr_pick.z)
          {
            analogWrite(DcPWM, 0);
            STATE_MAN = SM_GO_TO_LS;
          }     
          break;

        case SM_GO_DOWN_PLACE:
          LED_DEBUG(5);
          LowerEOAT(pr_place);
          
          if (Count_pulses >= pr_place.z)
          {
            analogWrite(DcPWM, 0);
            STATE_MAN = SM_IDLE;
          }     
          break;

        case SM_GO_TO_LS:
          LED_DEBUG(6);          
          RaiseEOAT();

          if (true)
          {
            //RestingEOAT();
            STATE_MAN = SM_IDLE;
          }        
          break;

        case SM_GRIP:
          LED_DEBUG(7);
          ActivateMagnet(); 
          STATE_MAN = SM_IDLE;
          break;

        case SM_DROP:
          LED_DEBUG(8);
          DeactivateMagnet();
          STATE_MAN = SM_IDLE;
          break;

        default:
          STATE_MAN = SM_IDLE;
          break;
      }

      break;
    
    ////////// AUTOMATIC SEQUENCE BELOW //////////
    case S_AUTOMATIC:

      if (fromPi_auto_resetSequence)
      {
        STATE_AUTO = SA_IDLE;
        fromPi_auto_resetSequence = false;
      }

      switch (STATE_AUTO)
      {
        case SA_GO_TO_HOME:
          LED_DEBUG(9);
          GoToPosition(pr_home);

          if (true)
          {
            STATE_AUTO = SA_IDLE;
          }
          break;

        case SA_IDLE:
          LED_DEBUG(10);
          DeactivateMagnet();
          toPi_sequenceDone = true;

          if (fromPi_auto_startSequence)
          {
            fromPi_auto_startSequence = false;
            toPi_sequenceDone = false;
            STATE_AUTO = SA_GO_TO_PICK1;
          }
          break;

        case SA_GO_TO_PICK1:
          LED_DEBUG(11);
          GoToPosition(pr_pick);

          if (true)
          {
            STATE_AUTO = SA_GO_TO_PIECE;
          }
          break;

        case SA_GO_TO_PIECE:
          LED_DEBUG(12);
          LowerEOAT(pr_pick);

          if (true)
          {
            STATE_AUTO = SA_PICK_PIECE;
          }
          break;

        case SA_PICK_PIECE:
          LED_DEBUG(13);
          ActivateMagnet();
          if (true)
          {
            STATE_AUTO = SA_GO_TO_LS1;
          }
          break;

        case SA_GO_TO_LS1:
          LED_DEBUG(14);
          RaiseEOAT();
          if (true)
          {
            RestingEOAT();
            STATE_AUTO = SA_GO_TO_POS;
          }
          break;

        case SA_GO_TO_POS:
          LED_DEBUG(15);
          GoToPosition(pr_place);

          if (true)
          {
            STATE_AUTO = SA_GO_TO_FLOOR;
          }
          break;

        case SA_GO_TO_FLOOR:
          LED_DEBUG(16);
          LowerEOAT(pr_place);
          /*if (encoder >= pr_place.z)
          {
            RestingEOAT();
            encoder = 0;
            STATE_AUTO = SA_DROP_PIECE;
          }*/
          if (true)
          {
            STATE_AUTO = SA_DROP_PIECE;
          }
          break;

        case SA_DROP_PIECE:
          LED_DEBUG(17);
          DeactivateMagnet();
          if (true)                             // TODO: ajouter délai avec compteur
          {
            STATE_AUTO = SA_GO_TO_LS2;
          }
          break;

        case SA_GO_TO_LS2:
          LED_DEBUG(18);
          RaiseEOAT();
          if (IsLimitSwitchActivated())
          {
            RestingEOAT();
            STATE_AUTO = SA_GO_TO_HOME;
          }
          break;
        
        default:
          STATE_AUTO = SA_GO_TO_HOME;
          break;
      }

      break;
    
    default:
      STATE = S_MANUAL;
      break;
  }
}

/*---------------------------- FUNCTIONS --------------------------------------*/

void GoToPosition(PositionRegister pr)
{
  //RaiseEOAT();
  ServoMotor.setGoalPosition(motorShoulder_ID, pr.j1);
  ServoMotor.setGoalPosition(motorElbow_ID,   pr.j2);
  while(ServoMotor.getPresentPosition(motorShoulder_ID) != pr.j1 && ServoMotor.getPresentPosition(motorElbow_ID) != pr.j2);
  
}

void LowerEOAT(PositionRegister pr)
{
  digitalWrite(DcDir, HIGH);
  analogWrite(DcPWM, 255);
  /*
  do{
    //Read DC encoder
  }
  while(Count_pulses <= pr.z);

  analogWrite(DcPWM, 0);*/

}

void RaiseEOAT()
{
  digitalWrite(DcDir, HIGH);
  analogWrite(DcPWM, 127);

  while(!IsLimitSwitchActivated()){
    /*if(encoder value < -50){
      analogwrite(DcPWM, 0);
      //message erreur
    }*/
  }

  analogWrite(DcPWM, 0);

}

void RestingEOAT()
{
  //Motor.setSpeed(0); TODO: Mettre le moteur à OFF
}

void ReadEncoder()
{
  int b = digitalRead(ENCB);
  if(b > 0){
    Count_pulses++;
  }
  else{
    Count_pulses--;
  }
  //return Count_pulses;
}

bool IsLimitSwitchActivated()
{
  return digitalRead(PIN_LIMITSWITCH);
}

void ActivateMagnet()
{
  digitalWrite(PIN_EMAGNET, HIGH);
}

void DeactivateMagnet()
{
  digitalWrite(PIN_EMAGNET, LOW);
}

void sendData(){
  //besoin d<Envoyer quoi?:
  //mode; sequence finished; erreur; ???
  //while(Serial.available()<1){
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

    msg3 = "2000";

    msg4 = String(fromPi_Mode);

    msg5 = String(fromPi_Step);

    msg = msg1 + msg2 + msg3 + msg4 + msg5;
    //msg = "2000";
    Serial.print(msg);
  //}

  return;
}

void readSerialPort() {
  
  /*communication order:  [j1 j1 j1 j1  --> int 0-9 times 4
                          j2 j2 j2 j2   --> int 0-9 times 4
                          z z z z       --> int 0-9 times 4
                          mode          --> int 0 = manual, 1 = automatic
                          etat          --> int 0-9: 0 = state no1, 1 = state no2, [...], 9 = state no10
                          ]*/

 	if (Serial.available()) {
 			//delay(2);
      
      while (Serial.available() == 0 );
 			//while (Serial.available() > 0){
        motorAngle = Serial.readString();
      //}
 			Serial.flush();
 	}

  String stringJ1 = motorAngle.substring(0, 3);
  String stringJ2 = motorAngle.substring(4, 7);
  String stringZ = motorAngle.substring(8, 11);
  String stringMode = motorAngle.substring(12, 12);
  String stringStep = motorAngle.substring(13, 13);

  fromPi_Mode = stringMode.toInt();
  fromPi_Step = stringStep.toInt();

  fromPi_posJ1 = stringJ1.toInt();
  fromPi_posJ2 = stringJ2.toInt();
  fromPi_posZ = stringZ.toInt();

  pr_place.j1 = stringJ1.toInt();
  pr_place.j2 = stringJ2.toInt();
  pr_place.z = stringZ.toInt();

  if (fromPi_Mode == 1) 
    STATE = S_AUTOMATIC;
  else
    STATE = S_MANUAL;
  
  switch (fromPi_Step) {
    case 0:
      if(STATE == S_AUTOMATIC){
        fromPi_auto_startSequence = true;
        fromPi_auto_resetSequence = false;
      }
      else {
        fromPi_man_goToHome = true;
        fromPi_man_goToPick = false;
        fromPi_man_goToPlace = false;
        fromPi_man_goDown = false;
        fromPi_man_goToLS = false;
        fromPi_man_grip = false;
        fromPi_man_drop = false;
      }
      break;
    case 1:
      if(STATE == S_AUTOMATIC){
        fromPi_auto_startSequence = false;
        fromPi_auto_resetSequence = true;
      }
      else {
        fromPi_man_goToHome = false;
        fromPi_man_goToPick = true;
        fromPi_man_goToPlace = false;
        fromPi_man_goDown = false;
        fromPi_man_goToLS = false;
        fromPi_man_grip = false;
        fromPi_man_drop = false;
      }
      break;
    case 2:
      fromPi_man_goToHome = false;
      fromPi_man_goToPick = false;
      fromPi_man_goToPlace = true;
      fromPi_man_goDown = false;
      fromPi_man_goToLS = false;
      fromPi_man_grip = false;
      fromPi_man_drop = false;
      break;
    case 3:
      fromPi_man_goToHome = false;
      fromPi_man_goToPick = false;
      fromPi_man_goToPlace = false;
      fromPi_man_goDown = true;
      fromPi_man_goToLS = false;
      fromPi_man_grip = false;
      fromPi_man_drop = false;
      break;
    case 4:
      fromPi_man_goToHome = false;
      fromPi_man_goToPick = false;
      fromPi_man_goToPlace = false;
      fromPi_man_goDown = false;
      fromPi_man_goToLS = true;
      fromPi_man_grip = false;
      fromPi_man_drop = false;
      break;
    case 5:
      fromPi_man_goToHome = false;
      fromPi_man_goToPick = false;
      fromPi_man_goToPlace = false;
      fromPi_man_goDown = false;
      fromPi_man_goToLS = false;
      fromPi_man_grip = true;
      fromPi_man_drop = false;
      break;
    case 6:
      fromPi_man_goToHome = false;
      fromPi_man_goToPick = false;
      fromPi_man_goToPlace = false;
      fromPi_man_goDown = false;
      fromPi_man_goToLS = false;
      fromPi_man_grip = false;
      fromPi_man_drop = true;
      break;
    default:
      fromPi_man_goToHome = false;
      fromPi_man_goToPick = false;
      fromPi_man_goToPlace = false;
      fromPi_man_goDown = false;
      fromPi_man_goToLS = false;
      fromPi_man_grip = false;
      fromPi_man_drop = false;
      break;
  }

  /*int firstIndexDelimiter = motorAngle.indexOf('|');
  motorAngleShoulder = motorAngle.substring(0, firstIndexDelimiter);
  pr_place.j1 = motorAngleShoulder.toInt();

  int lastIndexDelimiter = motorAngle.lastIndexOf('|');
  motorAngleElbow = motorAngle.substring(firstIndexDelimiter+1, lastIndexDelimiter);
  pr_place.j1 = motorAngleElbow.toInt();*/

  //pr_place.j1 = fromPi_posJ1;
  //pr_place.j2 = fromPi_posJ2;
  //pr_place.z  = fromPi_posZ;

  return;
}

void LED_DEBUG(int caseNumber){
  bool LED1 = caseNumber % 2;
  bool LED2 = caseNumber % 4;
  bool LED3 = caseNumber % 8;
  bool LED4 = caseNumber % 16;
  bool LED5 = caseNumber % 32;
  digitalWrite(LED1_PIN, LED1);
  digitalWrite(LED2_PIN, LED2);
  digitalWrite(LED3_PIN, LED3);
  digitalWrite(LED4_PIN, LED4);
  digitalWrite(LED5_PIN, LED5);
}
