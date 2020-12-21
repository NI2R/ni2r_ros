
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Int16.h>
//#include <std_msgs/Int32.h>
#include <std_msgs/Bool.h>


#include <geometry_msgs/Pose.h>

#include "Arm.h"
#include "Drapeau.h"
#include "Manche.h"
#include "Tirette.h"

ForeArm ForeArmAction; 
Setup SetupRobot;
Elevator ElevatorRobot;
Pompe PompeRobot;
Arm ArmRobot; 
Drapeau DrapeauAction;
Manche MancheAction;


bool Tirette = false;

ros::NodeHandle  nh;

bool traitementROS = false;
bool BlueSide = false;


std_msgs::Int16 response;
std_msgs::Int16 valVision;

std_msgs::Bool TiretteStateRos;



ros::Publisher arduinoState("arduinoState", &response);

ros::Publisher arduinoTirette("StateTirette", &TiretteStateRos);


void subscriberOrder( const std_msgs::Int16 &msg){
  traitementROS = true;
  response.data = 2;
  arduinoState.publish( &response);
  nh.spinOnce();
  
  switch (msg.data) {
  case 0:
    //Aucun ordre
    break;
  case 1://Init
    ArmRobot.InitArm();
    break;
  case 2://Mise en parking
    ArmRobot.Parking();
    break;
  case 3://Mise en préparation transport
    ArmRobot.Transport();
    break;
  case 4:
    ShootPhoto();
    break;
  case 5:
    GobeletEnPosi();
    break;
  case 6:
    //GetGobelet
    break;
  case 7:
    //AlumPhare
    break;
  case 8:
    //Drapeau
        //ShootPhoto();

    DrapeauAction.OutFlag();


    break;
  case 9:
    //MancheOut
    break;
  case 10:
    //MancheIn
    break;
  case 11:
    //OutAll
    break;
  case 12:
    //Out2
    break;
  case 13:
    //Out3
    break;
  case 14://Stop tout
    ElevatorRobot.PuissanceOFF();
    ElevatorRobot.LedOFF();
    break;
  default:
    digitalWrite(22, HIGH-digitalRead(22));   // blink the led
    break;
  }
  response.data = 1;
  arduinoState.publish( &response);
  traitementROS = false;
}

void subscriberVision( const std_msgs::Int16 &msg){
  valVision = msg;
//if(msg.position.y != 2){
  digitalWrite(22, HIGH-digitalRead(22));   // blink the led
//}
}

ros::Subscriber<std_msgs::Int16> order_sub("arduinoOrder", &subscriberOrder);
//ros::Subscriber<geometry_msgs::Pose> vision_sub("positionGoblet", &subscriberVision);
ros::Subscriber<std_msgs::Int16> vision_sub("positionGoblet", &subscriberVision);


void setup()
{

  pinMode(7, INPUT);//tirette

  pinMode(22, OUTPUT);
  nh.initNode();
  
  nh.advertise(arduinoTirette);

  nh.advertise(arduinoState);

  response.data = 1;
  arduinoState.publish( &response);
  nh.spinOnce();

  response.data = 1;
  
  nh.subscribe(order_sub);
  nh.subscribe(vision_sub);

  SetupRobot.SetAll();
  DrapeauAction.InFlag();

}

void loop()
{
  if(traitementROS==false){
    response.data = 1;
    arduinoState.publish( &response);
    nh.spinOnce();
 }else{
    response.data = 2;
    arduinoState.publish( &response);
    nh.spinOnce();
 }
   Tirette = digitalRead(7);
   TiretteStateRos.data = Tirette;
   arduinoTirette.publish(&TiretteStateRos); 
   nh.spinOnce();



  
//  arduinoState.publish( &response);
//  nh.spinOnce();
//  response.data = 1;

  delay(100);
}

void ShootPhoto(){
  ElevatorRobot.LedON();
  ElevatorRobot.GetGobelet();
  delay(500);
  ForeArmAction.PosiNeutre();
  delay(500);
}

void GobeletEnPosi(){
  //nh.spinOnce();
  int ValGobletVision = valVision.data; 
  ArmRobot.GetGobelet(900,true,BlueSide);
//  if(ValGobletVision > 2000){
//      ArmRobot.GetGobelet(900,true,BlueSide);
//  }else if(ValGobletVision < 2000 and ValGobletVision > 1000){
//      ArmRobot.GetGobelet(900,false,BlueSide);
//  }
  
}











void ProgTest(){
  //Serial.println("test");
//Elevator à garder (valide)
//ElevatorRobot.Setup();  
//ElevatorRobot.LedON();
//delay(3000);  
//ElevatorRobot.LedOFF();  
//ElevatorRobot.PuissanceON();
//ElevatorRobot.InitialPosition();
//ElevatorRobot.Move(400,1);
//Serial.println(ElevatorRobot.getPosition());
//ElevatorRobot.MoveTo(1200);
//ElevatorRobot.Transport();
//ElevatorRobot.GetGobelet();
//Serial.println(ElevatorRobot.getPosition());
//ElevatorRobot.DegageGobelet();
//Serial.println(ElevatorRobot.getPosition());
//ElevatorRobot.OutGobelet();
//Serial.println(ElevatorRobot.getPosition());
//ElevatorRobot.PosiManche();
//Serial.println(ElevatorRobot.getPosition());
//ElevatorRobot.PosiStart();
//Serial.println(ElevatorRobot.getPosition());
//ElevatorRobot.PuissanceOFF();

//FOREARM à garder (valide)
//ForeArmAction.MoveTo(300);
//delay(1000);
//Serial.println(Dynamixel.readPosition(1));
//ForeArmAction.MoveAndWait(0);
//ForeArmAction.InitDynamixel();
//ForeArmAction.PosiNeutre();
//ForeArmAction.PosiMin();
//ForeArmAction.PosiMax();
//ForeArmAction.PosiDepose();
//Serial.println(ForeArmAction.Position());
//ForeArmAction.Transport();
//ForeArmAction.PosiRecup(500);//Mettre ici en paramêtre la position du goblet récupéré sur ROS

//POMPE à garder (valide) pin 4 à 13
//PompeRobot.OpenAll();
//delay(2000);
//PompeRobot.CloseAll();
//PompeRobot.Open1();
//PompeRobot.Open2();
//PompeRobot.Open3();
//PompeRobot.Open4();
//PompeRobot.Open5();
//delay(100);
//PompeRobot.Close1();
//PompeRobot.Close2();
//PompeRobot.Close3();
//PompeRobot.Close4();
//PompeRobot.Close5();


/////////ARM
//ArmRobot.Parking();
ArmRobot.InitArm();
delay(500);
ArmRobot.Transport();



delay(1000);
ElevatorRobot.GetGobelet();
delay(1000);
ForeArmAction.PosiNeutre();
delay(1000);
ElevatorRobot.LedON();
delay(500);
//ArmRobot.GetGobelet(posiGoblet,0);

  //ArmRobot.GetGobelet(posiGoblet,couleurGoblet,couleurCote);
//  if(posiGoblet =! 0){
//    ElevatorRobot.LedOFF();
//    delay(10);
//    ElevatorRobot.LedON();
//    ElevatorRobot.LedOFF();
//    delay(10);
//    ElevatorRobot.LedON();
//    ElevatorRobot.LedOFF();
//    delay(10);
//    ElevatorRobot.LedON();
//    ElevatorRobot.LedOFF();
//    delay(10);
//    ElevatorRobot.LedON();
//  }
  delay(500);

//ElevatorRobot.LedOFF();
delay(5000);
ElevatorRobot.PuissanceOFF();
//delay(5000);
ElevatorRobot.LedOFF();

//OPTION A AJOUTER
//Serial.println(Dynamixel.readPosition(1));
//Dynamixel.setEndless (1, OFF); //active la rotation complète
//Dynamixel.turn(1,1,1023); //règle la vitesse


//DRAPEAU à garder (valide)
  //Dynamixel.setTempLimit(4,80);  // Set Max Temperature to 80 Celcius
  //Dynamixel.setVoltageLimit(4,65,160);  // Set Operating Voltage from 6.5v to 16v
  //Dynamixel.setMaxTorque(4,512); 
//DrapeauAction.MoveTo(70);
//DrapeauAction.InFlag();
//DrapeauAction.OutFlag();


//Manche à garder (valide)
//MancheAction.MoveTo(0);
//MancheAction.Out();
//delay(2000);
//MancheAction.In();


    
 //////////////////////////////////////   Serial.println("fin test");
 // ArmRobot.InitArm();
//  delay(2000);
//  ForeArmAction.DeploiementSaisieFloor();
//  DoorAction.OpenAll();
//  ElevatorRobot.GetPaletFloor();
//  ElevatorRobot.WaitGoToFloor(0);
//  PompeRobot.Open();
//  delay(2000);
//  ArmRobot.CoupBrasJaune();
//  delay(1000);
//  ForeArmAction.DeploiementSaisieFloor();
//  //delay(1000);
//  //PompeRobot.Open();
//  delay(2000);
//  ElevatorRobot.GoToFloor(6);
//  //delay(500);
//  ForeArmAction.ParquetG();
//  //ForeArmAction.DeploiementSaisieWall();
//  delay(5000);
  //PompeRobot.Close();

  //ForeArmAction.DeploiementSaisieFloor();
  //ForeArmAction.DeploiementDrop();
  //ForeArmAction.DeploiementSaisieWall();
  //ForeArmAction.ParquetG();
  //ForeArmAction.ParquetD();
//
//  //ArmRobot.Transport();
//  for(int i = 0; i<5; i++){
//        ArmRobot.PreTakePaletWall();
//        //Serial.flush();
//        delay(100);
//        ArmRobot.TakePaletWall();
//        //Serial.flush();
//        delay(100);
//        ArmRobot.PostTakePaletWall();
//  }
//  for(int i = 0; i<7; i++){
//        ArmRobot.PreOutPaletWall();
//        //Serial.flush();
//        delay(100);
//        ArmRobot.OutPaletWall();
//        //Serial.flush();
//        delay(100);
//        ArmRobot.PostOutPaletWall();
//  }
  

  //delay(50000000);
}
