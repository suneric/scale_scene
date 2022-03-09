#!/usr/bin/env python
import rospy
import numpy as np
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CameraInfo, PointCloud2

class NNCamera:
    def __init__(self, topic):
        self.topic = topic
        self.bridge=CvBridge()
        self.sub = rospy.Subscriber(self.topic, Image, self._color_callback)
        self.color = []

    def _color_callback(self, data):
        try:
            self.color = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    def show(self, name):
        cv.namedWindow(name)
        cv.imshow(name, self.color)
        cv.waitKey(3)

if __name__ == '__main__':
    # clean folder for save point cloud file
    rospy.init_node("camera_view_compare", anonymous=True, log_level=rospy.INFO)
    rospy.sleep(2) # wait for other node ready, such a gazebo
    cam1 = NNCamera("/cam1/image_raw")
    cam2 = NNCamera("/cam2/image_raw")
    rate = rospy.Rate(30)
    try:
        while not rospy.is_shutdown():
            if len(cam1.color) > 0:
                cam1.show("cam1")
            if len(cam2.color) > 0:
                cam2.show("cam2")
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
