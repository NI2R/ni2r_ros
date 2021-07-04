#!/usr/bin/env python
# -*-coding:Latin-1 -*
import rospy
from std_msgs.msg import Header, Time, Bool
from fiducial_msgs.msg import FiducialArray, Fiducial

class Aruco:
    def __init__(self):
        rospy.Subscriber("aruco_detect", FiducialArray, self.getFiducialArray)
        #self.pub_fiducial_array_topic = rospy.Publisher(self.dummy_fiducial,FiducialArray, queue_size=1)
 
    def getFiducialArray(self,data):
        self.fiducial_array = data
        #self.goNorth_array = []
        
        """
        if fiducial_array.fiducials[3].y0 < fiducial_array.fiducials[7].y2:
            self.goNorth = True
            #print("Go North!")
        elif fiducial_array.fiducials[3].y0 > fiducial_array.fiducials[7].y2:
            self.goNorth = False
            #print("Go South!")
        #goNorth_array.append(goNorth)
        """  
        
        return self.fiducial_array, True #goNorth_array   
    
    """
    def parkingFound():
        result = Bool()
        aruco_tags,north = getFiducialArray()
        if aruco_tags[1]:
            result.data = True
        else:
            result.data = False
            return result          
    """


def main():
    rospy.init_node('aruco_NordSud', anonymous = True)
    aruco = Aruco()
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    print("="*10 + " Start of aruco detection " + "="*10)
        
    #wait 20 or 30 seconds first in order to read the permanent orientation of the tag    
    #while(not(parkingFound())):
    
    aruco.getFiducialArray(data)

    """
    for i in range(len(aruco.fiducials)):
        print("x0:", aruco.fiducials[i].x0)
        print("y0:", aruco.fiducials[i].y0)
    
    #Erreur affiche : AttributeError: 'Aruco' object has no attribute 'fiducials'
    """
    
                
    #print(goNorth)
        
    print("="*10 + " End of aruco detection " + "="*10)
    

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass