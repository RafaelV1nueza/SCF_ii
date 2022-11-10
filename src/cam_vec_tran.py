import rospy
from geometry_msgs.msg import Pose
from tf.transformations import quaternion_from_euler

import numpy as np 

class CamInfoClass():
    # 
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 
        
        self.pub_state = rospy.Publisher('vectorPose_UR', Pose, queue_size=1)
        rospy.Subscriber("visp_auto_tracker/object_position", Pose, self.cam_vector)

        self.tag = Pose()

        #********** INIT NODE **********### 
        r = rospy.Rate(2) #1Hz 
        print("Node initialized 2hz")

        
    def cam_vector(self,tag_vector):
        self.tag = tag_vector.pose

        print('Recieved Vector Pose')



    def cleanup(self): 
        #This function is called just before finishing the node 
        # You can use it to clean things up before leaving 
        # Example: stop the robot before finishing a node.   
        
        #kill the robot
        print("---------------xxxxx-------------------Ded")
        print("                  __")
        print("     w  c(..)o   (")
        print("      \__(-)    __)")
        print("          /\   (")
        print("         /(_)___)")
        print("         w /|")
        print("          | |")
        print("Vinu     m  m")    

if __name__ == "__main__": 
    print("Hihi")
    rospy.init_node("tag_vecTf", anonymous=True) 
    CamInfoClass()