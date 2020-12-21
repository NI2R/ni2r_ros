#!/usr/bin/env python
# -*- coding: latin-1 -*-

import rospy
import math
from std_msgs.msg import Float32
from std_msgs.msg import Bool
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
        self.nPrecision = 5 # en mm
        self.Length_Precision = 10
        self.EnableCompute = False
        self.Retain = False
        self.EnableMove = False
        self.position_atteinte = False
        self.bValide_Distance_Rectiligne = False
        self.bValide_Distance_Angulaire_Inter = False
        self.bValide_Distance_Angulaire_Final = False
        self.bList_Valide_Distance_Rectiligne_Buffer = self.Length_Precision*[0]
        self.bList_Valide_Distance_Angulaire_Inter_Buffer = self.Length_Precision*[0]
        self.bList_Valide_Distance_Angulaire_Final_Buffer = self.Length_Precision*[0]

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
            print('Trajectoire : %d', self.EnableCompute)

            if self.EnableCompute:
                self.Retain = self.EnableCompute

            if self.Retain:
                solver_rectiligne = DistanceRectiligne(self.actual_point, self.goal_point)
                solver_angulaire = DistanceAngulaire(self.actual_point, self.goal_point)
                solver_rectiligne.solve()  # calcule la distance rectiligne a parcourir
                solver_angulaire.solve()  # calcule l'angle intermediaire relatif et l'angle final relatif

                solver_rectiligne.publish('Distance_rectiligne', solver_rectiligne.distance_rectiligne)
                solver_angulaire.publish('Angle_intermediaire', solver_angulaire.delta_theta)
                solver_angulaire.publish('Angle_final', solver_angulaire.delta_theta_final)

                print('Trajectoire : Distance_rectiligne = {}'.format(solver_rectiligne.distance_rectiligne))
                print('Trajectoire : Angle_intermediaire = {}'.format(solver_angulaire.delta_theta * 180/math.pi))
                print('Trajectoire : Angle_final = {}'.format(solver_angulaire.delta_theta_final * 180/math.pi))
                self.EnableMove = True
                for i in range(0, 30):
                    self.publish('/odriveEnableMove', self.EnableMove)
                    rospy.sleep(0.2)
                self.Retain = False
                print('Trajectoire : Published')

            if self.position_atteinte:
                self.actual_point.Pose2D.x = self.goal_point.Pose2D.x
                self.actual_point.Pose2D.y = self.goal_point.Pose2D.y
                self.actual_point.Pose2D.theta = self.goal_point.Pose2D.theta
                print('Actual point x = %f / y = %f / theta = %f', (self.actual_point.Pose2D.x, self.actual_point.Pose2D.y, self.actual_point.Pose2D.theta))

            #self.Compute_Rectiligne(solver_rectiligne)
            #self.Compute_Angulaire(solver_angulaire)
#
            #Position_OK = self.bValide_Distance_Rectiligne and self.bValide_Distance_Angulaire_Inter and self.bValide_Distance_Angulaire_Final
#
            #self.publish('Arrive', Position_OK)

            rospy.sleep(1)

    def Compute_Rectiligne(self, solver_rectiligne):
        bSum = True
        for i in range(self.Length_Precision):
            if abs(solver_rectiligne.distance_rectiligne) < self.nPrecision:
                self.bList_Valide_Distance_Rectiligne_Buffer[i] = True
            else:
                for j in range(self.Length_Precision):
                    self.bList_Valide_Distance_Rectiligne_Buffer[j] = False
            '''Concaténation de la liste buffer'''
            bSum = bSum and self.bList_Valide_Distance_Rectiligne_Buffer[i]
            print('bList_Valide_Distance_Rectiligne_Buffer =', self.bList_Valide_Distance_Rectiligne_Buffer)
        '''Stockage du Booléen final'''
        self.bValide_Distance_Rectiligne = bSum

    def Compute_Angulaire(self, solver_angulaire):
        bSum_Inter = True
        bSum_Final = True
        for i in range(self.Length_Precision):
            if abs(solver_angulaire.delta_theta) < self.nPrecision:
                self.bList_Valide_Distance_Angulaire_Inter_Buffer[i] = True
            else:
                for j in range(self.Length_Precision):
                    self.bList_Valide_Distance_Angulaire_Inter_Buffer[j] = False
            '''Concaténation de la liste buffer'''
            bSum_Inter = bSum_Inter and self.bList_Valide_Distance_Angulaire_Inter_Buffer[i]
            print('bList_Valide_Distance_Angulaire_Inter_Buffer =', self.bList_Valide_Distance_Angulaire_Inter_Buffer)

        '''Stockage du Booléen final'''
        self.bValide_Distance_Angulaire_Inter = bSum_Inter

        for i in range(self.Length_Precision):
            if abs(solver_angulaire.delta_theta_final) < self.nPrecision:
                self.bList_Valide_Distance_Angulaire_Final_Buffer[i] = True
            else:
                for j in range(self.Length_Precision):
                    self.bList_Valide_Distance_Angulaire_Final_Buffer[j] = False
            '''Concaténation de la liste buffer'''
            bSum_Final = bSum_Final and self.bList_Valide_Distance_Angulaire_Final_Buffer[i]
            print('bList_Valide_Distance_Angulaire_Final_Buffer =', self.bList_Valide_Distance_Angulaire_Final_Buffer)

        '''Stockage du Booléen final'''
        self.bValide_Distance_Angulaire_Final = bSum_Final

    def publish(self, strtopic, data):
        pub = rospy.Publisher(strtopic, Bool, queue_size=1)
        pub.publish(data)


    def subscribe(self):
        rospy.Subscriber('goal_point', Pose2D, self.callback_goal)
        #rospy.Subscriber('actual_point', Pose2D, self.callback_actual)
        #rospy.Subscriber('/odriveDistance_parcourue', Float32, self.callback_Odom)
        rospy.Subscriber('/odrivePosition_atteinte', Bool, self.callback_Position_Atteinte)
        rospy.Subscriber('/odriveEnableCompute', Bool, self.callback_Enable_Compute)


    def callback_goal(self, data):
        self.goal_point.Pose2D = data


    def callback_actual(self, data):
        self.actual_point.Pose2D = data

    def callback_Position_Atteinte(self, data):
        self.position_atteinte = data.data

    def callback_Enable_Compute(self, data):
        self.EnableCompute = data.data

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