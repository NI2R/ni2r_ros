#include <Wire.h>

#include <ros.h>
#include <std_msgs/Bool.h>
#include <std_msgs/Int16.h>

#include <VL53L0X.h>

ros::NodeHandle  nh;

VL53L0X sensor1;
VL53L0X sensor2;
VL53L0X sensor3;
VL53L0X sensor4;
VL53L0X sensor5;
VL53L0X sensor6;
VL53L0X sensor7;
VL53L0X sensor8;

int GAR;
int GAV;
int AVD;
int DAV;
int ARG;
int AVG;
int ARD;
int DAR;

bool Tirette;
bool Clef;
bool Cote;

std_msgs::Bool TiretteStateRos;
std_msgs::Bool ClefStateRos;
std_msgs::Bool CoteStateRos;

std_msgs::Int16 GARRos;
std_msgs::Int16 GAVRos;
std_msgs::Int16 AVDRos;
std_msgs::Int16 DAVRos;
std_msgs::Int16 ARGRos;
std_msgs::Int16 AVGRos;
std_msgs::Int16 ARDRos;
std_msgs::Int16 DARRos;


ros::Publisher arduinoTirette("StateTirette", &TiretteStateRos);
ros::Publisher arduinoClef("StateClef", &ClefStateRos);
ros::Publisher arduinoCote("StateCote", &CoteStateRos);

ros::Publisher CapteurGAR("CapteurGAR", &GARRos);
ros::Publisher CapteurGAV("CapteurGAV", &GAVRos);
ros::Publisher CapteurAVD("CapteurAVD", &AVDRos);
ros::Publisher CapteurDAV("CapteurDAV", &DAVRos);
ros::Publisher CapteurARG("CapteurARG", &ARGRos);
ros::Publisher CapteurAVG("CapteurAVG", &AVGRos);
ros::Publisher CapteurARD("CapteurARD", &ARDRos);
ros::Publisher CapteurDAR("CapteurDAR", &DARRos);

void setup(){

  InitCapteur();
  InitSwitch();
  CheckCapteur();
  GetSwitchState();

  nh.initNode();
  nh.advertise(arduinoTirette);
  nh.advertise(arduinoClef);
  nh.advertise(arduinoCote);

  nh.advertise(CapteurGAR);
  nh.advertise(CapteurGAV);
  nh.advertise(CapteurAVD);
  nh.advertise(CapteurDAV);
  nh.advertise(CapteurARG);
  nh.advertise(CapteurAVG);
  nh.advertise(CapteurARD);
  nh.advertise(CapteurDAR);
      
  arduinoTirette.publish(&TiretteStateRos); 
  arduinoClef.publish(&ClefStateRos); 
  arduinoCote.publish(&CoteStateRos);

  CapteurGAR.publish(&GARRos);
  CapteurGAV.publish(&GAVRos);
  CapteurAVD.publish(&AVDRos);
  CapteurDAV.publish(&DAVRos);
  CapteurARG.publish(&ARGRos);
  CapteurAVG.publish(&AVGRos);
  CapteurARD.publish(&ARDRos);
  CapteurDAR.publish(&DARRos);

  nh.spinOnce();
//Serial.begin (9600);

}


void loop(){

  CheckCapteur();
  //AfficheCapteur();
  GetSwitchState();
  //AfficheSwitch();
//
  arduinoTirette.publish(&TiretteStateRos); 
  arduinoClef.publish(&ClefStateRos); 
  arduinoCote.publish(&CoteStateRos); 

  CapteurGAR.publish(&GARRos);
  CapteurGAV.publish(&GAVRos);
  CapteurAVD.publish(&AVDRos);
  CapteurDAV.publish(&DAVRos);
  CapteurARG.publish(&ARGRos);
  CapteurAVG.publish(&AVGRos);
  CapteurARD.publish(&ARDRos);
  CapteurDAR.publish(&DARRos);

  nh.spinOnce();


delay(50);

}

void AfficheSwitch(){

  Serial.print("Tirette : ");
  Serial.print(Tirette);
  Serial.print(" |  Clef : ");
  Serial.print(Clef);
  Serial.print(" | Cote : ");
  Serial.print(Cote);
  Serial.println("");
  
}

void GetSwitchState(){
  Tirette = digitalRead(22);
  Clef = digitalRead(24);
  Cote = digitalRead(26);

  TiretteStateRos.data = Tirette;
  ClefStateRos.data = Clef;
  CoteStateRos.data = Cote;

}

void InitSwitch(){
  pinMode(22, INPUT);//tirette
  pinMode(24, INPUT);//clef
  pinMode(26, INPUT);//cote
}

void CheckCapteur(){

  GAR=sensor1.readRangeContinuousMillimeters();
  delay(10);
  GAV=sensor2.readRangeContinuousMillimeters();
  delay(10);
  AVD=sensor3.readRangeContinuousMillimeters();
  delay(10);
  DAV=sensor4.readRangeContinuousMillimeters();
  delay(10);
  ARG=sensor5.readRangeContinuousMillimeters();
  delay(10);
  AVG=sensor6.readRangeContinuousMillimeters();
  delay(10);
  ARD=sensor7.readRangeContinuousMillimeters();
  delay(10);
  DAR=sensor8.readRangeContinuousMillimeters();
  delay(10);

  GARRos.data=GAR;
  GAVRos.data=GAV;
  AVDRos.data=AVD;
  DAVRos.data=DAV;
  ARGRos.data=ARG;
  AVGRos.data=AVG;
  ARDRos.data=ARD;
  DARRos.data=DAR;
 
  
}

void InitCapteur(){

  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  
  delay(50);
  
  Wire.begin();
  
  digitalWrite(8, HIGH);
  delay(150);
  sensor1.init(true);
  delay(100);
  sensor1.setAddress((uint8_t)01);
  
  digitalWrite(9, HIGH);
  delay(150);
  sensor2.init(true);
  delay(100);
  sensor2.setAddress((uint8_t)02);
  
  digitalWrite(10, HIGH);
  delay(150);
  sensor3.init(true);
  delay(100);
  sensor3.setAddress((uint8_t)03);
  
  digitalWrite(11, HIGH);
  delay(150);
  sensor4.init(true);
  delay(100);
  sensor4.setAddress((uint8_t)04);
  
  digitalWrite(4, HIGH);
  delay(150);
  sensor5.init(true);
  delay(100);
  sensor5.setAddress((uint8_t)05);
  
  digitalWrite(5, HIGH);
  delay(150);
  sensor6.init(true);
  delay(100);
  sensor6.setAddress((uint8_t)06);
  
  digitalWrite(2, HIGH);
  delay(150);
  sensor7.init(true);
  delay(100);
  sensor7.setAddress((uint8_t)07);
  
  digitalWrite(3, HIGH);
  delay(150);
  sensor8.init(true);
  delay(100);
  sensor8.setAddress((uint8_t)10);
  
  sensor1.startContinuous();
  sensor2.startContinuous();
  sensor3.startContinuous();
  sensor4.startContinuous();
  sensor5.startContinuous();
  sensor6.startContinuous();
  sensor7.startContinuous();
  sensor8.startContinuous();
  
}

void AfficheCapteur(){

  Serial.print(" C GAR : ");
  Serial.print(GAR);
  
  Serial.print(" / C GAV : ");
  Serial.print(GAV);
  
  Serial.print(" / C AVD : ");
  Serial.print(AVD);
  
  Serial.print(" / C DAV : ");
  Serial.print(DAV);
  
  Serial.print(" / C ARG : ");
  Serial.print(ARG);
  
  Serial.print(" / C AVG : ");
  Serial.print(AVG);
  
  Serial.print(" / C ARD: ");
  Serial.print(ARD);
  
  Serial.print(" / C DAR : ");
  Serial.print(DAR);
  
  Serial.println("");
  
}
