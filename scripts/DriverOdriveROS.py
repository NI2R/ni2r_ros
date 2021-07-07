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

	while(not(robot.start)):
		sleep(0.1)
		# rospy.sleep(1)
	
	current_translation = lambda: Moteurs.Rounds_To_Length(Moteurs.motor1.encoder.pos_estimate)
	current_rotation = lambda: Moteurs.Rounds_To_Angle(Moteurs.motor1.encoder.pos_estimate)

	while(True):
		print("========== TRANSLATION =========")
		goal_translation = 1000 + current_translation() # 1m + initial current position
		while(goal_translation - current_translation() > 10):
			if(not(Moteurs.check_need_to_break())):
				remaining_translation = goal_translation - current_translation()
				print("Remaining translation = ", remaining_translation)
				Moteurs.Translation(remaining_translation)
			else:
				sleep(0.2)

		print("========== ROTATION =========")
		goal_rotation = 180 + current_rotation() # 180 degrees + initial current position
		while((goal_rotation - current_rotation()) > 1.8):
			if(not(Moteurs.check_need_to_break())):
				remaining_rotation = goal_rotation - current_rotation()
				print("Remaining rotation = ", remaining_rotation)
				Moteurs.Rotation(remaining_rotation)
			else:
				sleep(0.2)
	print("========== Fin de homologation 2021 =========")

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
