#!/usr/bin/env python


import sys
import os
import cv2
import numpy as np;
import time

from interfaceROS import Robot_properties
from std_msgs.msg import String as ROS_String
from std_msgs.msg import Int16
 
class TesterArduino:
	def __init__(self):
		self.robot = Robot_properties() #Objet contenant les infos du sub et sub (interface ROS et ici l'image IN et la position OUT


	def updater(self):

		#self.outputmessage()
		self.robot.publish(0)
		time.sleep(10)
		
		while self.robot.messageArduino == 1:#attente de l'arduino soit prete
			time.sleep(0.01)

		self.robot.publish(0)#envoie commande vide
		while self.robot.messageArduino == 1:#attente de l'arduino soit prete
			time.sleep(0.01)

		time.sleep(1)

		self.robot.publish(1)#envoi la commande de l'init
		while self.robot.messageArduino == 1:#attente de que l'arduino est termine
			time.sleep(0.01)

		time.sleep(1)

		self.robot.publish(2)#Mise en position parking
		while self.robot.messageArduino == 1:#attente de que l'arduino est termine
			time.sleep(0.01)

		time.sleep(1)

		#self.robot.publish(3)#Mise en position transport
		#while self.robot.messageArduino == 1:#attente de que l'arduino est termine
			#time.sleep(0.01)

		time.sleep(1)

		#self.robot.publish(4)#preparation photo
		#while self.robot.messageArduino == 1:#attente de que l'arduino est termine
			#time.sleep(0.01)

		time.sleep(1)

		#self.robot.publish(5)#mise en position pour prise goblet
		#while self.robot.messageArduino == 1:#attente de que l'arduino est termine
			#time.sleep(0.01)

		time.sleep(1)

		self.robot.publish(8)#Drapeau
		while self.robot.messageArduino == 1:#attente de que l'arduino est termine
			time.sleep(0.01)

		time.sleep(10)

		self.robot.publish(14)#arret de tout materiel
		while self.robot.messageArduino == 1:#attente de que l'arduino est termine
			time.sleep(0.01)

		time.sleep(20)
	
	def outputmessage(self):
		Msg = ROS_String
		self.robot.publish(Msg)

	
	



