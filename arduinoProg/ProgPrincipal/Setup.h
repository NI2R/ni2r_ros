#ifndef SETUP_ACTION
#define SETUP_ACTION

#include "Arduino.h"

//Moteur pas à pas
#define ENABLE 52 //Ok
#define DIRECTION 50 //Ok
#define IMPULL 48 //Ok
#define PUISSANCE 24 // OK

//Switch bute
#define SWITCHBUTE 33 //Ok

//Led
#define VISIONLED 22

//Pomp pin and electrovanne pin

#define POMPPIN1 46
#define VANPIN1 47
#define POMPPIN2 44
#define VANPIN2 45
#define POMPPIN3 42
#define VANPIN3 43
#define POMPPIN4 40
#define VANPIN4 41
#define POMPPIN5 38
#define VANPIN5 39

//PIN BOUTTON
#define COTEPIN 44
#define TIRETTEPIN 35

//PIN CAPTEUR DE PRESSION
#define CAPTEURPREPIN A1



class Setup{
  public:
    Setup();
    void SetElevator();
    void SetPomp();
    void SetTirette(); 
    void SetCapPression();
    void SetAll();
  
};
#endif
