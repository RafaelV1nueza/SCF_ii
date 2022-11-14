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
    # 
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 

        self.pub_quat = rospy.Publisher('vectorPose_UR', Pose, queue_size=1)
        rospy.Subscriber("visp_auto_tracker/object_position", PoseStamped, self.cam_vector)

        self.tag = Pose()
        self.image_flag  = 0

        #********** INIT NODE **********### 
        r = rospy.Rate(2) #1Hz 
        print("Node initialized 2hz")
        while not rospy.is_shutdown(): 
            print('Rotation tf')
            if self.image_flag:
                x = self.tag.orientation.x
                y = self.tag.orientation.y
                z = self.tag.orientation.z
                w = self.tag.orientation.w
                quat = [x,y,z,w]
                print("Quat")
                print(quat)
                print("nega quaternion")
                f = quaternion_multiply(quat,[0, 1, 0, 0])
                inverted = Pose()
                inverted.orientation.x = f[0]
                inverted.orientation.y = f[1]
                inverted.orientation.z = f[2]
                inverted.orientation.w = f[3]
                print(inverted)
                
                self.pub_quat.publish(inverted)
            r.sleep()  #It is very important that the r.sleep function is called at least once every cycle. 

    def cam_vector(self,tag_vector):
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