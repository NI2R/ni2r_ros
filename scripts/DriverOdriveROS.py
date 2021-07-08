#!/usr/bin/env python
# -*-coding:Latin-1 -*
from __future__ import print_function
import rospy

from time import sleep
import DriverOdrive

from std_msgs.msg import Float32, Bool

class Robot_properties:
	def __init__(self):
		self.start = False
		self.stop_timer = False
		self.Initialisation = False

		rospy.Subscriber("StateTirette", Bool, self.UpdateStart)
		rospy.Subscriber("stop_timer", Bool, self.UpdateStop)
		rospy.Subscriber("StateClef", Bool, self.UpdateKey)

	def UpdateStart(self, data):
		self.start = data.data

	def UpdateStop(self, data):
		self.stop_timer = data.data

	def UpdateKey(self, data):
		self.Initialisation = data.data

def main():

	rospy.init_node('DriverOdrive', anonymous=True)
	robot = Robot_properties()

	while(not(robot.Initialisation)):
		sleep(0.1)

	odrv0 = DriverOdrive.odrive.find_any()
	Moteurs = DriverOdrive.Odrive(robot, odrv0)
	print("========== Start homologation 2021 =========")
	Moteurs.Setup()

	while(not(robot.start)):
		sleep(0.1)
		# rospy.sleep(1)

	print("========== MARCHE AVANT =========")
	initial_dist = 566
	while(initial_dist - Moteurs.Rounds_To_Length(Moteurs.motor1.encoder.pos_estimate) > 10):
		if(not(Moteurs.check_need_to_break())):
			dist = initial_dist - Moteurs.Rounds_To_Length(Moteurs.motor1.encoder.pos_estimate)
			print(dist)
			Moteurs.Translation(dist)
		else:
			sleep(0.2)

	print("========== MARCHE ARRIERE =========")
	initial_dist = -250
	while(initial_dist - Moteurs.Rounds_To_Length(Moteurs.motor1.encoder.pos_estimate) < -10):
		if(not(Moteurs.check_need_to_break())):
			dist = initial_dist - Moteurs.Rounds_To_Length(Moteurs.motor1.encoder.pos_estimate)
			print(dist)
			Moteurs.Translation(dist)
		else:
			sleep(0.2)

	print("========== ROTATION =========")
	initial_angle = -90
	while(initial_dist - Moteurs.Rounds_To_Length(Moteurs.motor1.encoder.pos_estimate) < -10):
		if(not(Moteurs.check_need_to_break())):
			dist = initial_dist - Moteurs.Rounds_To_Length(Moteurs.motor1.encoder.pos_estimate)
			print(dist)
	Moteurs.Rotation(initial_angle)
		else:
			sleep(0.2)

	print("========== Fin de homologation 2021 =========")

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
