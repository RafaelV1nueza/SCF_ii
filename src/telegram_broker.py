#!/usr/bin/env python 
from os import wait
import rospy 
import time
#Import Datatypes
from std_msgs.msg import String

#Clase para comunicarse con telegram
class TelegramComm(): 
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) #Definir fucnion de cierre
        self.pub_tele = rospy.Publisher('pub_Telegram', String, queue_size=1) #Publish data to telegram
        self.pub_inst = rospy.Publisher('instr_tb', String, queue_size=1) #Publish Instructions to tb node
        self.pub_ubid = rospy.Publisher('ubidots', String, queue_size=1) #Publish Instructions to tb node
        rospy.Subscriber("state_tb", String, self.state_tb_callback) #Subscribe to tb state info
        rospy.Subscriber("sub_Telegram", String, self.tlgrm_callback) #Subscribe to telegram instructions
        #********** INIT NODE **********### 
        r = rospy.Rate(2) #1Hz 
        print("Node initialized 2hz")
        #Init variables
        self.state = 0      #State recieved variable
        self.tlgrm_msg = '' #Telegram mesage empty variable
        op = ''             #Empty option variable
        sent_menu1 = 0      #Menu1 flag
        menu1 = 10          #Menu1 option
        self.msg_flag = 0   #Telegram message flag
        nc_msg = 0          #NC robot flag
        resp_1 = 0          #Firts answe flag
        sent_menu2 = 0      #Menu2 flag
        posFile = '/home/vinu/catkin_ws/src/scf_reto/maps_tb/goals.txt' #Define psoitions file
        print('Initializing...')
        time.sleep(3)
        #While loop
        while not rospy.is_shutdown():
            print("""--Telegram Broker v1.0.1--
            Developed by S.T.E.V.E for SCF
    Running...
    Publishing to /pub_Telegram & /inst_tb
    subscribed to /state_tb & /sub_Telegram
    """)
            #self.pub_tele.publish("Robot not conected")
            #Resend Menu
            if self.tlgrm_msg in ['Menu','menu']: #If message in list
                sent_menu1 = 0      #Clear menu 1 flag
                sent_menu2 = 0      #Clear menu 2 flag
                self.msg_flag = 0   #Clear Tlgrm meg flag
                resp_1 = 0          #Clear Answer flag
                self.tlgrm_msg = '' #Clear telegram msg
                print('Displayig menu, again...')
            #First Selection
            if self.msg_flag and not nc_msg:        #If msg flag and robot conected
                if resp_1 == 0:                     #Check first answer flag
                    op = self.tlgrm_msg             #Save instruction
                    if op in ['0', 'D', 'd']:       #if instruction in list
                        menu1 = 0                   #Save instruction
                        resp_1 = 1                  #First answer flag
                    elif op in ['1','M','m']:       #If inst in list
                        menu1 = 1                   #Save inst
                        resp_1 = 1                  #First answer flag
                    self.tlgrm_msg = ''             #Empty telegram msg

                if menu1 == 0:                      #Use op instruction
                    print('definir puntos')
                    if sent_menu2 == 0:             #Sent menu 2 flag check
                        #Open position file and read lines
                        with open(posFile, 'r') as f:
                            lines = f.read()
                        print(lines)
                        #Publish positions in telegram DEFINIR PUNTOS
                        # + code for ubidots publish
                        self.pub_tele.publish('Las posiciones guardads son:')
                        print('processing...')
                        time.sleep(1)
                        self.pub_tele.publish(lines)
                        time.sleep(1)
                        self.pub_tele.publish("""Escribir una posicion en el formato:
[Nombre]:[X-coord],[Y-coord],[Angulo]""")

                        sent_menu2 = 1          #Sent menu2 flag

                    ans = self.tlgrm_msg        #Save msg as ans
                    if ans.count(',')==2 and ans.count(':') == 1:   #Validate ans format
                        #name:x-coord,y-coord,yaw
                        print('Writing new point')
                        #open position file and write new line
                        with open(posFile, 'a') as f:
                            f.write(ans+ '\n')
                        self.pub_tele.publish('Pose guardada')  #Publish mesage in telegram
                        sent_menu2 = 0          #Reset menu2 flag
                        sent_menu1 = 0          #Reset Menu1 flag
                        op = ''                 #Clear op var
                        menu1 = 10              #Reset menu1 var
                        self.msg_flag = 0       #Clear msg recieved flag
                    elif ans != '':             #Check for empty answer
                        sent_menu2 = 0          #Resend menu2
                    self.tlgrm_msg = ''         #Empty telegram message
                
                elif menu1 == 1:    #Menu option 1
                    print('Moverse')
                    if sent_menu2 == 0: #Check if menu2 sent
                        #Open position file
                        with open(posFile, 'r') as f:
                            lines = f.read()
                        print(lines)
                        #Publish Positions in telegram
                        # + code for ubidots publish
                        self.pub_tele.publish('Escribir el nombre de una de las posiciones guardadas:')
                        print('processing...')
                        time.sleep(1)
                        self.pub_tele.publish(lines)
                        self.tlgrm_msg = ''     #Clear telegram Message
                        sent_menu2 = 1          #Sent menu1 flag raised
                    ans = self.tlgrm_msg        #Save msg as ans
                    if lines.find(ans) != -1 and ans !='':  #If ans exixts and dif from empty
                        time.sleep(1)
                        print('Sending goal to brain')
                        self.pub_inst.publish('1'+ans)      #Publish goal to brain
                        print('Sent goal to brain')                        
                        time.sleep(3)
                        sent_menu2 = 0              #Clear menu2 flag
                        sent_menu1 = 0              #Clear menu1 flag
                        op = ''                     #Clear op
                        menu1 = 10                  #Reset menu1 value
                        self.msg_flag = 0           #Reset msg flag
                        print('Objetivo enviado correctamente...')
      
            
            #Display Menu
            else:
                #Send first menu if robot conected
                if sent_menu1 == 0:         #Check menu sent flag
                    if self.state == 0:     #Check robot state
                        #Send Menu Message
                        self.pub_tele.publish('\U0001F7E9 MENU PRINCIPAL \U0001F7E9 ')
                        time.sleep(1)
                        print('Idle Message')
                        self.pub_ubid.publish("Menu")
                        time.sleep(1)
                        self.pub_tele.publish("""Opciones a realizar:
[0] o [D] Definir puntos \u26F3\uFE0F
[1] o [M] Moverse a un punto \U0001F6F9
[2] o [P] Parar el Robot \U0001F6A8""")
                        nc_msg = 0      #Reset not conected flag
                    else:
                        print('nc_robot')
                        self.pub_tele.publish("Robot not conected")
                        time.sleep(1)
                        self.pub_ubid.publish("NC_robot")
                        nc_msg = 1      #Raise nc flag
                    sent_menu1 = 1      #Raise sent menu

            #Send Menu 1 if reconected bot
            if nc_msg and not self.state:   #if nc flag raised but state is 0
                sent_menu1 = 0              #Resend menu
            
            r.sleep()  #r sleep for while loop

    #Telegram Instruction Arrival
    def tlgrm_callback(self, msg_string):
        self.tlgrm_msg = msg_string.data            #Save incoming sting
        print("Recieved " + self.tlgrm_msg)         
        self.msg_flag = 1                           #Raice msg recieved flag
        if self.tlgrm_msg in ['2','P','p','paro','parar','stop']:   #Check if stop signal
            self.pub_inst.publish('2')  #Publish stop
            self.tlgrm_msg = ''         #Clear msg
            self.pub_tele.publish('Se ha enviado un PARO')
            self.msg_flag = 0           #Reset msg flag
    # Telegram State Arrival
    def state_tb_callback(self, msg_string):
        self.state = int(msg_string.data)
        #Recive state from robot

    def cleanup(self): 
        #End the function
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