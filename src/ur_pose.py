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
from geometry_msgs.msg import Pose
class RobotPositionClass():
    """This class will publish the translation values from UR robot to use with camera node"""
    def __init__(self):
        """Init""" 
        #rospy.on_shutdown(self.cleanup) 
        r = rospy.Rate(2) #1Hz
            #-----------------------SUBSCRIBERS---------------------
        rospy.Subscriber("/tf", TFMessage, self.pos_robot_cb)     #Vector de posicion del robot UR
        pose_pub = rospy.Publisher('pose_UR',Pose,queue_size=1) 
        print("Node initialized 2hz")
        self.flag01=0
        while not rospy.is_shutdown(): 
            print('Pose UR')
            if self.flag01:
                pose_pub.publish(self.new_pose)
            r.sleep()
        
    def pos_robot_cb(self, vector_robot):
        """Returns a translation values from UR Robot"""
        self.new_pose = Pose() 
        self.new_pose.position.x = vector_robot.transforms[0].transform.translation.x
        print("Pose x: ", self.new_pose.position.x)
        self.new_pose.position.y = vector_robot.transforms[0].transform.translation.y
        print("Pose y: ", self.new_pose.position.y)
        self.new_pose.position.z = vector_robot.transforms[0].transform.translation.z
        print("Pose z: ", self.new_pose.position.z)

if __name__ == "__main__": 
    print("Hihi")
    rospy.init_node("test_node", anonymous=True) 
    RobotPositionClass()