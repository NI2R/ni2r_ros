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

	print("========= PART1: 1/1.MARCHE AVANT =========")
	Moteurs.enable_lidar = False
	Moteurs.Translation_with_breaking(566)

	print("========= PART2: 1/6.MARCHE ARRIERE =========")
	Moteurs.Translation_with_breaking(-350)
	Moteurs.enable_lidar = True
	Moteurs.Translation_with_breaking(-1330) # Total is 1680

	print("========= PART2: 2/6.ROTATION =========")
	Moteurs.Rotation_with_breaking(-90)
	
	if not(robot.cote): 
		# COTE BLEU (0 = entre dans la boucle)
		print("========= PART2: 3/6.MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(120)

		print("========= PART2: 4/6.SORTIR LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(9)
		sleep(2)	
		
		print("========= PART2: 5/6.MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-620)
		
		print("========= PART2: 6/6.RENTRER LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(10)
		sleep(2)

		print("========= PART3: 1/10.ROTATION =========")
		Moteurs.Rotation_with_breaking(45)

		print("========= PART3: 2/10.MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(425)

		print("========= PART3: 3/10.ROTATION =========")
		Moteurs.Rotation_with_breaking(-45)

		print("========= PART3: 4/10.MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(500)

		print("========= PART3: 5/10.DIODE  =========")
		robot.Publish_ArduinoOrder(4)
		sleep(2)

		print("========= PART3: 6/10.MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-50)

		print("========= PART3: 7/10.PHOTO PLACEMENT =========")
		robot.Publish_ArduinoOrder(5)
		sleep(0.5)

		print("========= PART3: 8/10.ASPIRATION =========")
		robot.Publish_ArduinoOrder(6)
		sleep(0.5)

		print("========= PART3: 9/10.MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(50)

		print("========= PART3: 10/10.LEVER =========")
		robot.Publish_ArduinoOrder(3)
		sleep(1)

		print("========= PART4: 1/5.MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-100)

		print("========= PART4: 2/5.ROTATION =========")
		Moteurs.Rotation_with_breaking(90)

		print("========= PART4: 3/5.MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(370)

		print("========= PART4: 4/5.DROP =========")
		robot.Publish_ArduinoOrder(11)
		sleep(2)

		print("========= PART4: 5/5.RELEASE ALL =========")
		robot.Publish_ArduinoOrder(14)
		sleep(0.5)

	else:
		# COTE JAUNE
		print("========= PART2: 3/6.MARCHE ARRIERE =========*****")
		Moteurs.Translation_with_breaking(-120)

		print("========= PART2: 4/6.SORTIR LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(9)
		sleep(2)	

		print("========= PART2: 5/6.MARCHE AVANT =========*****")
		Moteurs.Translation_with_breaking(620)

		print("========= PART2: 6/6.RENTRER LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(10)
		sleep(2)

		print("========= PART3: 1/10.ROTATION =========")
		Moteurs.Rotation_with_breaking(-45)

		print("========= PART3: 2/10.MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-425)	

		print("========= PART3: 3/10.ROTATION =========")
		Moteurs.Rotation_with_breaking(-135)

		print("========= PART3: 4/10.MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(500)

		print("========= PART3: 5/10.DIODE  =========")
		robot.Publish_ArduinoOrder(4)
		sleep(2)

		print("========= PART3: 6/10.MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-50)

		print("========= PART3: 7/10.PHOTO PLACEMENT =========")
		robot.Publish_ArduinoOrder(5)
		sleep(0.5)

		print("========= PART3: 8/10.ASPIRATION =========")
		robot.Publish_ArduinoOrder(6)
		sleep(0.5)

		print("========= PART3: 9/10.MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(50)

		print("========= PART3: 10/10.LEVER =========")
		robot.Publish_ArduinoOrder(3)
		sleep(1)

		print("========= PART4: 1/5.MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-100)

		print("========= PART4: 2/5.ROTATION =========")
		Moteurs.Rotation_with_breaking(-90)

		print("========= PART4: 3/5.MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(370)

		print("========= PART4: 4/5.DROP =========")
		robot.Publish_ArduinoOrder(11)
		sleep(2)

		print("========= PART4: 5/5.RELEASE ALL =========")
		robot.Publish_ArduinoOrder(14)
		sleep(0.5)

	print("========= Fin de Match =========")

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
