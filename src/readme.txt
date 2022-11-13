a

#TurtleBot Bringup
ssh ubuntu@192.168.0.112
p:$ turtlebot
roslaunch turtlebot3_bringup turtlebot3_robot.launch

#Turtlebot Remote Bringup - Roscore
roslaunch turtlebot3_bringup turtlebot3_remote.launch

#Rviz Navigation
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/catkin_ws/src/scf_reto/src/maps_tb/r2d2_map.yaml

#Node Red
rosrun scf_reto node_red_run.py 

#Telegram Broker
rosrun scf_reto telegram_broker.py

#Tb_Brain
rosrun scf_reto reto_rob_mov.py 

Header for files


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
# File Name: file.py                                                    #
#                                                                       #
# Maintainer:user,user1                                                 #
#                                                                       #
# Version: v1.0.1 (alpha)                                               #
#                                                                       #
# Notes:                                                                #
#                                                                       #
#                                                                       #
#########################################################################
