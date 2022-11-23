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
# Test for: cam_vec_tran.py                                             #
#                                                                       #
# Version: v1.0.1 (alpha)                                               #
#                                                                       #
# Notes: Test for transformation from quaternion to pose & test for     #
#        transformation fron pose to quaternion vector                  #
#                                                                       #
# Latest edit: vinu                                                     #
#                                                                       #
# Date: 13.11.2022                                                      #
#########################################################################

import unittest
from geometry_msgs.msg import Pose
from cam_vec_tran import CamInfoClass

class QuaternionTestCase(unittest.TestCase):
   
    def test_Quat2Pose(self):
        #Cuaternion como vector a Pose msg
        pose_from_q = CamInfoClass.from_quat2pose(self,[0, 0, 0, 1])
        pose_def = Pose()
        pose_def.orientation.w = 1.0
        self.assertEqual(pose_from_q,pose_def)
        pose_from_q = CamInfoClass.from_quat2pose(self,[-1, 0, 0, 0])
        pose_def = Pose()
        pose_def.orientation.x = -1.0
        self.assertEqual(pose_from_q,pose_def)

    def test_Pose2Quat(self):
        # Pose msg a cuaternion como vector
        pose_def = Pose()
        pose_def.orientation.w = 1.0
        pose_from_q = CamInfoClass.from_pose2quat(self,pose_def)
        self.assertEqual(pose_from_q,[0, 0, 0, 1])
        pose_def = Pose()
        pose_def.orientation.y = -1.0
        pose_from_q = CamInfoClass.from_pose2quat(self,pose_def)
        self.assertEqual(pose_from_q,[0, -1, 0, 0])

if __name__ == '__main__':
    unittest.main()