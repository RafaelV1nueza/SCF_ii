#!/usr/bin/env python
# ---------------------------------------------------------------------
import rospy
#from geometry_msgs.msg import TransformStamped
from tf2_msgs.msg import TFMessage

class TestClass():
    def __init__(self): 
        #rospy.on_shutdown(self.cleanup) 
        r = rospy.Rate(2) #1Hz
            #-----------------------SUBSCRIBERS---------------------
        rospy.Subscriber("/tf", TFMessage, self.pos_robot_cb)     #Vector de posicion del robot UR 
        print("Node initialized 2hz")
        while not rospy.is_shutdown(): 
            print('Rotation tf')

            r.sleep()
        
    def pos_robot_cb(self, vector_robot):
        #vector_robot = TFMessage()
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