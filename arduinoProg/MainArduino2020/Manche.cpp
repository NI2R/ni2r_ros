#include "Manche.h"

Manche::Manche(){
  Dynamixel.setSerial(&Serial2); // &Serial - Arduino UNO/NANO/MICRO, &Serial1, &Serial2, &Serial3 - Arduino Mega
  Dynamixel.begin(1000000,15);  // Inicialize the servo at 1Mbps and Pin Control 2
}

void Manche::MoveTo(double pDX1){
	Dynamixel.move(2, pDX1);
}

void Manche::MoveAndWait(double val){
  MoveTo(val);
  while(Dynamixel.readPosition(2)<val - 10 or Dynamixel.readPosition(2)>val + 10){
    MoveTo(val);
  }
}

void Manche::In(){ //val a définir pour le départ
  MoveAndWait(1000);
}

void Manche::Out(){ //val a définir pour la fin
  MoveAndWait(0);
}
