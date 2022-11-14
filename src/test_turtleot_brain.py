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
from std_msgs.msg import String
from turtlebot_brain import SendGoalClass

class TurtleBotBrainTest(unittest.TestCase):
   
    def test_readGoalsFile(self):
        #Read Correctly goals file
        self.goals_file = '/home/vinu/catkin_ws/src/scf_reto/maps_tb/goals.txt'
        with open(self.goals_file, 'r') as f:
                data = f.read()
        lines = SendGoalClass.read_goals_file(self)
        self.assertEqual(lines,data)
    
    def test_findGoalinLine(self):
        #Find x y ang from line str with name of goal
        lines ="door:-5.3,3.5,3.14\nbookshelf:-6.5,4.3,1.57\nTest:0,0,0\nMenos:-1,-1,1.57"
        goal_name = 'bookshelf'
        x,y,ang = SendGoalClass.getGoalFromDatabase(self,lines,goal_name)
        self.assertEqual(x,-6.5)
        self.assertEqual(y,4.3)
        self.assertEqual(ang,1.57)
        
if __name__ == '__main__':
    unittest.main()