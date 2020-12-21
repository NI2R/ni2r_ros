#include "ForeArm.h"

ForeArm::ForeArm(){
  Dynamixel.setSerial(&Serial2); // &Serial - Arduino UNO/NANO/MICRO, &Serial1, &Serial2, &Serial3 - Arduino Mega
  Dynamixel.begin(1000000,15);  // Inicialize the servo at 1Mbps and Pin Control 2
}

void ForeArm::MoveTo(double pDX1){//, double pDX2){
	Dynamixel.move(1, pDX1);
  //Dynamixel.move(2, pDX2);
}

void ForeArm::MoveAndWait(double val){
  MoveTo(val);
  while(Dynamixel.readPosition(1)<val - 10 or Dynamixel.readPosition(1)>val + 10){
    MoveTo(val);
  }
}

void ForeArm::InitDynamixel(){ //val a définir pour le départ
  MoveAndWait(511);
}

void ForeArm::PosiNeutre(){
  MoveAndWait(511);
}

void ForeArm::PosiMax(){
  MoveAndWait(1023);
}

void ForeArm::PosiMin(){
  MoveAndWait(0);
}

void ForeArm::PosiDepose(){
  MoveAndWait(400);
}

int ForeArm::Position(){
  return Dynamixel.readPosition(1);
}

void ForeArm::Transport(){
  MoveAndWait(500);
}

void ForeArm::PosiRecup(double posi){
  MoveAndWait(posi);
}







//////////////// A retirer////////////

void ForeArm::DeploiementSaisieFloor(){
  MoveTo(505); 

}

void ForeArm::DeploiementDrop(){
   MoveTo(820); 
}

void ForeArm::ParquetG(){
  MoveTo(500); 
  
}

void ForeArm::ParquetD(){
  MoveTo(500);
  
}

void ForeArm::BrasTransport(){
  MoveTo(700);
  
}

void ForeArm::DeploiementSaisieWall(){
   MoveTo(820); 
}

void ForeArm::DeploiementOutWall(){
   MoveTo(820); 
}
