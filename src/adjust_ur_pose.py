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
# Version: v1.0.2 (alpha)                                               #
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
        
        #Init Class from Robot Brain
        client = TrajectoryClient()

        self.sep_const = 0.2 ##20cm de separacion
        self.pose_flag = 0
        self.vector_flag  = 0

        ###********** INIT NODE **********### 
        r = rospy.Rate(0.2) #1Hz 
        print("Node initialized 0.2hz")
        while not rospy.is_shutdown(): 
            print('While loop')
            if self.vector_flag and self.pose_flag:
                print("Sup")
                print("Actual Pose")
                #print(self.robot_pose)
                poseP,poseR = self.calc_new_pose(self.robot_pose,self.image_info)
                print("Actual pose               New Pose:")
                print("X: ",str(self.robot_pose.position.x)," to ", str(poseP[0]))
                print("Y: ",str(self.robot_pose.position.y)," to ",str(poseP[1]))
                print("Z: ",str(self.robot_pose.position.z)," to ",str(poseP[2]))
                print("Atual Pose                New Orientation: ")
                print("X: ",str(self.robot_pose.orientation.x)," to ",str(poseR[0]))
                print("Y: ",str(self.robot_pose.orientation.y)," to ",str(poseR[1]))
                print("Z: ",str(self.robot_pose.orientation.z)," to ",str(poseR[2])) 
                print("W: ",str(self.robot_pose.orientation.w)," to ",str(poseR[3])) 
                user_input = input("Mover el robot a la pose nueva? Y/N: ")
                if user_input in ['Yes', 'Y', 'y', 'si', 'Si', 'yes', 'YES', 'SI', 'sipis','sip']:
                    print('OK moviendo...')
                    print(poseP)
                    print(poseR)
                    client.send_cartesian_trajectory(poseP,poseR)
                    print('Successful..')
                elif user_input in ['N','n','NO','no','No','Nope','nopis']:
                    print('ok..Waiting for new data poses')
                    self.vector_flag = 0
                    self.pose_flag = 0


                else:
                    print('Unselected & Waiting for new data poses')
                
            else:
                print("Either pose or rot not recieved")

            r.sleep()  #It is very important that the r.sleep function is called at least once every cycle. 

    def calc_new_pose(self,ur_pose,img_info):
        """"Compute new pose from og robot pose and diferential pose from img"""
        new_pose = [(ur_pose.position.x+img_info.position.x), (ur_pose.position.y-img_info.position.z+self.sep_const), (ur_pose.position.z-img_info.position.y)]
        newRot = [img_info.orientation.x, img_info.orientation.y, img_info.orientation.z, img_info.orientation.w]
        return new_pose,newRot

    def vector_ur_cb(self,rot_pose):
        """Desc"""
        self.image_info = rot_pose
        if not self.vector_flag:
            print('    Recieved Image Pose')
        self.vector_flag = 1

    def pose_ur_cb(self,pose_pose):
        """Desc"""
        self.robot_pose = pose_pose
        if not self.pose_flag:
            print('    Recieved Vector Pose')
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