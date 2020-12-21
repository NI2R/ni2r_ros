#ifndef TIRETTE_ACTION
#define TIRETTE_ACTION

#include "Arduino.h"
#include "Setup.h"

class Tirette{
  public:
    Tirette();
    int GetCote();
    int GetTirette(); 
      
  private:
    static int TIRETTE;
    static int COTE;
    static int stateCote; 
    static int stateTirette; 
  
};
#endif
