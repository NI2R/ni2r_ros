#!/usr/bin/env python
# -*- coding: latin-1 -*-

import rospy
import time
import math
import logging
from std_msgs.msg import Int16
from std_msgs.msg import String
from std_msgs.msg import Bool

class Tools:
	def __init__(self):
		self.Arduino_Order = 0
		self.Arduino_State = 0
		self.bStateTirette = False
		self.Start = False
		self.Stop = False

	def Publish(self):
		self.publish_order_Arduino = rospy.Publisher('arduinoOrder', Int16, queue_size=10)  # 0=rien 1=init ... 8=Drapeau
		self.publish_order_Arduino.publish(self.Arduino_Order)
		print("la valeur %s, a ete publiee dans le topic %s", str(self.Arduino_Order), 'arduinoOrder')

		self.publish_stop = rospy.Publisher('Start_time', Bool, queue_size=10)
		self.publish_stop.publish(self.Start)
		print("la valeur %s, a ete publiee dans le topic %s", str(self.Start), 'Start')

		self.publish_stop = rospy.Publisher('Stop_time', Bool, queue_size=10)
		self.publish_stop.publish(self.Stop)
		print("la valeur %s, a ete publiee dans le topic %s", str(self.Stop), 'Stop')

	def Subscription(self):
		rospy.Subscriber('/arduinoState', Int16, self.Subscrib_Arduino_State)
		print("la valeur %s, a ete recuperee du topic %s", str(self.Subscrib_Arduino_State), '/arduinoState')
		rospy.Subscriber('StateTirette', Bool, self.Subscrib_State_Tirette) # 1 = Absente, 0 = Presente
		print("la valeur %s, a ete recuperee du topic %s", str(self.bStateTirette), 'StateTirette')

	def Subscrib_Arduino_State(self, data):
		self.Arduino_State = data.data

	def Subscrib_State_Tirette(self, data):
		self.bStateTirette = data.data

def main():

	''' == SETUP == '''
	tools = Tools()
	tools.Subscription()

	''' WAITING LOOP '''
	while not(tools.bStateTirette):
		print('En attente de la tirette : etat = %s', str(tools.bStateTirette))
		rospy.sleep(0.1)
	print('tirette Absente')
	''' WAITING LOOP END '''

	Start_Time = time.time()
	tools.Arduino_Order = 0
	''' END SETUP'''

	'''SUBSCRIPTION'''
	# tools.Subscription() # Twice?

	''' == PROGRAM LOOP == '''
	while not(rospy.is_shutdown()):
		'''PUBLISH'''
		tools.Publish()
		time.sleep(1)

		Current_Time = time.time()
		print('Time Comparaison : %s', str(Current_Time))
		if Current_Time - Start_Time >= 95:
			tools.Stop = True
			tools.Arduino_Order = 8
			while not(rospy.is_shutdown()):
				tools.Publish()
			break
	''' == LOOP-END == '''

if __name__ == '__main__':
	try:
		rospy.init_node('Main', anonymous=True)
		rospy.Rate(1)
		main()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
