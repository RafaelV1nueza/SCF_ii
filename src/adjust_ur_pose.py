#!/usr/bin/env python 

#########################################################################
#   _________  ___________ ___________ ____   ____ ___________          #
#  /   _____/  \__    ___/ \_   _____/ \   \ /   / \_   _____/          #
#  \_____  \     |    |     |    __)_   \   Y   /   |    __)_           #
#  /        \    |    |     |        \   \     /    |        \          #
# /_______  / /\ |____| /\ /_______  / /\ \___/ /\ /_______  / /\       #
#         \/  \/        \/         \/  \/       \/         \/  \/       #
#                                                                       #
#########################################################################
#                                                                       #
# File Name: adjust_ur_pose.py                                          #
#                                                                       #
# Maintainer:vinu                                                       #
#                                                                       #
# Version: v1.0.1 (alpha)                                               #
#                                                                       #
# Notes: Recieves a quaternion from a topic and inverts x and z axes,   #
#        Efective 180 degree rotation y axis from orientation ref.      #
#                                                                       #
#                                                                       #
# Latest edit: vinu                                                     #
#                                                                       #
# Date: 13.11.2022                                                      #
#########################################################################

import rospy
from geometry_msgs.msg import Pose
from collabROB_brain import TrajectoryClient

class AdjustPoseClass():
    """Class to Adjust Ur Position reading from pose and rotation topic"""
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 
        rospy.Subscriber("vector_UR", Pose, self.vector_ur_cb)
        rospy.Subscriber("visp_auto_tracker/object_position", PoseStamped, self.cam_vector)

        self.tag = Pose()
        self.image_flag  = 0

        #********** INIT NODE **********### 
        r = rospy.Rate(2) #1Hz 
        print("Node initialized 2hz")
        while not rospy.is_shutdown(): 
            print('Rotation tf')
            if self.image_flag:
                quat = self.from_pose2quat(self.tag)
                print("Recieved Quaternion:")
                print(quat)
                print("Inverted QUaternion:")
                f = quaternion_multiply(quat,[0, 1, 0, 0])
                inverted = self.from_quat2pose(f)
                print(inverted)
                
                self.pub_quat.publish(inverted)
            r.sleep()  #It is very important that the r.sleep function is called at least once every cycle. 

    def vector_ur_cb(self,rot_pose):
        """Desc"""
        self.tag = tag_vector.pose
        print('Recieved Vector Pose')
        self.image_flag = 1

    def cleanup(self): 
        
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

    rospy.init_node("adjust_pose_node", anonymous=True) 
    AdjustPoseClass()