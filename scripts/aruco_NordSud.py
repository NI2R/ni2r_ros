#!/usr/bin/env python
# -*-coding:Latin-1 -*
import rospy

from std_msgs.msg import Header, Time, Bool
from fiducial_msgs.msg import FiducialArray, Fiducial

#class Aruco_properties:
#def __init__(self):
 #   self.start = False
    
    #self.pub_fiducial_array_topic = rospy.Publisher(self.dummy_fiducial,FiducialArray, queue_size=1)


def getFiducialArray(self, data):
    fiducial_array = FiducialArray()
    goNorth_array = []
    
    # Header
    fiducial_array.header = Header()
    fiducial_array.header.seq = 42
    fiducial_array.header.stamp = rospy.Time()
    fiducial_array.header.frame_id = "some_frame"
    
    # Image_seq
    fiducial_array.image_seq = 42
    
    # Fiducial
    fiducial_array.fiducials = []
    
    dummy_fiducial = Fiducial()
    dummy_fiducial.fiducial_id = 0
    dummy_fiducial.direction = 0
    dummy_fiducial.x0 = 100.2 
    dummy_fiducial.y0 = 45.0 
    dummy_fiducial.x1 = 150.2 
    dummy_fiducial.y1 = 46.2 
    dummy_fiducial.x2 = 150.1 
    dummy_fiducial.y2 = 80.0 
    dummy_fiducial.x3 = 100.1 
    dummy_fiducial.y3 = 78.8 
    fiducial_array.fiducials.append(dummy_fiducial)
    
#    n_elements = 5
#    inc = 6.1  
#    for i in range(n_elements):
#        dummy_fiducial = Fiducial()
#        dummy_fiducial.fiducial_id = 0
#        dummy_fiducial.direction = 0
#        dummy_fiducial.x0 = 100.2 + inc
#        dummy_fiducial.y0 = 45.0 + inc
#        dummy_fiducial.x1 = 150.2 - inc
#        dummy_fiducial.y1 = 46.2 + inc
#        dummy_fiducial.x2 = 150.1 - inc
#        dummy_fiducial.y2 = 80.0 - inc
#        dummy_fiducial.x3 = 100.1 + inc
#        dummy_fiducial.y3 = 78.8 - inc
#        fiducial_array.fiducials.append(dummy_fiducial)
#        inc = -inc * 1.9 + 0.17
    
    if dummy_fiducial.y0 < dummy_fiducial.y2:
        goNorth = True
        #print("Go North!")
    elif dummy_fiducial.y0 > dummy_fiducial.y2:
        goNorth = False
        #print("Go South!")
    goNorth_array.append(goNorth)
        
    return fiducial_array, goNorth_array #, dummy_fiducial.y0, dummy_fiducial.y2

def parkingFound(self):
    result = Bool()
    aruco_tags = getFiducialArray()
    if aruco_tags[1]:
        result.data = True
    else:
        result.data = False
        return result
    
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)


def main():
    rospy.init_node('aruco_NordSud', anonymous = True)
    rospy.Subscriber("aruco_detect", FiducialArray, callback)
    
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

    print("="*10 + " Start of aruco detection " + "="*10)
        
    #wait 20 or 30 seconds first in order to read the permanent orientation of the tag    
    while(not(parkingFound())):

        aruco_tags,goNorth = getFiducialArray()
        print(aruco_tags)
        print(goNorth)
        
    print("="*10 + " End of aruco detection " + "="*10)
    

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass