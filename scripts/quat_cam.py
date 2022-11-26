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
# File Name: quat_cam.py                                                #
#                                                                       #
# Maintainer:vinu,                                                      #
#                                                                       #
# Version: v1.0.2 (alpha)                                               #
#                                                                       #
# Notes: my sanity is gone                                              #
#                                                                       #
#                                                                       #
# Latest edit: vinu                                                     #
#                                                                       #
# Date: 26.11.2022                                                      #
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
        rospy.Subscriber("visp_auto_tracker/status", PoseStamped, self.tag_status)

        self.tag = Pose()
        self.image_flag  = 0

        #********** INIT NODE **********### 
        r = rospy.Rate(2) #1Hz 
        print("Node initialized 2hz")
        while not rospy.is_shutdown(): 
            print('Rotation tf')
            if self.image_flag  and self.status_im != 1:
                quat = self.from_pose2quat(self.tag)
                print("Recieved Quaternion:")
                print(quat)
                print("Recieved Status:")
                print(self.status_im)
                
                q1 = [0,0,0,0]
                q1[0] = np.sign(quat[0])*quat[3]
                q1[1] = np.sign(quat[0])*np.sign(quat[1])*quat[1] 
                q1[2] = np.sign(quat[0])*np.sign(quat[2])*quat[2] 
                q1[3] = abs(quat[0])


                
                #print("Inverted QUaternion:")
                #a = quaternion_multiply(quat,[0, 1, 0, 0])
                #f = quaternion_multiply(a,[0.7071068, 0, 0, 0.7071068])
                rotation = self.from_quat2pose(q1)
                rotation.position = self.tag.position
                print(rotation)
                self.pub_quat.publish(rotation)
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

    def tag_status(self,msg):
        """Recieves status"""
        self.status_im = msg.data

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