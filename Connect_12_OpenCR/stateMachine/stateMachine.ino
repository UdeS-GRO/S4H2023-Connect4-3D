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
//#define Serial2                 Serial2
#define Serial            Serial

//Servos
#define motorShoulder_DIR_PIN   84
#define motorShoulder_ID        8
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
#define PIN_DEBUG               11

//Delays
#define delayBetweenStates      1000
#define delayPick               1000
#define delayPlace              1000

//Positions
#define HOME_POS_J1             4050       // TODO: hardcoder la valeur
#define HOME_POS_J2             3000       // TODO: hardcoder la valeur
#define HOME_POS_Z              0       // TODO: hardcoder la valeur
#define PICK_POS_J1             4050    // TODO: hardcoder la valeur
#define PICK_POS_J2             1500    // TODO: hardcoder la valeur
#define PICK_POS_Z              2750       // TODO: hardcoder la valeur

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
String  StringFromPi = "";

//DcMotor
long Count_pulses = 0;
int DcDirection = 0;  

//Timers
unsigned long timerPickPieceStart;
unsigned long timerPlacePieceStart;
unsigned long timerBetweenStates;

//States
int  fromPi_posJ1 = 0;
int  fromPi_posJ2 = 0;
int  fromPi_posZ = 0;

//bool fromPi_manual = true;
//bool fromPi_automatic = false;
bool fromPi_Mode = false;   //Manual by default
int fromPi_State = 0;

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

bool error;

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

  pr_pick.j1 = PICK_POS_J1;
  pr_pick.j2 = PICK_POS_J2;
  pr_pick.z = PICK_POS_Z;

  pr_place.j1 = 3000;
  pr_place.j2 = 1000;
  pr_place.z = 1000;

  //STATE = S_MANUAL;
  STATE = S_MANUAL;
  STATE_MAN = SM_IDLE;  
  STATE_AUTO = SA_GO_TO_HOME;

  PWMDebug(0);

}

/*---------------------------- LOOP FUNCTION ----------------------------------*/

void loop() 
{
  readSerialPort();
  //Serial.println(digitalRead(PIN_LIMITSWITCH));

  switch (STATE)
  {
    ////////// MANUAL SEQUENCE BELOW //////////
    case S_MANUAL:
      //GoToPosition(pr_pick);
      
      switch (STATE_MAN)
      {
        case SM_IDLE:
          RestingEOAT();        
          Count_pulses = 0;
          
          // fromPi_man_goToHome = false;
          // fromPi_man_goToPick = false;
          // fromPi_man_goToPlace = false;
          // fromPi_man_goDown = false;
          // fromPi_man_goToLS = false;
          // fromPi_man_grip = false;
          // fromPi_man_drop = false;

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
          
          RaiseEOAT();
          if(IsLimitSwitchActivated()){
            Count_pulses = 0;
            GoToPosition(pr_home);
            RestingEOAT();
          }

          if (IsAtPosition(motorShoulder_ID, pr_home.j1, 6) && IsAtPosition(motorElbow_ID, pr_home.j2, 6))
          {
            STATE_MAN = SM_IDLE;
          }
          break;

        case SM_GO_TO_PICK:
          GoToPosition(pr_pick);

          if (IsAtPosition(motorShoulder_ID, pr_pick.j1, 6) && IsAtPosition(motorElbow_ID, pr_pick.j2, 6))
          {
            STATE_MAN = SM_GO_DOWN_PICK;
          }
          break;

        case SM_GO_TO_PLACE:

          GoToPosition(pr_place);

          if (IsAtPosition(motorShoulder_ID, pr_place.j1, 6) && IsAtPosition(motorElbow_ID, pr_place.j2, 6))
          {
            STATE_MAN = SM_IDLE;
          }
          break;

        case SM_GO_DOWN_PICK:
          LowerEOAT(pr_pick);
          
          if (Count_pulses >= pr_pick.z)
          {
            RestingEOAT();
            Count_pulses = 0;
            STATE_MAN = SM_IDLE;
          }     
          break;

        case SM_GO_DOWN_PLACE:
          LED_DEBUG(5);
          LowerEOAT(pr_place);
          
          if (Count_pulses >= pr_place.z)
          {
            RestingEOAT();
            Count_pulses = 0;
            STATE_MAN = SM_IDLE;
          }     
          break;

        case SM_GO_TO_LS:
         
          RaiseEOAT();

          if (IsLimitSwitchActivated())
          {
            RestingEOAT();
            Count_pulses = 0;
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
      
      //GoToPosition(pr_place);
      if (fromPi_auto_resetSequence)
      {
        STATE_AUTO = SA_IDLE;
        fromPi_auto_resetSequence = false;
      }

      switch (STATE_AUTO)
      {
        
        case SA_GO_TO_HOME:
          RaiseEOAT();
          if(IsLimitSwitchActivated()){
            Count_pulses = 0;
            GoToPosition(pr_home);
            RestingEOAT();
          }

          if (IsAtPosition(motorShoulder_ID, pr_home.j1, 6) && IsAtPosition(motorElbow_ID, pr_home.j2, 6))
          {
            
            STATE_AUTO = SA_IDLE;
          }
          break;

        case SA_IDLE:
          LED_DEBUG(10);
          DeactivateMagnet();
          //digitalWrite(DcPWM, 0);
          toPi_sequenceDone = true;

          if (digitalRead(BDPIN_PUSH_SW_1))//fromPi_auto_startSequence == true)
          {
            //fromPi_auto_startSequence = false;
            //toPi_sequenceDone = false;
            STATE_AUTO = SA_GO_TO_PICK1;
          }
          break;

        case SA_GO_TO_PICK1:
          LED_DEBUG(11);
          GoToPosition(pr_pick);

          if (IsAtPosition(motorShoulder_ID, pr_pick.j1, 10) && IsAtPosition(motorElbow_ID, pr_pick.j2, 10))
          {
            //timerBetweenStates = millis();
            //if(timerBetweenStates - millis() >= delayBetweenStates)
            //{
              //timerBetweenStates = millis();
              STATE_AUTO = SA_GO_TO_PIECE;
            //}
          }
          break;

        case SA_GO_TO_PIECE:
          LED_DEBUG(12);
          LowerEOAT(pr_pick);

          if (Count_pulses >= pr_pick.z)
          {
            RestingEOAT();
            timerPickPieceStart = millis();
            STATE_AUTO = SA_PICK_PIECE;
          }
          break;

        case SA_PICK_PIECE:
          LED_DEBUG(13);
          ActivateMagnet();

          if ((millis() - timerPickPieceStart) >= delayPick)
          {
            STATE_AUTO = SA_GO_TO_LS1;
          }
          break;

        case SA_GO_TO_LS1:
          LED_DEBUG(14);
          RaiseEOAT();

          if(IsLimitSwitchActivated()){
            RestingEOAT();
            Count_pulses = 0;
            STATE_AUTO = SA_GO_TO_POS;
          }
          break;

        case SA_GO_TO_POS:
          LED_DEBUG(15);
          GoToPosition(pr_place);

          if (IsAtPosition(motorShoulder_ID, pr_place.j1, 6) && IsAtPosition(motorElbow_ID, pr_place.j2, 6))
          {
            //timerBetweenStates = millis();
            //if(timerBetweenStates >= delayBetweenStates)
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
          if (Count_pulses >= pr_place.z)
          {
            RestingEOAT();
            timerPlacePieceStart = millis();
            STATE_AUTO = SA_DROP_PIECE;
          }
          break;

        case SA_DROP_PIECE:
          LED_DEBUG(17);
          DeactivateMagnet();
          if (millis() - timerPlacePieceStart >= delayPlace)                             // TODO: ajouter délai avec compteur
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
            Count_pulses = 0;
            STATE_AUTO = SA_GO_TO_HOME;
          }
          break;

        default:
          STATE_AUTO = SA_GO_TO_HOME;
          break;
      }   
      break;
    
    default:
      //STATE = S_MANUAL;
      STATE = S_AUTOMATIC;
      break;
  }
}

/*---------------------------- FUNCTIONS --------------------------------------*/

void GoToPosition(PositionRegister pr)
{
  ServoMotor.setGoalPosition(motorShoulder_ID, pr.j1);
  //Serial.print("SHoulder Present position: ");
  //Serial.println(ServoMotor.getPresentPosition(motorShoulder_ID));
  //LED_DEBUG(4);
  //sendData();
  ServoMotor.setGoalPosition(motorElbow_ID,   pr.j2);
  //while(ServoMotor.getPresentPosition(motorShoulder_ID) != pr.j1 && ServoMotor.getPresentPosition(motorElbow_ID) != pr.j2);
  
}

void LowerEOAT(PositionRegister pr)
{
  digitalWrite(DcDir, HIGH);
  analogWrite(DcPWM, 200);
  
  /*
  do{
    //Read DC encoder
  }
  while(Count_pulses <= pr.z);

  analogWrite(DcPWM, 0);*/

}

void RaiseEOAT()
{
  digitalWrite(DcDir, LOW);
  analogWrite(DcPWM, 127);

  /*if(IsLimitSwitchActivated() || Count_pulses < 0){
    analogWrite(DcPWM, 0);
    Count_pulses = 0;
  }*/
}

void RestingEOAT()
{
  analogWrite(DcPWM, 0);
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
  return !digitalRead(PIN_LIMITSWITCH);
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
  while(Serial.available()<1){
    float SendShoulderPosFloat = ServoMotor.getPresentPosition(motorShoulder_ID);
    int SendShoulderPos = round(SendShoulderPosFloat);
    String SendShoulderPosStr = String(SendShoulderPos);

    float SendElbowPosFloat = ServoMotor.getPresentPosition(motorElbow_ID);
    int SendElbowPos = round(SendElbowPosFloat);
    String SendElbowPosStr = String(SendElbowPos);
    
    if(SendShoulderPosStr.length() == 0){
      msg1 = "0000";
    }
    else if(SendShoulderPosStr.length() == 1){
      msg1 = "000" + SendShoulderPosStr;
    }
    else if(SendShoulderPosStr.length() == 2){
      msg1 = "00" + SendShoulderPosStr;
    }
    else if(SendShoulderPosStr.length() == 3){
      msg1 = "0" + SendShoulderPosStr;
    }
    else{
      msg1 = SendShoulderPosStr;
    }

    if(SendElbowPosStr.length() == 0){
      msg2 = "0000";
    }
    else if(SendElbowPosStr.length() == 1){
      msg2 = "000" + SendElbowPosStr;
    }
    else if(SendElbowPosStr.length() == 2){
      msg2 = "00" + SendElbowPosStr;
    }
    else if(SendElbowPosStr.length() == 3){
      msg2 = "0" + SendElbowPosStr;
    }
    else{
      msg2 = SendElbowPosStr;
    }

    if(String(Count_pulses).length() == 0){
      msg3 = "0000";
    }
    else if(String(Count_pulses).length() == 1){
      msg3 = "000" + SendElbowPosStr;
    }
    else if(String(Count_pulses).length() == 2){
      msg3 = "00" + SendElbowPosStr;
    }
    else if(String(Count_pulses).length() == 3){
      msg3 = "0" + SendElbowPosStr;
    }
    else{
      msg3 = String(Count_pulses);
    }

    msg3 = "1234";

    msg4 = String(fromPi_Mode);

    msg5 = String(fromPi_State);

    msg = msg1 + msg2 + msg3 + msg4 + msg5;
    //msg = "2000";
    
    //Serial.print(msg);
  }

  //return;
}

void readSerialPort() {
  
  /*communication order:  [j1 j1 j1 j1  --> int 0-9 times 4
                          j2 j2 j2 j2   --> int 0-9 times 4
                          z z z z       --> int 0-9 times 4
                          mode          --> int 0 = manual, 1 = automatic
                          etat          --> int 0-9: 0 = state no1, 1 = state no2, [...], 9 = state no10
                          ]*/

  if (Serial.available() == 0){
  }
 	else if (Serial.available() >= 0) {
 			//delay(2);
      //while (Serial.available() == 0 );
 			//while (Serial.available() > 0){
        StringFromPi = Serial.readString();
        //LED_DEBUG(StringFromPi.length());

        //delay(1000);
      //}
 			
 	}
  Serial.flush();

  //String stringJ1 = StringFromPi.substring(0, 3);
  String stringJ1 = String(StringFromPi.charAt(0)) + String(StringFromPi.charAt(1)) + String(StringFromPi.charAt(2)) + String(StringFromPi.charAt(3));
  //String stringJ2 = StringFromPi.substring(4, 7);
  String stringJ2 = String(StringFromPi.charAt(4)) + String(StringFromPi.charAt(5)) + String(StringFromPi.charAt(6)) + String(StringFromPi.charAt(7));
  //String stringZ = StringFromPi.substring(8, 11);
  String stringZ = String(StringFromPi.charAt(8)) + String(StringFromPi.charAt(9)) + String(StringFromPi.charAt(10)) + String(StringFromPi.charAt(11));
  //String stringMode = StringFromPi.substring(12, 12);
  String stringMode = String(StringFromPi.charAt(12));
  //String stringState = StringFromPi.substring(13, 13);
  String stringState = String(StringFromPi.charAt(13));
  fromPi_State = stringState.toInt();

  fromPi_posJ1 = stringJ1.toInt();
  fromPi_posJ2 = stringJ2.toInt();
  fromPi_posZ = stringZ.toInt();

  pr_place.j1 = stringJ1.toInt();
  pr_place.j2 = stringJ2.toInt();
  pr_place.z = stringZ.toInt();

  if(pr_place.j1 == 0)
    pr_place.j1 = pr_home.j1;
  if(pr_place.j2 == 0)
    pr_place.j2 = pr_home.j2;
  if(pr_place.z == 0)
    pr_place.z = pr_home.z;

  if (stringMode == "0"){
    fromPi_Mode = false;
    STATE = S_MANUAL;
  }
  else if (stringMode == "1"){
    fromPi_Mode = true;
    STATE = S_AUTOMATIC;
  }
  else{
    LED_DEBUG(2);
    error = true;
  }

  //STATE = S_AUTOMATIC;
  
  switch (fromPi_State) {
    case 0:
      if(STATE == S_AUTOMATIC){
        fromPi_auto_startSequence = true;
        fromPi_auto_resetSequence = false;
        digitalWrite(LED1_PIN, HIGH);
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
        digitalWrite(LED2_PIN, HIGH);
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

  /*int firstIndexDelimiter = StringFromPi.indexOf('|');
  motorAngleShoulder = StringFromPi.substring(0, firstIndexDelimiter);
  pr_place.j1 = motorAngleShoulder.toInt();

  int lastIndexDelimiter = StringFromPi.lastIndexOf('|');
  motorAngleElbow = StringFromPi.substring(firstIndexDelimiter+1, lastIndexDelimiter);
  pr_place.j1 = motorAngleElbow.toInt();*/

  //pr_place.j1 = fromPi_posJ1;
  //pr_place.j2 = fromPi_posJ2;
  //pr_place.z  = fromPi_posZ;

  return;
}

void LED_DEBUG(int caseNumber){
  /*bool LED1 = caseNumber % 1;
  bool LED2 = caseNumber % 2;
  bool LED3 = caseNumber % 4;
  bool LED4 = caseNumber % 8;
  bool LED5 = caseNumber % 16;
  digitalWrite(LED1_PIN, LED1);
  digitalWrite(LED2_PIN, LED2);
  digitalWrite(LED3_PIN, LED3);
  digitalWrite(LED4_PIN, LED4);
  digitalWrite(LED5_PIN, LED5);*/

  if(caseNumber % 1 >= 0)
    digitalWrite(LED1_PIN, HIGH);
  else
    digitalWrite(LED1_PIN, LOW);
  if(caseNumber % 2 >= 0)
    digitalWrite(LED2_PIN, HIGH);
  else
    digitalWrite(LED2_PIN, LOW);
  if(caseNumber % 4 >= 0)
    digitalWrite(LED3_PIN, HIGH);
  else
    digitalWrite(LED3_PIN, LOW);
  if(caseNumber % 8 >= 0)
    digitalWrite(LED4_PIN, HIGH);
  else
    digitalWrite(LED4_PIN, LOW);
  if(caseNumber % 16 >= 0)
    digitalWrite(LED5_PIN, HIGH);
  else
    digitalWrite(LED5_PIN, LOW);

}

void PWMDebug(int Step){
  analogWrite(PIN_DEBUG, 25*Step);
}

bool IsAtPosition(int MotorID, int EndPos, int Treshold)
{
  return (ServoMotor.getPresentPosition(MotorID) >= (EndPos-Treshold)) && (ServoMotor.getPresentPosition(MotorID) <= (EndPos+Treshold));
}
