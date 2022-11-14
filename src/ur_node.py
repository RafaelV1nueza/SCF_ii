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
# File Name: ur_node.py                                                 #
#                                                                       #
# Maintainer: josh                                                      #
#                                                                       #
# Version: v1.0.1 (alpha)                                               #
#                                                                       #
# Notes: Reads x y and z pose form a tf topic. To add: publish.         #
#                                                                       #
#                                                                       #
#                                                                       #
# Latest edit: vinu                                                     #
#                                                                       #
# Date: 14.11.2022                                                      #
#########################################################################

import rospy
#from geometry_msgs.msg import TransformStamped
from tf2_msgs.msg import TFMessage

class TestClass():
    """This class will publish the translation values from UR robot to use with camera node"""
    def __init__(self):
        """Init""" 
        #rospy.on_shutdown(self.cleanup) 
        r = rospy.Rate(2) #1Hz
            #-----------------------SUBSCRIBERS---------------------
        rospy.Subscriber("/tf", TFMessage, self.pos_robot_cb)     #Vector de posicion del robot UR 
        print("Node initialized 2hz")
        while not rospy.is_shutdown(): 
            print('Rotation tf')

            r.sleep()
        
    def pos_robot_cb(self, vector_robot):
        """Returns a translation values from UR Robot"""
        self.pose_x = vector_robot.transforms[0].transform.translation.x
        print("Pose x: ", self.pose_x)
        self.pose_y = vector_robot.transforms[0].transform.translation.y
        print("Pose y: ", self.pose_y)
        self.pose_z = vector_robot.transforms[0].transform.translation.z
        print("Pose z: ", self.pose_z)

if __name__ == "__main__": 
    print("Hihi")
    rospy.init_node("test_node", anonymous=True) 
    TestClass()