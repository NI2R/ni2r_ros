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

		rospy.Subscriber("StateTirette", Bool, self.UpdateStart)
		rospy.Subscriber("stop_timer", Bool, self.UpdateStop)

	def UpdateStart(self, data):
		self.start = data.data

	def UpdateStop(self, data):
		self.stop_timer = data.data


def main():
	rospy.init_node('DriverOdrive', anonymous=True)
	robot = Robot_properties()

	odrv0 = DriverOdrive.odrive.find_any()
	Moteurs = DriverOdrive.Odrive(robot, odrv0)
	print("========== Start homologation 2021 =========")
	Moteurs.Setup()

	dist = 1000000
	while(not(robot.start)):
		sleep(0.1)
		# rospy.sleep(1)

	print("========== TRANSLATION =========")
	Moteurs.Translation(dist)

	# print("========== Fin de homologation 2021 =========")

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass