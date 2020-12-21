#ifndef FOREARM_ACTION
#define FOREARM_ACTION

#include "Arduino.h"
#include <DynamixelSerial.h>
#include "Setup.h"

class ForeArm
{
public:
	ForeArm();
	void MoveTo(double);//MoveTo
  void MoveAndWait(double);
  void InitDynamixel();
  void PosiNeutre();
  void PosiMax();
  void PosiMin();
  void PosiDepose();
  int Position();
  void Transport();
  void PosiRecup(double);

  

  //////////////// A retirer////////////
  void DeploiementSaisieFloor();
  void DeploiementDrop();
  void ParquetG();
  void ParquetD();
  void BrasTransport();
  void DeploiementSaisieWall();
  void DeploiementOutWall();

};
#endif
