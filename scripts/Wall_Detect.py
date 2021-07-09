#!/usr/bin/env python
# -*-coding:Latin-1 -*
import rospy
import math
from time import sleep
from std_msgs.msg import Int16MultiArray, Int16

############## SETUP IN MM ##############
#table dimensions
X_MAX = 3000
Y_MAX = 2000

#initial position if in bottom 
X_INIT_BOTTOM = 300
Y_INIT_BOTTOM = 800

#robot dimensions
L = 260
l = 330

AVG, AVD, ARG, ARD, GAV, GAR, DAV, DAR = 0, 0, 0, 0, 0, 0, 0, 0

############## FONCTIONS ##############
def getAVG(arg):
    global AVG
    AVG = arg.data 
def getAVD(arg):
    global AVD
    AVD = arg.data 
    
def getARG(arg):
    global ARG
    ARG = arg.data   
def getARD(arg):
    global ARD
    ARD = arg.data 
    
def getGAV(arg):
    global GAV
    GAV = arg.data 
def getGAR(arg):
    global GAR
    GAR = arg.data 
    
def getDAV(arg):
    global DAV
    DAV = arg.data 
def getDAR(arg):
    global DAR
    DAR = arg.data 
    
def start_position(parkingSpot):
    if parkingSpot == 'top':
        #initial position if in top 
        X_INIT = 2700
        Y_INIT = 800
    elif parkingSpot == 'bottom':
        #initial position if in bottom 
        X_INIT = 300
        Y_INIT = 800    
    else:
        print("Error, check parking spot argument: top or bottom?")
        exit()
        
    tab = [X_INIT, Y_INIT]
    return tab

def read_sensor(sensor):
    return sensor

def distance_from_wall(sensor_list):
    return int((sensor_list[0] + sensor_list[1] + sensor_list[2])/2)

def orientation_from_wall(sensor_list):
    #if sensor_pair[0] > sensor_pair[1]:
    return math.atan((sensor_list[0] - sensor_list[1])/sensor_list[2]) *180/math.pi
    #else:
        #return math.atan2((sensor_pair[1] - sensor_pair[0])/length)
        
def publisher(coord):
    tab = Int16MultiArray()
    tab.data.append(coord[0])
    tab.data.append(coord[1])
    tab.data.append(coord[2])

    pub = rospy.Publisher('Wall_Detect_topic', Int16MultiArray, queue_size=1) #topicname + type of topic + nb in queue
    pub.publish(tab) #Publication de l'objectif
    
############## MAIN ##############
def main():
    global L,l
    global AVG, AVD, ARG, ARD, GAV, GAR, DAV, DAR
    
    rospy.init_node('Wall_Detect', anonymous = True)
    
    #subscribing to all sensors
    rospy.Subscriber("CapteurAVG", Int16, getAVG)
    rospy.Subscriber("CapteurAVD", Int16, getAVD)
    
    rospy.Subscriber("CapteurARG", Int16, getARG)
    rospy.Subscriber("CapteurARD", Int16, getARD)
    
    rospy.Subscriber("CapteurGAV", Int16, getGAV)
    rospy.Subscriber("CapteurGAR", Int16, getGAR)
    
    rospy.Subscriber("CapteurDAV", Int16, getDAV)
    rospy.Subscriber("CapteurDAR", Int16, getDAR)
    
    #sensors and their value
    #Top Left&Right
    top_list = [AVG,AVD,L] #two sensors and robot length
    
    #Bottom Left&Right
    bottom_list = [ARG,ARD,L]
    
    #Left Top&Bottom
    left_list = [GAV,GAR,l]
    
    #Right Top&Bottom
    right_list = [DAV,DAR,l]

    print("="*10 + " Start of wall detection " + "="*10)
    
    pos_init = start_position("bottom")
    print("Initial position: ", pos_init)
        
    while not rospy.is_shutdown():
        dist_bottom = distance_from_wall(bottom_list)
        dist_left = distance_from_wall(right_list)
        
        current_position = [dist_bottom,dist_left]
        print("Current position", current_position)
        
        alpha = orientation_from_wall(bottom_list)
        print("Current orientation", alpha)
        
        coord = current_position
        coord.append(alpha)
        publisher(coord) #Demande de publication du nouvel objectif
        sleep(1)
        
    print("="*10 + " End of wall detection " + "="*10)
    
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass