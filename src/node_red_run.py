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
# File Name: node_red_run.py                                            #
#                                                                       #
# Maintainer:vinu                                                       #
#                                                                       #
# Version: v1.0.1 (alpha)                                               #
#                                                                       #
# Notes: Runs the NodeRed command in a hidden terminal as an object, to #
#       kill the procces it finds the process id w/ the function ps ax  #
#       | grep node-red. It may contain some bugs. To en an umproperly  #
#       finished process run the command manually and kill the proces   #
#       with the node-red id.                                           #
#                                                                       #
# Latest edit: vinu                                                     #
#                                                                       #
# Date: 13.11.2022                                                      #
#########################################################################

from os import wait
import rospy 
import os
import time
class NodeRedClass():
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 
        time.sleep(1)
        print('Initializing Node-Red instance...')
        proc = os.popen('node-red', 'r')
        print('Running Node-Red instance...')
        b = os.popen('ps ax  | grep node-red')
        print(b)
        c = b.readlines()
        print(c)
        d = c[1]
        print(d)
        n1 = 0
        n2 = d.find(' ',3)
        self.pid = d[n1:n2]
        print(self.pid)
        
        r = rospy.Rate(0.1)
        while not rospy.is_shutdown():
            print("""Node-Red 
    Status: 
    Running... 
    Process number
     """ + self.pid)
            r.sleep()

    def cleanup(self):
        #if not kill
        #use
        #ps ax  | grep node-red
        #and
        #kill pid#
        comm = 'kill '+ str(self.pid)
        print(comm)
        os.popen(comm)
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
    rospy.init_node("nodered_node", anonymous=True) 
    NodeRedClass()