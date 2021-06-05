#!/usr/bin/env python
# -*-coding:Latin-1 -*
from __future__ import print_function
import rospy

from time import sleep, time

from std_msgs.msg import Bool

class Robot_properties:
	def __init__(self):
		self.start = False
		self.timer_start = 0
		self.match_duration = 5 # in seconds

		rospy.Subscriber("StateTirette", Bool, self.UpdateStart)

		self.pub_stop_timer = '/stop_timer'

		self.pub_stop_timer_topic = rospy.Publisher(self.pub_stop_timer, Bool, queue_size=1)

	def UpdateStart(self, data):
		self.start = data.data

	def isStopTimer(self):
		result = Bool()
		result.data = time.time() - self.timer_start > self.match_duration
		self.pub_stop_timer_topic.publish(result)
		return result.data

def main():
	rospy.init_node('Main', anonymous=True)
	robot = Robot_properties()

	while(not(robot.start)):
		sleep(0.1)
		# rospy.sleep(1)
	robot.timer_start = time.time()

	while(not(robot.isStopTimer())):
		sleep(0.1)

	print("========== Fin de homologation 2021 =========")

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
