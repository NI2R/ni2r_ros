#!/usr/bin/env python
# -*-coding:Latin-1 -*

from __future__ import print_function

from time import sleep
import math
from MCP3008 import MCP3008

import odrive
from odrive.enums import *

# TODO: Le robot vascille lors du deplacement, verifier si ca vient des coeff d'acceleration OU
# Si ca vient du coefficient de velocity dans la close loop de la Odrive (reglable)

class Odrive:
	def __init__(self, robot, odrv0):
		self.robot = robot
		self.sharp = MCP3008()

		self.motor0 = odrv0.axis0
		self.motor1 = odrv0.axis1
		self.Diameter = 80 #mm
		self.entre_axe = 275.0 #mm
		self.consigne = 0

	def Setup(self):
		trap_traj_vel_max = 0.75  # Vitesse maximale consigne
		trap_traj_accel = 5  # Rampe acceleration 10
		trap_traj_decel = 5  # Rampe deceleration 10
		trap_traj_inertia = 0  # A determiner

		print("========== Calibration **BIIIIP** =========")
		self.motor0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
		self.motor1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
		while self.motor0.current_state != AXIS_STATE_IDLE and self.motor1.current_state != AXIS_STATE_IDLE:
			sleep(0.1)

		print("========== Configuration Odrive =========")

		loop_control = AXIS_STATE_CLOSED_LOOP_CONTROL # Maintient en position les roues
		self.motor0.requested_state = loop_control
		self.motor1.requested_state = loop_control
		sleep(1)

		vel_limit = 100  # Vitesse maximale Odrive
		self.motor0.controller.config.vel_limit = vel_limit
		self.motor1.controller.config.vel_limit = vel_limit

		print("========== Setup input mode =========")
		mode = INPUT_MODE_TRAP_TRAJ # Consigne en position avec controle de la vitesse et accelerations

		self.motor0.controller.config.input_mode = mode
		self.motor1.controller.config.input_mode = mode

		while self.motor0.controller.config.input_mode != mode and self.motor0.controller.config.input_mode != mode:
			sleep(0.1) # Wait input mode is set

		print("========== Setup configs of input mode =========")

		self.motor0.trap_traj.config.vel_limit = trap_traj_vel_max
		self.motor1.trap_traj.config.vel_limit = trap_traj_vel_max

		self.motor0.trap_traj.config.accel_limit = trap_traj_accel
		self.motor1.trap_traj.config.accel_limit = trap_traj_accel

		self.motor0.trap_traj.config.decel_limit = trap_traj_decel
		self.motor1.trap_traj.config.decel_limit = trap_traj_decel

		self.motor0.controller.config.inertia = trap_traj_inertia
		self.motor1.controller.config.inertia = trap_traj_inertia

		print("========== SETUP done =========")

	def Length_to_rounds(self, length):

		"""Convertie un distance (en mm) a parcourir en nombre de tours de roue"""
		nb_rounds = length / (self.Diameter * math.pi)
		#print("nb_rounds = ", nb_rounds)
		return(nb_rounds)

	def Rounds_To_Length(self, rounds):
		"""Convertie un nombre de tours de roue a parcourir en une distance (en mm)"""
		length = rounds * (self.Diameter * math.pi)
		#print("nb_rounds = ", nb_rounds)
		return(length)

	def angle_to_rounds(self, angle):
		"""Convertie un angle (en degres) a parcourir en nombre de tours de roue"""
		nb_rounds = (angle * self.entre_axe) / (360 * self.Diameter)
		#print("nb_rounds = ", nb_rounds)
		return(nb_rounds)

	def check_need_to_break(self):
		"""Anything that could trigger the break (sharp, ros)"""
		result = False

		result = result or self.robot.stop_timer
		result = result or self.sharp.isCollide(550) # ~150mm

		return result

	def check_arrived(self):
		"""Anything that could trigger the break (sharp, ros)"""
# TODO: Use position difference instead of null velocity
		return self.motor0.encoder.vel_estimate == 0 and self.motor1.encoder.vel_estimate == 0	

	def wait_end_move(self):
		"""Wait the move (translation or rotation) to be executed"""
		sleep(0.2) # FIX - Delay to let motors start (no null velocity)
		while not(self.check_arrived()):
			if(self.check_need_to_break()):
				self.Freinage()
			#print
			sleep(0.1)


	def Translation(self,distance):
		''' Deplacement en mm (relatif)'''
		print("Position de depart\nPosition moteur0 = %.2f\nPosition moteur1 = %.2f" % (self.motor0.encoder.pos_estimate,self.motor1.encoder.pos_estimate)) # TODO: To fix


		self.consigne = self.Length_to_rounds(distance)
		self.motor0.controller.move_incremental(-1.0 * self.consigne, False) # False pour relatif
		self.motor1.controller.move_incremental(1.0 * self.consigne, False) # False pour relatif
		self.wait_end_move()


	def Rotation(self,angle):
		''' Rotation en degres de roue parcourue (trigonometrique)'''
		print("Position de depart\nPosition moteur0 = %.2f\nPosition moteur1 = %.2f" % (self.motor0.encoder.pos_estimate,self.motor1.encoder.pos_estimate)) # TODO: To fix
		self.consigne = self.angle_to_rounds(angle)
		self.motor0.controller.move_incremental(-1.0 * self.consigne, False) # False pour relatif
		self.motor1.controller.move_incremental(-1.0 * self.consigne, False) # False pour relatif
		self.wait_end_move()


	def Freinage(self):
		print("========== Freinage!!! =========")
		print("Avant freinage: ", self.motor0.encoder.pos_estimate)
		print("Avant freinage: ", self.motor1.encoder.pos_estimate)
		while(self.motor0.controller.input_pos != self.motor0.encoder.pos_estimate and self.motor1.controller.input_pos != self.motor1.encoder.pos_estimate):
			self.motor0.controller.input_pos = self.motor0.encoder.pos_estimate
			self.motor1.controller.input_pos = self.motor1.encoder.pos_estimate
		print("Apres freinage: ", self.motor0.encoder.pos_estimate)
		print("Apres freinage: ", self.motor1.encoder.pos_estimate)

	def Display_position(self,duration_in_sec):
		"""Affiche la position estimee par le Odrive durant le temps indiquee en argument - Thread blocking"""
		for i in range(duration_in_sec):
			print(self.motor0.encoder.pos_estimate) # Estimated position by Odrive (readonly)
			print(self.motor1.encoder.pos_estimate)
			sleep(1)

def main():
	odrv0 = odrive.find_any()
	Moteurs = Odrive(odrv0)
	print("========== Start homologation 2021 =========")
	Moteurs.Setup()

	print("========== TRANSLATION =========")
	dist = 1000
	Moteurs.Translation(dist)
	#Moteurs.Display_position(3)

	print("========== Fin de homologation 2021 =========")


if __name__ == "__main__" :
	main()
