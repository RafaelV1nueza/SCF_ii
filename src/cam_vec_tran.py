import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
import numpy as np 



def cam_info(self, x_goal, y_goal, yaw):
        # Creates a new goal with the MoveBaseGoal constructor
        # it receives x_goal and y_goal [m] and yaw [rad]
        # All the coordinates are measured with respect to the "/map" frame. 
        # It returns a MoveBaseGoal pose.
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "/map"
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