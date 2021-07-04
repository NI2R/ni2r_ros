#!/usr/bin/env python
# -*-coding:Latin-1 -*
import rospy
from time import sleep
from std_msgs.msg import Header, Time, Bool
from fiducial_msgs.msg import FiducialArray, Fiducial

class Aruco:
    def __init__(self):
        self.fiducial_array = FiducialArray()
        rospy.Subscriber("fiducial_vertices", FiducialArray, self.getFiducialArray)
        self.pub_fiducial_array_topic = rospy.Publisher('NordSud_topic', Bool, queue_size=1) #topicname + type of topic + nb in queue
    
    def getFiducialArray(self,data):
        self.fiducial_array = data  
        
    def publisher(self, goal):
        goNorth = Bool()
        goNorth.data = goal
        self.pub_fiducial_array_topic.publish(goNorth) #Publication de l'objectif

def main():
    rospy.init_node('aruco_NordSud', anonymous = True)
    aruco = Aruco()
    
    print("="*10 + " Start of aruco detection " + "="*10)
    
    while not rospy.is_shutdown():
        for i in range(len(aruco.fiducial_array.fiducials)):
            if aruco.fiducial_array.fiducials[i].fiducial_id == 17:
                if aruco.fiducial_array.fiducials[i].y0 < aruco.fiducial_array.fiducials[i].y2:
                    goNorth = True
                elif aruco.fiducial_array.fiducials[i].y0 > aruco.fiducial_array.fiducials[i].y2:
                    goNorth = False
    
            print(goNorth)
            aruco.publisher(goNorth) #Demande de publication du nouvel objectif
            sleep(1)
        
    print("="*10 + " End of aruco detection " + "="*10)
    

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass