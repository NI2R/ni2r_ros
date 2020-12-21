#ifndef DRAPEAU_ACTION
#define DRAPEAU_ACTION

#include "Arduino.h"
#include <DynamixelSerial.h>
#include "Setup.h"

class Drapeau
{
public:
	Drapeau();
	void MoveTo(double);//MoveTo
  void MoveAndWait(double);
  void InFlag();
  void OutFlag();
};
#endif
