#ifndef POMPE_ACTION
#define POMPE_ACTION

#include "Arduino.h"
#include "Setup.h"


class Pompe{
  public:
  Pompe();
  void OpenAll();
  void CloseAll();
  void Open1();
  void Close1();
  void Open2();
  void Close2();
  void Open3();
  void Close3();
  void Open4();
  void Close4();
  void Open5();
  void Close5();


  //////////////////A SUPPRIMER////////////////////
  void Open();
  void Close();
  /////////////////////////////////////////////////


  private:
  static int POMP1;
  static int VAN1;
  static int POMP2;
  static int VAN2;
  static int POMP3;
  static int VAN3;
  static int POMP4;
  static int VAN4;
  static int POMP5;
  static int VAN5;



  /////////////////A SUPPRIMER////////////////////
  static int POMP;
  static int VAN;
  /////////////////////////////////////////////////
 
};
#endif
