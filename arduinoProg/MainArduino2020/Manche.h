#ifndef MANCHE_ACTION
#define MANCHE_ACTION

#include "Arduino.h"
#include <DynamixelSerial.h>
#include "Setup.h"

class Manche
{
public:
	Manche();
	void MoveTo(double);//MoveTo
  void MoveAndWait(double);
  void In();
  void Out();
};
#endif
