#include "Drapeau.h"

Drapeau::Drapeau(){
  Dynamixel.setSerial(&Serial2); // &Serial - Arduino UNO/NANO/MICRO, &Serial1, &Serial2, &Serial3 - Arduino Mega
  Dynamixel.begin(1000000,15);  // Inicialize the servo at 1Mbps and Pin Control 2
}

void Drapeau::MoveTo(double pDX1){
	Dynamixel.move(4, pDX1);
}

void Drapeau::MoveAndWait(double val){
  MoveTo(val);
  while(Dynamixel.readPosition(4)<val - 10 or Dynamixel.readPosition(4)>val + 10){
    MoveTo(val);
  }
}

void Drapeau::InFlag(){ //val a définir pour le départ
  MoveAndWait(70);
}

void Drapeau::OutFlag(){ //val a définir pour la fin
  MoveAndWait(950);
}
