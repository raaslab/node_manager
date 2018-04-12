#!/usr/bin/env python
import rospy
import time 
import os 
from std_msgs.msg import String

lasttime = 0

def callback(data):
	global lasttime
	lasttime = rospy.get_rostime()

def listener():

	rospy.init_node('node_manager', anonymous=True)
	rospy.Subscriber("chatter", String, callback)

	timeout = rospy.get_param('timeout',2)
	
	global lasttime
	lasttime = rospy.get_rostime()

	r = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		now = rospy.get_rostime()

		if (now.secs - lasttime.secs > timeout):
			lasttime = now
			rospy.loginfo("I haven't heard")
			nodes = os.popen("rosnode list").readlines()
			print nodes
			if any("chatter" in s for s in nodes):
				
				os.system(os.path.dirname(os.path.realpath(__file__))+"/killnode.sh")

    		r.sleep()

if __name__ == '__main__':
	listener()
