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
#define Serial2 Serial2
#define DEBUG_SERIAL Serial

//Servos

//DcMotor

//Carte OpenCR
#define BDPIN_PUSH_SW_1         34
#define BDPIN_PUSH_SW_2         35

#define ENCA                    2
#define ENCB                    4

#define PIN_EMAGNET A1      // TODO: mettre la bonne valeur
#define PIN_LIMITSWITCH A2  // TODO: mettre la bonne valeur

#define HOME_POS_J1 0       // TODO: hardcoder la valeur
#define HOME_POS_J2 0       // TODO: hardcoder la valeur
#define HOME_POS_Z  0       // TODO: hardcoder la valeur
#define PICK_POS_J1 0       // TODO: hardcoder la valeur
#define PICK_POS_J2 0       // TODO: hardcoder la valeur
#define PICK_POS_Z  0       // TODO: hardcoder la valeur

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
               SM_GO_DOWN,
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
void LowerEOAT();
void RaiseEOAT();
void RestingEOAT();
bool IsLimitSwitchActivated();
void ActivateMagnet();
void DeactivateMagnet();

/*---------------------------- VARIABLES DEFINITIONS --------------------------*/

int  fromPi_posJ1 = 0;
int  fromPi_posJ2 = 0;
int  fromPi_posZ = 0;
bool fromPi_manual = true;
bool fromPi_automatic = false;

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

unsigned long encoder = 0;

void setup() 
{
  Serial.begin(BAUDRATE);
  pinMode(PIN_EMAGNET, OUTPUT);
  pinMode(PIN_LIMITSWITCH, INPUT);

  STATE = S_MANUAL;
  STATE_MAN = SM_IDLE;  
  STATE_AUTO = SA_GO_TO_HOME;
}

/*---------------------------- LOOP FUNCTION ----------------------------------*/

void loop() 
{

  pr_place.j1 = fromPi_posJ1;
  pr_place.j2 = fromPi_posJ2;
  pr_place.z  = fromPi_posZ;

  switch (STATE)
  {
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
            STATE_MAN = SM_GO_DOWN;
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

          GoToPosition(pr_home);
          if (true)                             // TODO: condition d'arrivé à home
          {
            STATE_MAN = SM_IDLE;
          }
          break;

        case SM_GO_TO_PICK:

          GoToPosition(pr_pick);
          if (true)                             // TODO: condition d'arrivé à pick
          {
            STATE_MAN = SM_IDLE;
          }
          break;

        case SM_GO_TO_PLACE:

          GoToPosition(pr_place);
          if (true)                             // TODO: condition d'arrivé à place
          {
            STATE_MAN = SM_IDLE;
          }
          break;

        case SM_GO_DOWN:

          LowerEOAT();
          if (encoder >= pr_place.z)
          {
            RestingEOAT();
            encoder = 0;
            STATE_MAN = SM_IDLE;
          }      
          break;

        case SM_GO_TO_LS:

          RaiseEOAT();
          if (IsLimitSwitchActivated())
          {
            RestingEOAT();
            STATE_MAN = SM_IDLE;
          }        
          break;

        case SM_GRIP:
          ActivateMagnet(); 
          STATE_MAN = SM_IDLE;
          break;

        case SM_DROP:
          DeactivateMagnet();
          STATE_MAN = SM_IDLE;
          break;

        default:
          STATE_MAN = SM_IDLE;
          break;
      }

      break;

    case S_AUTOMATIC:

      if (fromPi_auto_resetSequence)
      {
        STATE_AUTO = SA_IDLE;
        fromPi_auto_resetSequence = false;
      }

      switch (STATE_AUTO)
      {
        case SA_GO_TO_HOME:

          GoToPosition(pr_home);
          if (true)                             // TODO: condition d'arrivé à home
          {
            STATE_AUTO = SA_IDLE;
          }
          break;
        
        case SA_IDLE:

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
   
          GoToPosition(pr_pick);
          if (true and true)                     // TODO: condition d'arrivé ET ajouter délai avec compteur
          {
            STATE_AUTO = SA_GO_TO_PIECE;
          }
          break;

        case SA_GO_TO_PIECE:
        
          LowerEOAT();
          if (encoder >= pr_pick.z)
          {
            RestingEOAT();
            encoder = 0;
            STATE_AUTO = SA_PICK_PIECE;
          }
          break;

        case SA_PICK_PIECE:

          ActivateMagnet();
          if (true)                             // TODO: ajouter délai avec compteur
          {
            STATE_AUTO = SA_GO_TO_LS1;
          }
          break;

        case SA_GO_TO_LS1:

          RaiseEOAT();
          if (IsLimitSwitchActivated())
          {
            RestingEOAT();
            STATE_AUTO = SA_GO_TO_POS;
          }
          break;

        case SA_GO_TO_POS:
        
          GoToPosition(pr_place);
          if (true and true)                     // TODO: condition d'arrivé ET ajouter délai avec compteur
          {
            STATE_AUTO = SA_GO_TO_FLOOR;
          }
          break;

        case SA_GO_TO_FLOOR:
        
          LowerEOAT();
          if (encoder >= pr_place.z)
          {
            RestingEOAT();
            encoder = 0;
            STATE_AUTO = SA_DROP_PIECE;
          }
          break;

        case SA_DROP_PIECE:
        
          DeactivateMagnet();
          if (true)                             // TODO: ajouter délai avec compteur
          {
            STATE_AUTO = SA_GO_TO_LS2;
          }
          break;

        case SA_GO_TO_LS2:

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
  //ServoMotor.setGoalPosition(motorShoulder_ID, pr.j1); TODO
  //ServoMotor.setGoalPosition(motorElbow_ID,   pr.j2); TODO
}

void LowerEOAT()
{
  //Motor.setSpeed(1); TODO: Faire descendre l'actuateur
}

void RaiseEOAT()
{
  //Motor.setSpeed(-1); TODO: Faire monter l'actuateur
}

void RestingEOAT()
{
  //Motor.setSpeed(0); TODO: Mettre le moteur à OFF
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
