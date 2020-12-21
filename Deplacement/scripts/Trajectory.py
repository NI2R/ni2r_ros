#!/usr/bin/env python
# -*- coding: latin-1 -*-

import rospy
import math
from std_msgs.msg import Float32
from geometry_msgs.msg import Pose2D
from DistanceAngulaire import DistanceAngulaire
from DistanceRectiligne import DistanceRectiligne

class Point:
    def __init__(self, name, x, y, theta):
        self.name = name
        self.x = x
        self.y = y
        self.theta = theta
        self.coordonnes = [x, y, theta]
        self.Pose2D = Pose2D()
        self.Pose2D.x = x
        self.Pose2D.y = y
        self.Pose2D.theta = theta

class Trajectory:
    def __init__(self):
        self.goal_point = Point('goal', 0, 0, 0)
        self.actual_point = Point('actual', 0, 0, 0)
        self.Odom = 0

    def main_trajectory(self, btest=False):

        #if btest:
        #    actual_point = Point('actual', 0, 0, 0)
        #    x = float(input("X du point vise en mm = \n"))
        #    y = float(input("Y du point vise en mm = \n"))
        #    theta = float(input("Theta du point vise en radian = \n"))
        #    goal_point = Point('goal', x, y, theta * math.pi / 180)
        #else:
        self.subscribe()

        while not rospy.is_shutdown():
            self.subscribe()
            #print('goal_point.Pose2D.x =', self.goal_point.Pose2D.x)
            #print('goal_point.Pose2D.y =', self.goal_point.Pose2D.y)
            #print('goal_point.Pose2D.theta =', self.goal_point.Pose2D.theta)
            self.actual_point.x = self.Odom
            solver_rectiligne = DistanceRectiligne(self.actual_point, self.goal_point)
            #print('solver_rectiligne.distance_rectiligne =', solver_rectiligne.distance_rectiligne)
            solver_angulaire = DistanceAngulaire(self.actual_point, self.goal_point)
            #print('solver_angulaire.delta_theta =', solver_angulaire.delta_theta)
            #print('solver_angulaire.delta_theta_final =', solver_angulaire.delta_theta_final)
            solver_rectiligne.solve()  # calcule la distance rectiligne a parcourir
            solver_angulaire.solve()  # calcule l'angle intermediaire relatif et l'angle final relatif

            solver_rectiligne.publish('Distance_rectiligne', solver_rectiligne.distance_rectiligne)
            solver_angulaire.publish('Angle_intermediaire', solver_angulaire.delta_theta)
            solver_angulaire.publish('Angle_final', solver_angulaire.delta_theta_final)

            print('Distance_rectiligne = {}'.format(solver_rectiligne.distance_rectiligne))
            print('Angle_intermediaire = {}'.format(solver_angulaire.delta_theta * 180/math.pi))
            print('Angle_final = {}'.format(solver_angulaire.delta_theta_final * 180/math.pi))


            #if solver_rectiligne.distance_rectiligne > 0:
            #    actual_point.x += 20

            rospy.sleep(2)


    def subscribe(self):
        rospy.Subscriber('goal_point', Pose2D, self.callback_goal)
        rospy.Subscriber('actual_point', Pose2D, self.callback_actual)
        rospy.Subscriber('/odriveDistance_parcourue', Float32, self.callback_Odom)


    def callback_goal(self, data):
        self.goal_point.Pose2D = data


    def callback_actual(self, data):
        self.actual_point.Pose2D = data

    def callback_Odom(self, data):
        self.Odom = data


if __name__ == '__main__':
    try:
        rospy.init_node('martialtuesmoche', anonymous=True)
        rospy.Rate(1)
        Traj = Trajectory()
        Traj.main_trajectory(False)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass