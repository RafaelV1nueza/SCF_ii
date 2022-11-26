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
# Date: 26.11.2022                                                      #
#########################################################################

import rospy
import time

import sys
import actionlib
from controller_manager_msgs.srv import SwitchControllerRequest, SwitchController
from controller_manager_msgs.srv import LoadControllerRequest, LoadController
from controller_manager_msgs.srv import ListControllers, ListControllersRequest
import geometry_msgs.msg as geometry_msgs
from cartesian_control_msgs.msg import (
    FollowCartesianTrajectoryAction,
    FollowCartesianTrajectoryGoal,
    CartesianTrajectoryPoint,
)

from geometry_msgs.msg import Pose
##from collabROB_brain import TrajectoryClient

#All controllers to stop conflicting
CARTESIAN_TRAJECTORY_CONTROLLERS = [
    "pose_based_cartesian_traj_controller",
    "joint_based_cartesian_traj_controller",
    "forward_cartesian_traj_controller",
]
JOINT_TRAJECTORY_CONTROLLERS = [
    "scaled_pos_joint_traj_controller",
    "scaled_vel_joint_traj_controller",
    "pos_joint_traj_controller",
    "vel_joint_traj_controller",
    "forward_joint_traj_controller",
]
CONFLICTING_CONTROLLERS = ["joint_group_vel_controller", "twist_controller"]


class AdjustPoseClass():
    """Class to Adjust Ur Position reading from pose and rotation topic"""
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 
        rospy.loginfo("Starting Init ...")
        #Read controller switch service
        rospy.loginfo("Read controller switch service")
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

        #Select/Switch Controller
        rospy.loginfo("Select/switch controller")
        self.carte_traj_controller = CARTESIAN_TRAJECTORY_CONTROLLERS[1] #Controlador 6 aqui se cambia
        self.switch_controller(self.carte_traj_controller) 

        #Action lib Client
        rospy.loginfo("Action lib client")
        goal = FollowCartesianTrajectoryGoal() #Create empty goal
        trajectory_client = actionlib.SimpleActionClient(
            "{}/follow_cartesian_trajectory".format(self.cartesian_trajectory_controller),
            FollowCartesianTrajectoryAction,
        )
        # Wait for action server to be ready
        rospy.loginfo("Waiting for action server to be ready...")
        timeout = rospy.Duration(5)
        if not trajectory_client.wait_for_server(timeout):
            rospy.logerr("Could not reach controller action server.")
            sys.exit(-1)

        #Subscriber
        rospy.loginfo("Starting subscribers")
        rospy.Subscriber("vector_UR", Pose, self.vector_ur_cb)
        rospy.Subscriber("pose_UR", Pose, self.pose_ur_cb)
        
        #Flags and constants
        self.sep_const = 0.2 ##20cm de separacion
        self.pose_flag = 0
        self.vector_flag = 0

        ###********** INIT NODE **********### 
        r = rospy.Rate(0.2) #1Hz 
        print("Node initialized 0.2hz")
        while not rospy.is_shutdown(): 
            print('While loop')
            if self.vector_flag and self.pose_flag:
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
                    goal = FollowCartesianTrajectoryGoal() #Create empty goal
                    pose_list = [
                        geometry_msgs.Pose(
                            geometry_msgs.Vector3(poseP[0], poseP[1], poseP[2]), geometry_msgs.Quaternion(poseR[0], poseR[1], poseR[2], poseR[3])
                            )
                        ]
                    duration_list = [10.0]
                    for i, pose in enumerate(pose_list):
                        point = CartesianTrajectoryPoint()
                        point.pose = pose
                        point.time_from_start = rospy.Duration(duration_list[i])
                        goal.trajectory.points.append(point)

                    self.ask_confirmation(pose_list)
                    rospy.loginfo(
                        "Executing trajectory using the {}".format(self.cartesian_trajectory_controller)
                    )
                    trajectory_client.send_goal(goal)
                    trajectory_client.wait_for_result()

                    result = trajectory_client.get_result()

                    rospy.loginfo("Trajectory execution finished in state {}".format(result.error_code))

                    print('Successful..')

                elif user_input in ['N','n','NO','no','No','Nope','nopis']:
                    print('ok..Waiting for new data poses')
                    self.vector_flag = 0
                    self.pose_flag = 0
                    goal = FollowCartesianTrajectoryGoal()

                else:
                    print('Unselected & Waiting for new data poses')
                
            else:
                if not self.vector_flag:
                    print("No image pose recieved")
                if not self.pose_flag:
                    print("No robot pose recieved")

                print("Either pose or rot not recieved")

            r.sleep()  #It is very important that the r.sleep function is called at least once every cycle. 

    def calc_new_pose(self,ur_pose,img_info):
        """"Compute new pose from og robot pose and diferential pose from img"""
        new_pose = [(ur_pose.position.x+img_info.position.x), (ur_pose.position.y-img_info.position.z+self.sep_const), (ur_pose.position.z-img_info.position.y)]
        newRot = [img_info.orientation.x, img_info.orientation.y, img_info.orientation.z, img_info.orientation.w]
        return new_pose,newRot

    def vector_ur_cb(self,rot_pose):
        """Returns pose + rot from image info"""
        self.image_info = rot_pose
        if not self.vector_flag:
            print('    Recieved Image Pose')
        self.vector_flag = 1

    def pose_ur_cb(self,pose_pose):
        """Returns pose + rot fron ur pose topic"""
        self.robot_pose = pose_pose
        if not self.pose_flag:
            print('    Recieved Vector Pose')
        self.pose_flag = 1

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

    def ask_confirmation(self, waypoint_list):
        """Ask the user for confirmation. This function is obviously not necessary, but makes sense
        in a testing script when you know nothing about the user's setup."""
        rospy.logwarn("The robot will move to the following waypoints: \n{}".format(waypoint_list))
        confirmed = False
        valid = False
        while not valid:
            input_str = input(
                "Please confirm that the robot path is clear of obstacles.\n"
                "Keep the EM-Stop available at all times. You are executing\n"
                "the motion at your own risk. Please type 'y' to proceed or 'n' to abort: "
            )
            valid = input_str in ["y", "n"]
            if not valid:
                rospy.loginfo("Please confirm by entering 'y' or abort by entering 'n'")
            else:
                confirmed = input_str == "y"
        if not confirmed:
            rospy.loginfo("Exiting as requested by user.")
            self.vector_flag = 0
            self.pose_flag = 0
            return
            
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