#ifndef ELEVATOR_ACTION
#define ELEVATOR_ACTION

#include "Arduino.h"
#include "Setup.h"


class Elevator{
  public:
  Elevator();
  void Setup();
  void PuissanceON();
  void PuissanceOFF();
  void LedON();
  void LedOFF();
  void Move(int, bool);
  void InitialPosition();
  int getPosition();
  void MoveTo(int);
  void Transport();
  void GetGobelet();
  void DegageGobelet();
  void OutGobelet();
  void PosiManche();
  void PosiStart();


  //////////////////A retirer/////////////////////////
 void GoToFloor(int);
 void GoOut(int);
 void GetPaletFloor();
 void GetPaletWall();
 void GetOutPalet();
 void GetOutPaletWall();
 void WaitGoToFloor(int);
////////////////////////////////////////////////////////




  private:
  static int ENA;
  static int DIR;
  static int PUL;
  static int PUI;

  static int SWT;

  static int LED;

  static int NbTick;
  static int Position;



  //////////////////A retirer/////////////////////////
  const static int etage[];
////////////////////////////////////////////////////////


  
};
#endif
