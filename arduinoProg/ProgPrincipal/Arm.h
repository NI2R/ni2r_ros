#ifndef ARM_ACTION
#define ARM_ACTION

#include "Arduino.h"
#include "Setup.h"
#include "ForeArm.h"
#include "Elevator.h"
#include "Pompe.h"

class Arm{
  public:
  Arm();
 void SetArm();
 void InitArm();
 void Parking();
 void Transport();
 void GetGobelet(int,int,int);


  private:
  ForeArm ForeArmAction;
  Setup SetupRobot;
  Elevator ElevatorRobot;
  Pompe PompeRobot;

 
};
#endif
