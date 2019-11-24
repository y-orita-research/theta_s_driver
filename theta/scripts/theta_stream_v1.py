#!/usr/bin/env python

#
# author: Yasuaki Orita
#

import io
import json
import inspect
import time
import cv2
import numpy as np
import requests
import signal
import sys

import roslib
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


frameRate = 10

#theta URL
url = 'http://192.168.1.1:80/osc/commands/execute'

#ROS Publisher
image_pub = rospy.Publisher("theta/image_raw/equirectangular", Image, queue_size=1)
bridge = CvBridge()



def handler(signal, StackFrame):
    print("Shutting down by user keybord operation ...")
    sys.exit(0)


def startSession():
    j = {'name': 'camera.{}'.format(inspect.currentframe().f_code.co_name), 'parameters': {}}
    res = requests.post(url, data=json.dumps(j))
    print("---Start session with following ID---")
    print(res.json())
    return res.json()


def _getLivePreview(id):
    global image_pub
    global bridge

    j = {'name': 'camera.{}'.format(inspect.currentframe().f_code.co_name), 'parameters': {'sessionId': id}}
    res = requests.post(url, data=json.dumps(j), stream=True)

    bytes = b''
    rate = rospy.Rate(frameRate)

    for byteData in res.iter_content(chunk_size=1024):
        bytes += byteData
        s = bytes.find(b'\xff\xd8')
        e = bytes.find(b'\xff\xd9')
        if s != -1 and e != -1:
            jpg = bytes[s:e+2]
            bytes = bytes[e+2:]
            try:
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                i_msg = bridge.cv2_to_imgmsg(i, "bgr8")
                i_msg.header.stamp = rospy.get_rostime()
                image_pub.publish(i_msg)
                print("Publish equirectangular image")
            except:
                print("OpenCV Error")
            rate.sleep()

    return res.json()


def closeSession(id):
    j = {'name': 'camera.{}'.format(inspect.currentframe().f_code.co_name), 'parameters': {'sessionId': id}}
    res = requests.post(url, data=json.dumps(j))
    print("---Close session---")
    print(res.json())
    return res.json()




def main():
    signal.signal(signal.SIGINT, handler)

    #ROS node Initialization
    rospy.init_node('THETA_publisher', anonymous=True)

    #Start a session between THETA and PC
    d = startSession()
    if d['state'] == 'error':
        return closeSession('SID_001')

    # start streaming equ. image 
    id = d['results']['sessionId']
    img = _getLivePreview(id)

    #Close the session
    closeSession(id)
    
    
if __name__ == '__main__':
    main()
