#!/usr/bin/env python
# -*- coding: latin-1 -*-

import rospy
import time
import math
import logging
from std_msgs.msg import Int16
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose2D


class Point:
    def __init__(self, name, x, y, theta):
        self.name = name
        self.x = x
        self.y = y
        self.theta = theta
        self.Pose2D = Pose2D()

    def Get_Coordonnes(self, point):
        self.Pose2D.x = point.x
        self.Pose2D.y = point.y
        self.Pose2D.theta = point.theta
        self.x = point.x
        self.y = point.y
        self.theta = point.theta


class Tools:
    def __init__(self):
        self.nPoint = 1
        self.nbActual_Point = 0
        self.dPointdictionnary = {}
        self.log = logging
        self.data = 0
        self.Code_Aruco = 'None'
        self.Arduino_Order = 0
        self.Arduino_State = 0
        self.cgoal = Point(name='goal', x=0, y=0, theta=0)
        self.cgoal.x = 0
        self.cgoal.y = 0
        self.cgoal.theta = 0
        self.bArrive = False
        self.bStateClef = False
        self.bStateCote = False
        self.bStateTirette = False
        self.bStateTiretteBuffer = True
        self.bPosition_Atteinte = False
        self.Stop = False

    def Reset(self):
        self.cgoal.x = 0
        self.cgoal.y = 0
        self.cgoal.theta = 0
        self.cgoal.Pose2D.x = 0
        self.cgoal.Pose2D.y = 0
        self.cgoal.Pose2D.theta = 0

    def Switch_Side(self, bBool):
        if bBool:
            self.log.info("you chose the yellow side")
            #for i in range(0, self.nPoint):
            #TODO: conversion des angles

        else:
            self.log.info("you chose the blue side")

    def Next_Point(self):
        if self.nbActual_Point < self.nPoint:
            self.nbActual_Point += 1
            self.log.info('le point actuel est %s', str(self.nbActual_Point))
        else:
            self.log.error('le point actuel est %s et souhaite etre increment�', str(self.nbActual_Point))
        self.cgoal.Get_Coordonnes(self.dPointdictionnary["Point"+str(self.nbActual_Point)])

    def Logs(self, loglevel):
        self.log.basicConfig(filename='main.log', format='%(asctime)s %(levelname)s:%(message)s', level=loglevel)
        self.log.basicConfig(format='%(levelname)s:%(message)s', level=loglevel)
        self.log.critical('============================ New Try ============================')

    def Publish(self):
        self.publish_order_Arduino = rospy.Publisher('arduinoOrder', Int16, queue_size=10)  # 0=rien 1=init ... 8=Drapeau
        self.publish_order_Arduino.publish(self.Arduino_Order)
        self.log.info("la valeur %s, a ete publiee dans le topic %s", str(self.Arduino_Order), 'arduinoOrder')
        self.publish_goal_point = rospy.Publisher('goal_point', Pose2D, queue_size=200)
        self.publish_goal_point.publish(self.cgoal.Pose2D)
        self.log.info("la valeur %s, a ete publiee dans le topic %s", str(self.cgoal.Pose2D), 'goal_point')
        self.publish_stop = rospy.Publisher('Stop_time', Bool, queue_size=10)
        self.publish_stop.publish(self.Stop)
        self.log.info("la valeur %s, a ete publiee dans le topic %s", str(self.Stop), 'Stop')


    def Subscription(self):
        rospy.Subscriber('/arduinoState', Int16, self.Subscrib_Arduino_State)
        self.log.debug("la valeur %s, a ete recuperee du topic %s", str(self.Subscrib_Arduino_State), '/arduinoState')
        rospy.Subscriber('CodeAruco', String, self.Subscrib_Code_Aruco)
        self.log.debug("la valeur %s, a ete recuperee du topic %s", str(self.Subscrib_Code_Aruco), 'Code_Aruco')
        rospy.Subscriber('Arrive', Bool, self.Subscrib_Arrive)
        self.log.debug("la valeur %s, a ete recuperee du topic %s", str(self.Subscrib_Arrive), 'Arrive')
        rospy.Subscriber('StateClef', Bool, self.Subscrib_State_Clef) # 1 = Debug, 0 = Normal
        self.log.debug("la valeur %s, a ete recuperee du topic %s", str(self.bStateClef), 'StateClef')
        rospy.Subscriber('StateCote', Bool, self.Subscrib_State_Cote) # 1 = Jaune, 0 = Bleu
        self.log.debug("la valeur %s, a ete recuperee du topic %s", str(self.bStateCote), 'StateCote')
        rospy.Subscriber('StateTirette', Bool, self.Subscrib_State_Tirette) # 1 = Absente, 0 = Presente
        self.log.debug("la valeur %s, a ete recuperee du topic %s", str(self.bStateTirette), 'StateTirette')
        rospy.Subscriber('/odrivePosition_atteinte', Bool, self.Subscrib_Position_Atteinte)  # 1 = Atteinte, 0 = en cours
        self.log.debug("la valeur %s, a ete recuperee du topic %s", str(self.bPosition_Atteinte), 'StateTirette')

    def Subscrib_Arduino_State(self, data):
        self.Arduino_State = data.data

    def Subscrib_Code_Aruco(self, data):
        self.Code_Aruco = data.data

    def Subscrib_Arrive(self, data):
        self.bArrive = data.data

    def Subscrib_State_Clef(self, data):
        self.bStateClef = data.data

    def Subscrib_State_Cote(self, data):
        self.bStateCote = data.data

    def Subscrib_State_Tirette(self, data):
        self.bStateTirette = data.data

    def Subscrib_Position_Atteinte(self, data):
        self.bPosition_Atteinte = data.data




    def Road_Creation(self):
        self.dPointdictionnary["Point0"] = Point("Point0", 1, 1, 1)
        self.dPointdictionnary["Point1"] = Point("Homologation", 545 + 130, 0, 0)
        self.dPointdictionnary["Point2"] = Point("Point2", 3, 3, 3)
        self.dPointdictionnary["Point3"] = Point("Point3", 0, 0, 0)
        self.dPointdictionnary["Point4"] = Point("Point4", 0, 0, 0)
        self.dPointdictionnary["Point5"] = Point("Point5", 0, 0, 0)
        self.dPointdictionnary["Point6"] = Point("Point6", 0, 0, 0)
        self.dPointdictionnary["Point7"] = Point("Point7", 0, 0, 0)
        self.dPointdictionnary["Point8"] = Point("Point8", 0, 0, 0)
        self.dPointdictionnary["Point9"] = Point("Point9", 0, 0, 0)
        self.dPointdictionnary["Point10"] = Point("Point10", 0, 0, 0)
        self.dPointdictionnary["Point11"] = Point("Point11", 0, 0, 0)
        self.dPointdictionnary["Point12"] = Point("Point12", 0, 0, 0)
        self.dPointdictionnary["Point13"] = Point("Point13", 0, 0, 0)
        self.dPointdictionnary["Point14"] = Point("Point14", 0, 0, 0)
        if self.Code_Aruco == 'NORD':
            self.log.info('Le Code_Aruco a ete identifie comme etant %s', self.Code_Aruco)
            self.dPointdictionnary["Point15"] = Point("Point15", 0, 0, 0)
            self.dPointdictionnary["Point16"] = Point("Point16", 0, 0, 0)
            self.dPointdictionnary["Point17"] = Point("Point17", 0, 0, 0)
            self.dPointdictionnary["Point18"] = Point("Point18", 0, 0, 0)
            self.dPointdictionnary["Point19"] = Point("Point19", 0, 0, 0)
            self.dPointdictionnary["Point20"] = Point("Point20", 0, 0, 0)
        elif self.Code_Aruco == 'SUD':
            self.log.info('Le Code_Aruco a ete identifie comme etant %s', self.Code_Aruco)
            self.dPointdictionnary["Point15"] = Point("Point15", 0, 0, 0)
            self.dPointdictionnary["Point16"] = Point("Point16", 0, 0, 0)
            self.dPointdictionnary["Point17"] = Point("Point17", 0, 0, 0)
            self.dPointdictionnary["Point18"] = Point("Point18", 0, 0, 0)
            self.dPointdictionnary["Point19"] = Point("Point19", 0, 0, 0)
            self.dPointdictionnary["Point20"] = Point("Point20", 0, 0, 0)
        else:
            self.log.error('Le Code_Aruco n a pas ete identifie, sa valeur = %s', self.Code_Aruco)
            self.dPointdictionnary["Point15"] = Point("Point15", 0, 0, 0)
            self.dPointdictionnary["Point16"] = Point("Point16", 0, 0, 0)
            self.dPointdictionnary["Point17"] = Point("Point17", 0, 0, 0)
            self.dPointdictionnary["Point18"] = Point("Point18", 0, 0, 0)
            self.dPointdictionnary["Point19"] = Point("Point19", 0, 0, 0)
            self.dPointdictionnary["Point20"] = Point("Point20", 0, 0, 0)

        for i in range(0, self.nPoint + 1):
            self.log.debug('le point %s a ete ajoute au dictionnaire : x = %s, y = %s, theta = %s',
                          self.dPointdictionnary["Point"+str(i)].name,
                          str(self.dPointdictionnary["Point"+str(i)].x),
                          str(self.dPointdictionnary["Point"+str(i)].y),
                          str(self.dPointdictionnary["Point"+str(i)].theta)
                          )

def Logs(log, loglevel):
    log.basicConfig(filename='Super_main.log', format='%(asctime)s %(levelname)s:%(message)s', level=loglevel)
    log.basicConfig(format='%(levelname)s:%(message)s', level=loglevel)
    log.critical('============================ New Try ============================')

def main():

    ''' == SETUP == '''

    log = logging
    Logs(log, log.DEBUG)
    tools = Tools()
    tools.Logs(logging.DEBUG)
    #tools.Arduino_Order = 1
    tools.Subscription()
    print('=============================Fin du SETUP=============================')
    log.info('Fin du SETUP')

    ''' WAITING LOOP '''
    while not(tools.bStateTirette):
        print('En attente de la tirette : etat = %s', str(tools.bStateTirette))
        log.info('En attente de la tirette : etat = %s', str(tools.bStateTirette))
        rospy.sleep(0.5)
    ''' WAITING LOOP END '''

    print('tirette Absente')
    #log.info('tirette arrachee')
    Start_Time = time.time()
    tools.Switch_Side(tools.bStateCote)
    tools.Arduino_Order = 0
    ''' == SETUP END == '''

    '''SUBSCRIPTION'''
    tools.Subscription()
    log.info('SUBSCRIPTION')

    ''' == PROGRAM LOOP == '''
    tools.Road_Creation()
    tools.Next_Point()
    while not(rospy.is_shutdown()):
        log.info('Inside PROGRAM LOOP')

        #'''SUBSCRIPTION'''
        #tools.Subscription()
        #log.info('SUBSCRIPTION')

        '''PROGRAM'''
        if tools.bPosition_Atteinte:
            tools.Next_Point()

        '''PUBLISH'''
        tools.Publish()
        time.sleep(1)
        log.info('PUBLISH')

        Current_Time = time.time()
        log.info('Time Comparaison : %s', str(Current_Time))
        if Current_Time - Start_Time >= 95:
            tools.Stop = True
            tools.Reset()
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

