#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/UInt16.h>
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
//Tirette TiretteRobot; 
Drapeau DrapeauAction;
Manche MancheAction;

ros::NodeHandle node_handle;

std_msgs::String Out_msg;
std_msgs::String Order_msg;
geometry_msgs::Pose Posi_msg;
int posiGoblet = 5;
int couleurGoblet = 0;
int couleurCote = 2;


void subscriberOrder(const std_msgs::String& Order_msg) {
  //posiGoblet = 0;
  String message = Order_msg.data;
  message.c_str();
  traitementMessage(message);

}

void subscriberPosi(const geometry_msgs::Pose& Posi_msg) {
  posiGoblet = Posi_msg.position.x;
  if (posiGoblet > 500){
      traitementMessage("test");
  }else{
      traitementMessage("");
  }
  delay(1000);
  //posiGoblet = Posi_msg.position.x;
  //couleurGoblet = Posi_msg.position.y;

}

ros::Publisher out_publisher("arduinoState", &Out_msg);
ros::Subscriber<std_msgs::String> order_subscriber("arduinoAction", &subscriberOrder);
ros::Subscriber<geometry_msgs::Pose> posi_subscriber("positionGoblet", &subscriberPosi);

void setup()
{  
  pinMode(LED_BUILTIN, OUTPUT);
  node_handle.initNode();
  node_handle.advertise(out_publisher);//publish
  node_handle.subscribe(posi_subscriber);
  node_handle.subscribe(order_subscriber);

  SetupRobot.SetAll();
  //ProgTest();
  delay(1000);

  digitalWrite(LED_BUILTIN, LOW); 
  ElevatorRobot.LedON();
}

void loop()
{ 
  
  node_handle.spinOnce();

}

void publishMessage(int etat){ //permet de publier ceux que je veux vers ROS

  switch(etat){
    case 0:
      Out_msg.data = "attente ordre";
      break;
    case 1:
      Out_msg.data = "action en cours";
      break;
    case 2:
      Out_msg.data = "action terminee";
      break;
  }
  out_publisher.publish(&Out_msg);
  node_handle.spinOnce();
  
}

void traitementMessage(String message){//fonction dans laquel je dois traiter les infos reçu de ROS
  if (message  == "test") {
    digitalWrite(LED_BUILTIN, HIGH); 
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }
  
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
for(int i = 0; i<100; i++){
  for(int j = 0; j<100;j++){
      node_handle.spinOnce();
      delay(1);
  }
  ArmRobot.GetGobelet(posiGoblet,couleurGoblet,couleurCote);
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
}
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
