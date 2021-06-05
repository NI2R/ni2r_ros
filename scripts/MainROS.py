#!/usr/bin/env python
# -*-coding:Latin-1 -*
from __future__ import print_function
import rospy

from time import sleep, time

from std_msgs.msg import Bool, Int16

class Robot_properties:
	def __init__(self):
		self.start = False
		self.timer_start = 0
		self.match_duration = 90 # in seconds

		rospy.Subscriber("StateTirette", Bool, self.UpdateStart)

		self.pub_stop_timer = '/stop_timer'
		self.pub_arduino = '/arduinoOrder'

		self.pub_stop_timer_topic = rospy.Publisher(self.pub_stop_timer, Bool, queue_size=1)
		self.pub_arduino_topic = rospy.Publisher(self.pub_arduino, Int16, queue_size=1)

	def UpdateStart(self, data):
		self.start = data.data

	def isStopTimer(self):
		result = Bool()
		result.data = time() - self.timer_start > self.match_duration
		self.pub_stop_timer_topic.publish(result)
		
		if(result.data):
			arduino_command = Int16()
			arduino_command_raise_flag = 15
			arduino_command.data = arduino_command_raise_flag
			self.pub_arduino_topic.publish(arduino_command)

		return result.data

def main():
	rospy.init_node('Main', anonymous=True)
	robot = Robot_properties()

	print("========== Start homologation 2021 =========")
	while(not(robot.start)):
		sleep(0.1)
		# rospy.sleep(1)
	robot.timer_start = time()
	print("========== Tirette triggered =========")

	while(not(robot.isStopTimer())):
		sleep(0.1)

	print(time() - robot.timer_start)
	print("========== Fin de homologation 2021 =========")

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
