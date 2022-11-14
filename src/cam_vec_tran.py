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
# File Name: cam_vec_tran.py                                            #
#                                                                       #
# Maintainer:vinu,valeria                                               #
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
from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_multiply
import numpy as np 

class CamInfoClass():
    """Class to invert a vector read fron ROS topic"""
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 

        self.pub_quat = rospy.Publisher('vector_UR', Pose, queue_size=1)
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
    def from_pose2quat(self,pose_data):
        """"Returns a quaternion as a vector from a Pose message"""
        x = pose_data.orientation.x
        y = pose_data.orientation.y
        z = pose_data.orientation.z
        w = pose_data.orientation.w
        quat = [x,y,z,w]
        return quat
    def from_quat2pose(self,q):
        """"Returns a pose mesage from a quaternion vector """
        q_pose = Pose()
        q_pose.orientation.x = q[0]
        q_pose.orientation.y = q[1]
        q_pose.orientation.z = q[2]
        q_pose.orientation.w = q[3]
        return q_pose
    def cam_vector(self,tag_vector):
        """Sets self.tag variable with Pose data from a PoseStamped"""
        self.tag = tag_vector.pose
        print('Recieved Vector Pose')
        self.image_flag = 1

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