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
# Maintainer:vinu/josh                                                  #
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

import sys

import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from controller_manager_msgs.srv import SwitchControllerRequest, SwitchController
from controller_manager_msgs.srv import LoadControllerRequest, LoadController
from controller_manager_msgs.srv import ListControllers, ListControllersRequest
import geometry_msgs.msg as geometry_msgs
from cartesian_control_msgs.msg import (
    FollowCartesianTrajectoryAction,
    FollowCartesianTrajectoryGoal,
    CartesianTrajectoryPoint,
)

JOINT_NAMES = [
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
]
JOINT_TRAJECTORY_CONTROLLERS = [
    "scaled_pos_joint_traj_controller",
    "scaled_vel_joint_traj_controller",
    "pos_joint_traj_controller",
    "vel_joint_traj_controller",
    "forward_joint_traj_controller",
]
CARTESIAN_TRAJECTORY_CONTROLLERS = [
    "pose_based_cartesian_traj_controller",
    "joint_based_cartesian_traj_controller",
    "forward_cartesian_traj_controller",
]
CONFLICTING_CONTROLLERS = ["joint_group_vel_controller", "twist_controller"]

class AdjustRobotClass():
    """Class to Move Ur Position reading from pose and rotation topic"""
    def __init__(self): 
        
        rospy.on_shutdown(self.cleanup) 
        rospy.Subscriber("vector_UR", Pose, self.vector_ur_cb)
        rospy.Subscriber("pose_UR", Pose, self.pose_ur_cb)
        
        timeout = rospy.Duration(5)
        self.switch_srv = rospy.ServiceProxy(
            "controller_manager/switch_controller", SwitchController
        )

        self.load_srv = rospy.ServiceProxy("controller_manager/load_controller", LoadController)
        self.list_srv = rospy.ServiceProxy("controller_manager/list_controllers", ListControllers)
        try:
            self.switch_srv.wait_for_service(timeout.to_sec())
        except rospy.exceptions.ROSException as err:
            rospy.logerr("Could not reach controller switch service. Msg: {}".format(err))
            sys.exit(-1)

        self.joint_trajectory_controller = JOINT_TRAJECTORY_CONTROLLERS[0]
        self.cartesian_trajectory_controller = CARTESIAN_TRAJECTORY_CONTROLLERS[0]

        self.sep_const = 0.2 ##20cm de separacion
        self.pose_flag = 0
        self.vector_flag  = 0

        controller_selec = self.choose_controller()
        
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
                    self.send_cartesian_trajectory(poseP,poseR)
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

    def choose_controller(self):
        """Ask the user to select the desired controller from the available list."""
        #Show controller list
        rospy.loginfo("Available trajectory controllers:")
        for (index, name) in enumerate(JOINT_TRAJECTORY_CONTROLLERS):
            rospy.loginfo("{} (joint-based): {}".format(index, name))
        for (index, name) in enumerate(CARTESIAN_TRAJECTORY_CONTROLLERS):
            rospy.loginfo("{} (Cartesian): {}".format(index + len(JOINT_TRAJECTORY_CONTROLLERS), name))
        #Allow user input
        choice = -1
        while choice < 0:
            #input_str = input(
            #    "Please choose a controller by entering its number (Enter '0' if "
            #    "you are unsure / don't care): "
            #)
            input_str = '6'
            try:
                choice = int(input_str)
                if choice < 0 or choice >= len(JOINT_TRAJECTORY_CONTROLLERS) + len(
                    CARTESIAN_TRAJECTORY_CONTROLLERS
                ):
                    rospy.loginfo(
                        "{} not inside the list of options. "
                        "Please enter a valid index from the list above.".format(choice)
                    )
                    choice = -1
            except ValueError:
                rospy.loginfo("Input is not a valid number. Please try again.")
        if choice < len(JOINT_TRAJECTORY_CONTROLLERS):
            self.joint_trajectory_controller = JOINT_TRAJECTORY_CONTROLLERS[choice]
            return "joint_based"

        self.cartesian_trajectory_controller = CARTESIAN_TRAJECTORY_CONTROLLERS[
            choice - len(JOINT_TRAJECTORY_CONTROLLERS)
        ]
        return "cartesian"

    def send_cartesian_trajectory(self, Pose, Rotation):
        """Creates a Cartesian trajectory and sends it using the selected action server"""
        self.switch_controller(self.cartesian_trajectory_controller)

        # make sure the correct controller is loaded and activated
        goal = FollowCartesianTrajectoryGoal()
        trajectory_client = actionlib.SimpleActionClient(
            "{}/follow_cartesian_trajectory".format(self.cartesian_trajectory_controller),
            FollowCartesianTrajectoryAction,
        )

        # Wait for action server to be ready
        timeout = rospy.Duration(5)
        if not trajectory_client.wait_for_server(timeout):
            rospy.logerr("Could not reach controller action server.")
            sys.exit(-1)

        # The following list are arbitrary positions
        # Change to your own needs if desired
        
        pose_list = [
            geometry_msgs.Pose(
                geometry_msgs.Vector3(0.132, 0.579, 0.496), geometry_msgs.Quaternion(0, 0.7071068, 0.7071068, 0)
            ),
            geometry_msgs.Pose(
                geometry_msgs.Vector3(Pose[0], Pose[1], Pose[2]), geometry_msgs.Quaternion(Rotation[0], Rotation[1], Rotation[2], Rotation[3])
            )
        ]
        duration_list = [10.0, 10.0]
        for i, pose in enumerate(pose_list):
            point = CartesianTrajectoryPoint()
            point.pose = pose
            point.time_from_start = rospy.Duration(duration_list[i])
            goal.trajectory.points.append(point)

    def switch_controller(self, target_controller):
        """Activates the desired controller and stops all others from the predefined list above"""
        other_controllers = (
            JOINT_TRAJECTORY_CONTROLLERS
            + CARTESIAN_TRAJECTORY_CONTROLLERS
            + CONFLICTING_CONTROLLERS
        )
		#from other controllers remove the selected controller
        other_controllers.remove(target_controller)
		
        srv = ListControllersRequest()
        response = self.list_srv(srv)
        for controller in response.controller:
            if controller.name == target_controller and controller.state == "running":
                return

        srv = LoadControllerRequest()
        srv.name = target_controller
        self.load_srv(srv)

        srv = SwitchControllerRequest()
        srv.stop_controllers = other_controllers
        srv.start_controllers = [target_controller]
        srv.strictness = SwitchControllerRequest.BEST_EFFORT
        self.switch_srv(srv)

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
    
    AdjustRobotClass()