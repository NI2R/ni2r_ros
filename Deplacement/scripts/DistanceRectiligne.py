#!/usr/bin/env python
# -*- coding: latin-1 -*-

import rospy
import sys
import math
import geometry_msgs.msg
from std_msgs.msg import Float32


class DistanceRectiligne:
    def __init__(self, p1, p2):
        self.X1 = p1.Pose2D.x
        self.Y1 = p1.Pose2D.y
        self.X2 = p2.Pose2D.x
        self.Y2 = p2.Pose2D.y
        self.delta_X = 0
        self.delta_Y = 0
        self.distance_rectiligne = 0

    def solve(self):

        #print('INFO : Coordonnées Point Actuel : X = {}, Y = {}'.format(self.X1, self.Y1))
        #print('INFO : Coordonnées Point à Atteindre : X = {}, Y = {}'.format(self.X2, self.Y2))

        self.delta_X = self.X2 - self.X1
        self.delta_Y = self.Y2 - self.Y1

        self.distance_rectiligne = math.sqrt(self.delta_X**2 + self.delta_Y**2)

        #print('INFO : Delta_X = {}, Delta_Y = {}'.format(self.delta_X,self.delta_Y))
        #print('INFO : Distance rectiligne = {}'.format(self.distance_rectiligne))

    def publish(self, strtopic, data):
        pub = rospy.Publisher(strtopic, Float32, queue_size=1)
        pub.publish(data)
