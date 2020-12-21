#include "Pompe.h"


int Pompe::POMP1 = POMPPIN1;
int Pompe::VAN1 = VANPIN1;
int Pompe::POMP2 = POMPPIN2;
int Pompe::VAN2 = VANPIN2;
int Pompe::POMP3 = POMPPIN3;
int Pompe::VAN3 = VANPIN3;
int Pompe::POMP4 = POMPPIN4;
int Pompe::VAN4 = VANPIN4;
int Pompe::POMP5 = POMPPIN5;
int Pompe::VAN5 = VANPIN5;



//A supprimer///////////////
int Pompe::POMP = POMPPIN1;
int Pompe::VAN = VANPIN1;
////////////////////////


Pompe::Pompe(){
  
}
void Pompe::OpenAll(){
  digitalWrite(POMP1, HIGH);
  digitalWrite(VAN1, HIGH);
  digitalWrite(POMP2, HIGH);
  digitalWrite(VAN2, HIGH);
  digitalWrite(POMP3, HIGH);
  digitalWrite(VAN3, HIGH);
  digitalWrite(POMP4, HIGH);
  digitalWrite(VAN4, HIGH);
  digitalWrite(POMP5, HIGH);
  digitalWrite(VAN5, HIGH);
}

void Pompe::CloseAll(){
  digitalWrite(POMP1, LOW);
  digitalWrite(VAN1, LOW);
  digitalWrite(POMP2, LOW);
  digitalWrite(VAN2, LOW);
  digitalWrite(POMP3, LOW);
  digitalWrite(VAN3, LOW);
  digitalWrite(POMP4, LOW);
  digitalWrite(VAN4, LOW);
  digitalWrite(POMP5, LOW);
  digitalWrite(VAN5, LOW);
}

void Pompe::Open1(){
  digitalWrite(POMP1, HIGH);
  digitalWrite(VAN1, HIGH);
}

void Pompe::Close1(){
  digitalWrite(POMP1, LOW);
  digitalWrite(VAN1, LOW);
}

void Pompe::Open2(){
  digitalWrite(POMP2, HIGH);
  digitalWrite(VAN2, HIGH);
}

void Pompe::Close2(){
  digitalWrite(POMP2, LOW);
  digitalWrite(VAN2, LOW);
}

void Pompe::Open3(){
  digitalWrite(POMP3, HIGH);
  digitalWrite(VAN3, HIGH);
}

void Pompe::Close3(){
  digitalWrite(POMP3, LOW);
  digitalWrite(VAN3, LOW);
}

void Pompe::Open4(){
  digitalWrite(POMP4, HIGH);
  digitalWrite(VAN4, HIGH);
}

void Pompe::Close4(){
  digitalWrite(POMP4, LOW);
  digitalWrite(VAN4, LOW);
}

void Pompe::Open5(){
  digitalWrite(POMP5, HIGH);
  digitalWrite(VAN5, HIGH);
}

void Pompe::Close5(){
  digitalWrite(POMP5, LOW);
  digitalWrite(VAN5, LOW);
}















/////////////////////////////////// a supprimer//////////////////////////////
void Pompe::Open(){
  digitalWrite(POMP, HIGH);
  digitalWrite(VAN, HIGH);
}

void Pompe::Close(){
  digitalWrite(POMP, LOW);
  digitalWrite(VAN, LOW);
}
/////////////////////////////////////////////
