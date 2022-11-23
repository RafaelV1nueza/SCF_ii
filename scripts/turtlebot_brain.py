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
# File Name: turtlebot_brain.py                                         #
#                                                                       #
# Maintainer: vinu                                                      #
#                                                                       #
# Version: v1.0.2 (alpha)                                               #
#                                                                       #
# Notes: Turtlebot goal sender ROS node, uses defined goals contained in#
#       goals.txt inside maps_tb dir. Recieves instr form ROS node. Can #
#       cancel goals.                                                   #
#                                                                       #
# Latest edit: vinu                                                     #
#                                                                       #
# Date: 14.11.2022                                                      #
#########################################################################

from os import wait
import rospy 
# Bring in the SimpleActionClient
import actionlib
# Bring in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
from std_msgs.msg import String

import numpy as np 
import time

#This class will publish a navigation goal to the ros_navigation_stack
class SendGoalClass(): 
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 
        #Create action client
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        # Wait until the action server has started up and started listening for goals.
        print("Waiting for Server . . . .")
        self.client.wait_for_server()
        print("Server Online. . . .")

        #Publishers and Subscribers
        self.pub_state = rospy.Publisher('state_tb', String, queue_size=1) 
        rospy.Subscriber("instr_tb", String, self.instr_tb_callback) 

        #********** INIT NODE **********### 
        r = rospy.Rate(2) #1Hz 
        print("Node initialized 2hz")

        #Init Variables
        
        i = 0
        self.instFlag = 0
        self.action = 10
        goalSent = 0

        self.placeFlag = 0
        self.msg_ask = 0
        self.msg_av =0

        self.goals_file = '/home/vinu/catkin_ws/src/scf_reto/maps_tb/goals.txt'

        # Define Goals
        #Read Goal file
        lines = self.read_goals_file
        print('Posiciones:')
        for line in lines:
            print(line)

        
        #While loop
        while not rospy.is_shutdown(): 
            i = i+1
            print("""Turtlebot Brain v1.0.1
Developed by S.T.E.V.E for SCF
    Status:
        Running
    Connected to:
        Turtlebot2 @ 192.168.0.112
    Managed from:
        192.168.0.11
    Subscribed to:
        /instr_tb
    Publishes to:
        /state_tb
    Relays to:
        actionlib.SimpleActionClient: move_base

    ----- Now you can use it... -----
            """)
            print("+ Iteration [2Hz]: " +str(i))

            if self.placeFlag:
                print("+ Goal: " + self.where)
                if goalSent == 0:
                    print("+ Sending goal ...")
                    self.client.send_goal(self.goal, feedback_cb = self.my_feedback_cb)
                    goalSent = 1
                else:
                    print("+ Goal Sent ...")

                print("+ Estado de el objetivo: " + str(self.client.get_state() ))
                
                if self.client.get_state() == 3:
                    goalSent = 0
                    av = "+ I arrived to " + self.where
                    print(av)
                    print("X: "+ str(self.poseX))

                    print("Y: "+ str(self.poseY))
                    
                
                    self.placeFlag = 0
                        
                else:
                    print("+ Working on it")
                
            else:
                print("No goal")
                self.pub_state.publish("0")

            if self.instFlag:
                self.placeFlag = 0
            
                if self.action == 1:
                    print('Going somewhere...')
                    self.placeFlag = 1
                    self.instFlag = 0

                elif self.action == 2:
                    print('Deteniendo Robot')
                    self.client.cancel_all_goals()
                    self.instFlag = 0
                    goalSent = 0
            
            r.sleep()  #It is very important that the r.sleep function is called at least once every cycle. 

    def read_goals_file(self):
        with open(self.goals_file, 'r') as f:
                lines = f.read()
        return lines

    def getGoalFromDatabase(self,lines,goal_name):
        a = 1
        b = len(goal_name)
        self.where = (goal_name[a:b])
        c = lines.find(goal_name[a:b])
        d = lines.find(',',c+b)
        x=float(lines[c+b:d])
        e = lines.find(',',d+1)
        y= float(lines[d+1:e])
        f = lines.find('\n',e+1)
        ang=float(lines[e+1:f])
        return x,y,ang

    def instr_tb_callback(self, msg_string):
        
        self.inst = msg_string.data
        print("Recieved: " + self.inst)
        
        if self.inst[0] == '1':
            #Moverse a un punto
            print('Place')
            self.action = 1
            lines = self.read_goals_file()
            goal_name = self.inst
            x,y,ang = self.getGoalFromDatabase(lines,goal_name)

            self.goal = self.set_goal(x,y,ang)

            #hacer cosas de place
        elif self.inst[0] == '2':
            #Parar el robot
            print('Detener')
            self.action = 2
        else:
            print('Error: Invalid Instruction')
            self.action = 10
        self.instFlag = 1

    def my_feedback_cb(self, robot_pose):

        #print("Feedback cb")
        #print(robot_pose)
        self.poseX = robot_pose.base_position.pose.position.x
        self.poseY = robot_pose.base_position.pose.position.y #current robot pose
        x = robot_pose.base_position.pose.orientation.x
        y = robot_pose.base_position.pose.orientation.y
        z = robot_pose.base_position.pose.orientation.z
        w = robot_pose.base_position.pose.orientation.w
        angles = euler_from_quaternion([x,y,z,w])
        self.yaw = angles[0]
        self.feedback_flag = 1
   
    def set_goal(self, x_goal, y_goal, yaw):
        # Creates a new goal with the MoveBaseGoal constructor
        # it receives x_goal and y_goal [m] and yaw [rad]
        # All the coordinates are measured with respect to the "map" frame. 
        # It returns a MoveBaseGoal pose.
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        # Position
        goal.target_pose.pose.position.x = x_goal
        goal.target_pose.pose.position.y = y_goal
        # Rotation of the mobile base frame w.r.t. "map" frame as a quaternion
        quat = quaternion_from_euler(0,0,yaw)
        goal.target_pose.pose.orientation.x = quat[0]
        goal.target_pose.pose.orientation.y = quat[1]
        goal.target_pose.pose.orientation.z = quat[2]
        goal.target_pose.pose.orientation.w = quat[3]
        return goal
    
    def cleanup(self): 
        #This function is called just before finishing the node 
        # You can use it to clean things up before leaving 
        # Example: stop the robot before finishing a node.   
        
        #kill the robot
        self.client.cancel_all_goals()

        print("---------------xxxxx-------------------Ded")
        print("                  __")
        print("     w  c(..)o   (")
        print("      \__(-)    __)")
        print("          /\   (")
        print("         /(_)___)")
        print("         w /|")
        print("          | |")
        print("Vinu     m  m")    
############################### MAIN PROGRAM #################################### 
if __name__ == "__main__": 
    rospy.init_node("tb_brain", anonymous=True) 
    SendGoalClass()