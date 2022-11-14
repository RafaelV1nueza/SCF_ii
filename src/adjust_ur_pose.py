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
import time
from geometry_msgs.msg import Pose
from collabROB_brain import TrajectoryClient

class AdjustPoseClass():
    """Class to Adjust Ur Position reading from pose and rotation topic"""
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 
        rospy.Subscriber("vector_UR", Pose, self.vector_ur_cb)
        rospy.Subscriber("pose_UR", Pose, self.pose_ur_cb)
        
        self.pose_flag = 0
        self.vector_flag  = 0

        #********** INIT NODE **********### 
        r = rospy.Rate(2) #1Hz 
        print("Node initialized 2hz")
        while not rospy.is_shutdown(): 
            print('While loop')
            if self.vector_flag and self.pose_flag:
                print("Sup")
                print("Actual Pose")
                print(self.robot_pose)
                poses = self.calc_new_pose(self.robot_pose,self.image_info)
                print()
                
            else:
                print("Either pose or rot not recieved")

            r.sleep()  #It is very important that the r.sleep function is called at least once every cycle. 

    def calc_new_pose(self,ur_pose,img_info):
        """"Dessc"""
        
        new_pose = [(ur_pose.position.x-img_info.position.x), (ur_pose.position.y-img_info.position.z+0.2), (ur_pose.position.z-img_info.position.y)]

        return new_pose

    def vector_ur_cb(self,rot_pose):
        """Desc"""
        self.image_info = rot_pose
        print('Recieved Image Pose')
        self.vector_flag = 1

    def pose_ur_cb(self,pose_pose):
        """Desc"""
        self.robot_pose = pose_pose
        print('Recieved Vector Pose')
        self.pose_flag = 1

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