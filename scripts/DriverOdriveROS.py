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
		self.Initialisation = False
		self.cote = 0		
		self.AduinoOrder = 0

		rospy.Subscriber("StateTirette", Bool, self.UpdateStart)
		rospy.Subscriber("stop_timer", Bool, self.UpdateStop)
		rospy.Subscriber("StateClef", Bool, self.UpdateKey)
		rospy.Subscriber("StateCote", Bool, self.UpdateCote)

		self.pub_arduino = '/arduinoOrder'
		self.pub_arduino_topic = rospy.Publisher(self.pub_arduino, Int16, queue_size=1)

	def UpdateStart(self, data):
		self.start = data.data

	def UpdateStop(self, data):
		self.stop_timer = data.data

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
	while not(robot.Initialisation): 
		sleep(0.1)

	odrv0 = DriverOdrive.odrive.find_any()
	Moteurs = DriverOdrive.Odrive(robot, odrv0)
	print("========== Start homologation 2021 =========")
	Moteurs.Setup()

	while(not(robot.start)):
		sleep(0.1)
		# rospy.sleep(1)

	print("========== MARCHE AVANT =========")
	Moteurs.Translation_with_breaking(566)
	
	if not(robot.cote):

		print("========== MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-1100)

		print("========== ROTATION =========")
		Moteurs.Rotation_with_breaking(-90)

		print("========== MARCHE AVANT =========")
		Moteurs.Translation_with_breaking(-760)

		print("========== SORTIR LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(9)
		sleep(2)	
		
		print("========== MARCHE ARRIERE =========")
		Moteurs.Translation_with_breaking(-1400)
		
		print("========== RENTRER LA CREMAILLERE =========")
		robot.Publish_ArduinoOrder(10)
		sleep(2)
			

	print("========== Fin de homologation 2021 =========")

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
