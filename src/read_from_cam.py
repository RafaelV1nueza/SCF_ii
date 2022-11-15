#!/usr/bin/env python 

import numpy as np
import rospy
import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
video = "/dev/video0"

bridge = CvBridge()
video_capture = cv2.VideoCapture(video)
print("test")

def talker():
    pub = rospy.Publisher('/usb_cam/image_raw',Image,queue_size=1)
    rospy.init_node('vale', anonymous=True)
    rate = rospy.Rate(10)
    print('ros setup')
    while (True):
        print('wile loop')
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Our operations on the frame comes here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        msg = bridge.cv2_to_imgmsg(frame,'bgr8')
        pub.publish(msg)

        #rate.sleep()

# When everything's done, release the capture

if __name__ == '__main__':
    print("init")
    talker()
    print('ded')
    video_capture.release()
    cv2.destroyAllWindows()