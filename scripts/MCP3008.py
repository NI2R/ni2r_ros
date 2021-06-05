#!/usr/bin/env python
# -*-coding:Latin-1 -*

import spidev
import time

# 5 sensors, ID from 0 to 4 included
# Sensor #0 : Front Left
# Sensor #1 : Front Right
# Sensor #2 : Front Center
# Sensor #3 : Back Left
# Sensor #4 : Back Right

class MCP3008:
	def __init__(self):
		self.communication = spidev.SpiDev()
		self.n_sensors = 5
		self.sensor_value = [0] * self.n_sensors
		
		self.n_loop_mean = 5
		self.delay_loop = 0.060 #limit is 200k samples/sec for MCP but sharp is limited by 20/sec

		self.communication.open(0,0)
		self.communication.max_speed_hz=1000000
		self.communication.mode =0b00

	def updateValues(self):
		for i in range(self.n_loop_mean):
			for sensor_id in range(self.n_sensors):
				resp = self.communication.xfer2([0x01, (0x08 + sensor_id) << 4, 0x00])
				self.sensor_value[sensor_id] += ((resp[1] & 0x03) << 8) + resp[2]
			time.sleep(self.delay_loop) # 0.060 * 5 = 0.3s

		for sensor_id in range(self.n_sensors):
			self.sensor_value[sensor_id] /= self.n_loop_mean

	def isCollide(self, threshold_value):
		result = False

		self.updateValues()

		# for sensor in self.sensor_value:
		# 	result = result or (sensor > threshold_value)

		for sensor_id in range(self.n_sensors):
			result = result or (self.sensor_value[sensor_id] > threshold_value)
			if(self.sensor_value[sensor_id] > threshold_value):
				print("Sensor %d is triggered" % sensor_id)

		return result
