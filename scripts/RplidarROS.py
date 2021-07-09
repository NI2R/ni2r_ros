#!/usr/bin/env python
# -*-coding:Latin-1 -*
# from __future__ import print_function
import rospy

from time import sleep, time
from sensor_msgs.msg import LaserScan

from std_msgs.msg import Bool

from std_srvs.srv import Empty

class Robot_properties:
	def __init__(self):
		self.stop_timer = False
		self.scans = []
		self.obstacle_range = 0.45 # in meters

		rospy.Subscriber("stop_timer", Bool, self.UpdateStop)
		rospy.Subscriber("scan", LaserScan, self.UpdateLidar)

		self.pub_stop_lidar = '/stop_lidar'

		self.pub_stop_lidar_topic = rospy.Publisher(self.pub_stop_lidar, Bool, queue_size=1)

	def UpdateLidar(self, data):
		self.scans = data.ranges

	def UpdateStop(self, data):
		self.stop_timer = data.data

	def isLidarObstacle(self):
		result = Bool()
		
		too_close = False
		for scan in self.scans:
			if scan < self.obstacle_range:
				too_close = True
				#print("[Lidar] Obstacle detected")
				break
		result.data = too_close
		self.pub_stop_lidar_topic.publish(result)

		return result.data

def main():
	rospy.init_node('rplidar_ni2r_ros', anonymous=True)
	robot = Robot_properties()

	while(not(robot.stop_timer)):
		robot.isLidarObstacle()
		sleep(0.1)
	
	rospy.wait_for_service('stop_motor')
	stop_lidar_spin = rospy.ServiceProxy('stop_motor', Empty)
	stop_lidar_spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
