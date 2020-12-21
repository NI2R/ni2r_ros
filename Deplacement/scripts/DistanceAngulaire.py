#!/usr/bin/env python
# -*- coding: latin-1 -*-

import rospy
import sys
import math
from std_msgs.msg import Float32


class DistanceAngulaire:
    def __init__(self, p1, p2):
        self.X1 = p1.Pose2D.x
        self.Y1 = p1.Pose2D.y
        self.X2 = p2.Pose2D.x
        self.Y2 = p2.Pose2D.y
        self.theta1 = p1.Pose2D.theta   # angle actuel
        self.theta2 = p2.Pose2D.theta   # angle que l'on veut avoir sur le point final.
        self.theta_target = 0   # angle directeur du parcour entre les points
        self.delta_X = self.X2 - self.X1
        self.delta_Y = self.Y2 - self.Y1
        self.theta_direct = 0
        self.theta_indirect = 0
        self.delta_theta = 0
        self.delta_theta_final = 0
        self.angular_distance = 0
        self.erreur_admissible = 1

    def solve(self):
        # self.delta_theta = self.theta2 - self.theta1
        # print('INFO : Delta_X = {}, Delta_Y = {}'.format(self.delta_X, self.delta_Y))
        # Calcul de l'angle intermédiaire pour atteindre le point2 : self.theta_target Absolu
        # et de la consigne relative : self.delta_theta

        if self.delta_X == 0:
            if self.delta_Y > 0 and math.pi/2 - 0.1 < self.theta1 < math.pi/2 + 0.1:
                self.delta_theta = 90 - self.theta1
            elif self.delta_Y < 0 and -math.pi/2 - 0.1 < self.theta1 < -math.pi/2 + 0.1:
                self.delta_theta = -90 - self.theta1
            elif self.delta_Y == 0:
                self.delta_theta = 0
            else:
                print('EXCEPTION : delta_X = 0 et delta_theta = {}'.format(self.delta_theta))
        elif self.delta_Y == 0:
            if self.delta_X > 0 and -0.1 < self.theta1 < 0.1:
                self.delta_theta = - self.theta1
            elif self.delta_X > 0 and math.pi - 0.1 < self.theta1 < math.pi + 0.1:
                self.delta_theta = math.pi - self.theta1
            else:
                print('EXCEPTION : delta_Y = 0 et delta_theta = {}'.format(self.delta_theta))
        elif self.delta_X != 0 and self.delta_Y != 0:
            if self.delta_X > 0:
                self.theta_target = math.atan(self.delta_Y/self.delta_X)
            elif self.delta_X < 0:
                self.theta_target = math.atan(self.delta_X/self.delta_Y)
                if self.delta_Y < 0:
                    self.theta_target -= math.pi
                elif self.delta_Y > 0:
                    self.theta_target += math.pi
                else:
                    print('EXCEPTION : delta_X < 0 et theta_target = {}'.format(self.theta_target))
            else:
                self.theta_target = 0

            self.delta_theta = min(self.theta_target - self.theta1, 2*math.pi + self.theta_target - self.theta1)
            #print('INFO : delta_theta = {}'.format(self.delta_theta))
        else:
            print('EXCEPTION : delta_theta = {}'.format(self.delta_theta))

        # delta_theta est calculé : angle intermédiaire de poucaour entre les 2 points

        #condition de dernière rotation temporisation pour ne pas envoyer de donnees aberrantes

        #i = 0
        #done = False
        #if abs(self.delta_X) < self.erreur_admissible and abs(self.delta_Y) < self.erreur_admissible:
        #    i = i + 1
        #    if i > 10:
        #        done = True
        #        self.delta_theta_final = 0
        #if done:

        # Recherche du theta optimal

        self.theta_direct = self.theta2 - self.theta1
        if self.theta_direct > 0:
            self.theta_indirect = self.theta2 - self.theta1 - 2 * math.pi
        elif self.theta_direct < 0:
            self.theta_indirect = self.theta2 - self.theta1 + 2 * math.pi
        else:
            self.delta_theta_final = 0

        if abs(self.theta_direct) - abs(self.theta_indirect) > 0:
            self.delta_theta_final = self.theta_indirect
        elif abs(self.theta_direct) - abs(self.theta_indirect) < 0:
            self.delta_theta_final = self.theta_direct
        else:
            self.delta_theta_final = 0

        '''
        print('INFO : Theta1 = {}'.format(self.theta1))
        print('INFO : Theta2 = {}'.format(self.theta2))
        print('INFO : Theta_direct = {}'.format(self.theta_direct))
        print('INFO : Theta_indirect = {}'.format(self.theta_indirect))
        print('INFO : delta_theta_final (rad) = {}'.format(self.delta_theta_final))
        '''
        #print('INFO : delta_theta_final = {}'.format(self.delta_theta_final * 180/math.pi))

    def publish(self, strtopic, data):
        pub = rospy.Publisher(strtopic, Float32, queue_size=1)
        pub.publish(data)
