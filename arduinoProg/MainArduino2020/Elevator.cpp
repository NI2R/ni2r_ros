#include "Elevator.h"

int Elevator::NbTick = 0;

int Elevator::Position = 0;

int Elevator::ENA = ENABLE;
int Elevator::DIR = DIRECTION;
int Elevator::PUL = IMPULL;
int Elevator::SWT = SWITCHBUTE;
int Elevator::PUI = PUISSANCE;
int Elevator::LED = VISIONLED;

const int Elevator::etage[] = {1652,1270,1010,748,490,236,50,0};



Elevator::Elevator(){
  
}

void Elevator::Setup(){

  digitalWrite(ENA, LOW);
  digitalWrite(DIR, LOW);
  digitalWrite(PUL, LOW);
  digitalWrite(PUI, LOW);
  digitalWrite(LED, LOW);
  
}
void Elevator::PuissanceON(){

  digitalWrite(PUI, HIGH);
  //digitalWrite(ENA, HIGH);
  //digitalWrite(DIR, HIGH);
  digitalWrite(PUL, HIGH);

}

void Elevator::PuissanceOFF(){

  digitalWrite(PUI, LOW);
  
}

void Elevator::LedON(){

  digitalWrite(LED, HIGH);
  
}

void Elevator::LedOFF(){

  digitalWrite(LED, LOW);
  
}

void Elevator::Move(int nbTick, bool sens){ //OK
  digitalWrite(ENA, HIGH);
  digitalWrite(DIR,sens); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < nbTick; x++) {
    digitalWrite(PUL,HIGH); 
    delayMicroseconds(600); 
    digitalWrite(PUL,LOW); 
    delayMicroseconds(600); 
  } 
}

void Elevator::InitialPosition(){ //OK
  PuissanceON();
  bool switchState = digitalRead(SWT);
  digitalWrite(ENA, HIGH);
  digitalWrite(DIR,LOW); // Enables the motor to move in a particular direction
  while(switchState == true){
    digitalWrite(PUL,HIGH); 
    delayMicroseconds(600); 
    digitalWrite(PUL,LOW); 
    delayMicroseconds(600); 
    switchState = digitalRead(SWT);
   }
   Position = 0;
}

int Elevator::getPosition(){ //OK
  return Position;
}

void Elevator::MoveTo(int destination){ //OK
  if (Position > destination){
    Move(Position-destination, LOW);
    Position = destination;
  }
  if (Position < destination){
    Move(destination-Position, HIGH);
    Position = destination;
  }
}

void Elevator::Transport(){
  MoveTo(400);
}

void Elevator::GetGobelet(){
  MoveTo(800);
}

void Elevator::DegageGobelet(){
  MoveTo(200);
}

void Elevator::OutGobelet(){
  MoveTo(1200);
}

void Elevator::PosiManche(){
  MoveTo(500);
}

void Elevator::PosiStart(){
  MoveTo(200);
}








//////////////// A retirer////////////

void Elevator::GoToFloor(int floorNb){
  switch(floorNb){
    case 0:
       MoveTo(1600);
       delay(500);
       MoveTo(etage[0]);
    break;
    case 1:
       MoveTo(etage[1]);
    break;
    case 2:
       MoveTo(etage[2]);
    break;
    case 3:
       MoveTo(etage[3]);
    break;
    case 4:
       MoveTo(etage[4]);
    break;
    case 5:
       MoveTo(etage[5]);
    break;
      case 6:
       MoveTo(etage[6]);
    break;
      case 7:
       MoveTo(etage[7]);
    break;
  }
}

void Elevator::GoOut(int floorNb){
  GoToFloor(floorNb+1);
}

void Elevator::GetPaletFloor(){
  GoToFloor(0);
}

void Elevator::GetOutPalet(){
 MoveTo(1200);
}

void Elevator::GetPaletWall(){
 MoveTo(1500);
}

void Elevator::GetOutPaletWall(){
 MoveTo(800);
}

void Elevator::WaitGoToFloor(int floorNb){
  while(NbTick < etage[floorNb]-50 or NbTick > etage[floorNb]-50){
    delay(5);
  }
}
