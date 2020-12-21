#include "Setup.h"

Setup::Setup(){
  
}

void Setup::SetElevator(){
  pinMode(ENABLE, OUTPUT);
  pinMode(DIRECTION, OUTPUT);
  pinMode(IMPULL, OUTPUT);

  pinMode(PUISSANCE, OUTPUT);

  pinMode(SWITCHBUTE, INPUT);

  pinMode(VISIONLED, OUTPUT);
}

void Setup::SetPomp(){
  pinMode(POMPPIN1, OUTPUT);
  pinMode(VANPIN1, OUTPUT);
  pinMode(POMPPIN2, OUTPUT);
  pinMode(VANPIN2, OUTPUT);
  pinMode(POMPPIN3, OUTPUT);
  pinMode(VANPIN3, OUTPUT);
  pinMode(POMPPIN4, OUTPUT);
  pinMode(VANPIN4, OUTPUT);
  pinMode(POMPPIN5, OUTPUT);
  pinMode(VANPIN5, OUTPUT);


}

void Setup::SetTirette(){
  pinMode(TIRETTEPIN, INPUT);
  pinMode(COTEPIN, INPUT);
}

void Setup::SetCapPression(){
    pinMode(CAPTEURPREPIN, INPUT);
}

void Setup::SetAll(){
  SetElevator();
  SetPomp();
  //SetTirette();
  SetCapPression();
}
