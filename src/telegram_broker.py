#!/usr/bin/env python 
from os import wait
import rospy 
import time
# Bring in the SimpleActionClient
# Bring in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
from std_msgs.msg import String

import numpy as np 


#Clase para comunicarse con telegram
class TelegramComm(): 
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 
        self.pub_tele = rospy.Publisher('pub_Telegram', String, queue_size=1) #Publish data to telegram
        self.pub_inst = rospy.Publisher('instr_tb', String, queue_size=1) #Publish Instructions to tb node
        rospy.Subscriber("state_tb", String, self.state_tb_callback) #Subscribe to tb state info
        rospy.Subscriber("sub_Telegram", String, self.tlgrm_callback) #Subscribe to telegram instructions
        #********** INIT NODE **********### 
        r = rospy.Rate(2) #1Hz 
        print("Node initialized 2hz")
        #Init var
        self.state = 0
        self.tlgrm_msg = ''
        op = ''
        sent_menu1 = 0
        menu1 = 10
        self.msg_flag = 0
        nc_msg = 0
        resp_1 = 0
        sent_menu2 = 0
        #Do something else
        print('Initializing...')
        time.sleep(3)
        while not rospy.is_shutdown():
            print("""--Telegram Broker v1.0.1--
            Developed by S.T.E.V.E for SCF
    Running...
    Publishing to /pub_Telegram & /inst_tb
    subscribed to /state_tb & /sub_Telegram
    """)
            #self.pub_tele.publish("Robot not conected")
            #Resend Menu
            if self.tlgrm_msg == 'Menu' or self.tlgrm_msg == 'menu':
                sent_menu1 = 0
                sent_menu2 = 0
                self.msg_flag = 0
                self.tlgrm_msg = ''
                print('Displayig menu, again...')
            #First Selection
            if self.msg_flag and not nc_msg:
                if resp_1 == 0:
                    op = self.tlgrm_msg
                    if op == '0' or op == 'D':
                        menu1 = 0
                        resp_1 = 1
                    elif op == '1' or op == 'M':
                        menu1 = 1
                        resp_1 = 1
                    self.tlgrm_msg = ''

                if menu1 == 0:
                    print('definir puntos')
                    if sent_menu2 == 0:
                        pos = []
                        with open('/home/vinu/catkin_ws/src/scf_reto/maps_tb/goals.txt', 'r') as f:
                            lines = f.read()
                        print(lines)
                        self.pub_tele.publish('Las posiciones guardads son:')

                        print('processing...')
                        time.sleep(1)
                        self.pub_tele.publish(lines)
                        time.sleep(1)
                        self.pub_tele.publish("""Escribir una posicion en el formato:
[Nombre]:[X-coord],[Y-coord],[Angulo]""")

                        sent_menu2 = 1

                    ans = self.tlgrm_msg 
                    if ans.count(',')==2 and ans.count(':') == 1:
                        #name:x-coord,y-coord,yaw
                        print('Writing new point')
                        with open('/home/vinu/catkin_ws/src/scf_reto/maps_tb/goals.txt', 'a') as f:
                            f.write(ans+ '\n')
                        self.pub_tele.publish('Pose guardada')
                        sent_menu2 = 0
                        sent_menu1 = 0
                        op = ''
                        menu1 = 10
                        self.msg_flag = 0
                    elif ans != '':
                        sent_menu2 = 0
                    self.tlgrm_msg = ''
                
                elif menu1 == 1:
                    print('Moverse')
                    if sent_menu2 == 0:
                        with open('/home/vinu/catkin_ws/src/scf_reto/maps_tb/goals.txt', 'r') as f:
                            lines = f.read()
                        print(lines)
                        self.pub_tele.publish('Escribir el nombre de una de las posiciones guardadas:')
                        print('processing...')
                        time.sleep(1)
                        self.pub_tele.publish(lines)
                        self.tlgrm_msg = ''
                        sent_menu2 = 1
                    ans = self.tlgrm_msg
                    if lines.find(ans) != -1 and ans !='':
                        time.sleep(1)
                        print('Sending goal to brain')
                        self.pub_inst.publish('1'+ans)
                        print('Sent goal to brain')
                        
                        #self.pub_tele.publish('Objetivo "'+ ans + '" se enviara en 3s...')
                        time.sleep(3)
                        sent_menu2 = 0
                        sent_menu1 = 0
                        op = ''
                        menu1 = 10
                        self.msg_flag = 0
                        print('Objetivo enviado correctamente...')

                
            
            #Display Menu
            else:
                #Send first menu if robot conected
                if sent_menu1 == 0:
                    if self.state == 0:
                        #Send Idle Message
                        self.pub_tele.publish('\U0001F7E9 MENU PRINCIPAL \U0001F7E9 ')
                        time.sleep(2)
                        print('Idle Message')
                        self.pub_tele.publish("""Opciones a realizar:
[0] o [D] Definir puntos \u26F3\uFE0F
[1] o [M] Moverse a un punto \U0001F6F9
[2] o [P] Parar el Robot \U0001F6A8""")
                        nc_msg = 0
                        resp_1 = 0
                    else:
                        print('nc_robot')
                        self.pub_tele.publish("Robot not conected")
                        nc_msg = 1
                    sent_menu1 = 1

            #Send Menu 1 if reconected bot
            if nc_msg and not self.state:
                sent_menu1 = 0
            r.sleep()  #It is very important that the r.sleep function is called at least once every cycle. 

    #Telegram Instruction Arrival
    def tlgrm_callback(self, msg_string):
        self.tlgrm_msg = msg_string.data
        print("Recieved " + self.tlgrm_msg)
        self.msg_flag = 1
        if self.tlgrm_msg == '2' or self.tlgrm_msg == 'P':
            self.pub_inst.publish('2')
            self.tlgrm_msg = ''
            self.pub_tele.publish('Se ha enviado un PARO')
            self.msg_flag = 0
    # Telegram State Arrival
    def state_tb_callback(self, msg_string):
        self.state = int(msg_string.data)
        #print("State: " + str(self.state))   

    def cleanup(self): 
        #This function is called just before finishing the node 
        # You can use it to clean things up before leaving 
        # Example: stop the robot before finishing a node.   
        
        #kill the node
       

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
    rospy.init_node("telegram_broker", anonymous=True) 
    TelegramComm()