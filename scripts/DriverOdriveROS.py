#!/usr/bin/env python
# -*-coding:Latin-1 -*
from __future__ import print_function
import rospy

from time import sleep
import DriverOdrive

from std_msgs.msg import Float32, Bool, Int16

class Robot_properties:
	def __init__(self):
		self.start = False
		self.stop_timer = False
		self.stop_lidar = False
		self.Initialisation = False
		self.cote = 0
		self.AduinoOrder = 0

		rospy.Subscriber("StateTirette", Bool, self.UpdateStart)
		rospy.Subscriber("stop_timer", Bool, self.UpdateStop)
		rospy.Subscriber("stop_lidar", Bool, self.UpdateStopLidar)
		rospy.Subscriber("StateClef", Bool, self.UpdateKey)
		#rospy.Subscriber("StateCote", Bool, self.UpdateCote)

		self.pub_arduino = '/arduinoOrder'
		self.pub_arduino_topic = rospy.Publisher(self.pub_arduino, Int16, queue_size=1)

	def UpdateStart(self, data):
		self.start = data.data

	def UpdateStop(self, data):
		self.stop_timer = data.data

	def UpdateStopLidar(self, data):
		self.stop_lidar = data.data

	def UpdateKey(self, data):
		self.Initialisation = data.data

	def UpdateCote(self, data):
		self.cote = data.data

	def Publish_ArduinoOrder(self,order):
		arduino_command = Int16()
		arduino_command_raise_flag = order
		arduino_command.data = arduino_command_raise_flag
		self.pub_arduino_topic.publish(arduino_command)

def main():

	rospy.init_node('DriverOdrive', anonymous=True)
	robot = Robot_properties()

	"""Mode match = standby"""
	#while not(robot.Initialisation): 
		#sleep(0.1)
	odrv0 = DriverOdrive.odrive.find_any()
	Moteurs = DriverOdrive.Odrive(robot, odrv0)
	print("========= Start Match =========")
	Moteurs.Setup()
	
	if robot.cote:
		print("**** COTE JAUNE ****")
	elif not(robot.cote):
		print("**** COTE BLEU ****")
	else :
		print("COTE EXCEPTION")


	while(not(robot.start)):
		sleep(0.1)
		# rospy.sleep(1)

	Moteurs.enable_lidar = False
	print("========= MARCHE AVANT =========")
	Moteurs.Translation_with_breaking(566)

	print("========= MARCHE ARRIERE =========")
	Moteurs.Translation_with_breaking(-1680)

	#Moteurs.enable_lidar = True  retirer pour la coupe polytech
	print("========= ROTATION =========")
	Moteurs.Rotation_with_breaking(-90)
	
	if not(robot.cote): 
		# COTE BLEU (0 = entre dans la boucle)
		print("========= MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(120)

		print("========= SORTIR LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(9)
		sleep(2)	
		
		print("========= MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-620)
		
		print("========= RENTRER LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(10)
		sleep(2)	

		print("========= ROTATION =========")
		Moteurs.Rotation_with_breaking(45)

		print("========= MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(425) # 850

		print("========= ROTATION =========")
		Moteurs.Rotation_with_breaking(-45)

		print("========= MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(500)

		print("========= DIODE  =========")
		robot.Publish_ArduinoOrder(4)
		sleep(2)

		print("========= MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-50)

		print("========= PHOTO PLACEMENT =========")
		robot.Publish_ArduinoOrder(5)
		sleep(0.5)

		print("========= ASPIRATION =========")
		robot.Publish_ArduinoOrder(6)
		sleep(0.5)

		print("========= MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(50)

		print("========= LEVER =========")
		robot.Publish_ArduinoOrder(8)
		sleep(1)

		print("========= LEVER 2 =========")
		robot.Publish_ArduinoOrder(8)
		sleep(1)

		print("========= MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-100)

		print("========= MID =========")
		robot.Publish_ArduinoOrder(3)
		sleep(1)

		print("========= ROTATION =========")
		Moteurs.Rotation_with_breaking(90)

		print("========= MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(370)

		print("========= DROP =========")
		robot.Publish_ArduinoOrder(11)
		sleep(1)

		print("========= RELAESE ALL =========")
		robot.Publish_ArduinoOrder(14)
		sleep(0.5)

		print("========= RELAESE ALL =========")
		robot.Publish_ArduinoOrder(14)
		sleep(0.5)


	else:
		# COTE JAUNE
		print("========= MARCHE ARRIERE =========*****")
		Moteurs.Translation_with_breaking(-120)

		print("========= SORTIR LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(9)
		sleep(2)	

		print("========= MARCHE AVANT =========*****")
		Moteurs.Translation_with_breaking(620)

		print("========= RENTRER LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(10)
		sleep(2)

		print("========= ROTATION =========")
		Moteurs.Rotation_with_breaking(-45)

		print("========= MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-850)	

	print("========= Fin de Match =========")

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
