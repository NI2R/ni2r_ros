#include "Tirette.h"

int Tirette::TIRETTE = TIRETTEPIN;
int Tirette::COTE = COTEPIN;

int Tirette::stateCote = 0; 
int Tirette::stateTirette = 0; 

Tirette::Tirette(){
  
}

int Tirette::GetCote(){
  stateCote = digitalRead(COTE);
  return stateCote;
}

int Tirette::GetTirette(){
  stateTirette = digitalRead(TIRETTE);
  return stateTirette;
}
