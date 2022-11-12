#!/usr/bin/env python 
import rospy

class TestClass():
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 
        r = rospy.Rate(2) #1Hz 
        print("Node initialized 2hz")
        while not rospy.is_shutdown(): 
            print('Rotation tf')

if __name__ == "__main__": 
    print("Hihi")
    rospy.init_node("test_node", anonymous=True) 
    TestClass()





#!/usr/bin/env python 
#from os import wait
#import os
#import time







# if __name__ == "__main__": 
#     time.sleep(1)
#     print('Initializing Node-Red instance...')
#     proc = os.popen('node-red', 'r')
#     print('Running Node-Red instance...')
#     b = os.popen('ps ax  | grep node-red')
#     print(b)
#     c = b.readlines()
#     d = c[1]
#     n1 = 3
#     n2 = d.find(' ',3)
#     pid = d[n1:n2]
#     print(pid)






# #with open('goals.txt', 'w') as f:


# #    f.write('-1.5,4.5,1.57')
# obj = []
# with open('goals.txt', 'r') as f:
#     lines = f.readlines()
# for line in lines:
#     print(line)
#     a = line.find(':')
#     b = line.find(',')
#     c = line.find(',',(b+1))
#     d = len(line)-1

#     obj = obj + [line]
#     n1 = float(line[int(a+1):int(b)])
#     n2 = float(line[int(b+1):int(c)])
#     n3 = float(line[int(c+1):int(d)])
#     print(n1)
#     print(n2)
#     print(n3)

# print(obj)



