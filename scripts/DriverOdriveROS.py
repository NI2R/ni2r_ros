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

		rospy.Subscriber("Start_time", Bool, self.UpdateStart)

	def UpdateStart(self, data):
		self.start = data.data


def main():
	rospy.init_node('DriverOdrive', anonymous=True)

	wheel_diameter = 80 #mm
	robot_entreaxe = 275.0 #mm
	odrv0 = odrive.find_any()
	Moteurs = Odrive(odrv0, wheel_diameter, robot_entreaxe)
	print("========== Start homologation 2021 =========")
	Moteurs.Setup()

	print("========== TRANSLATION =========")
	dist = 1000
	while(not(self.start)):
		sleep(0.1)
		# rospy.sleep(1)
	Moteurs.Translation(dist)

	print("========== Fin de homologation 2021 =========")

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
