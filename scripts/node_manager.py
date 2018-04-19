#!/usr/bin/env python
import rospy
import time 
import os 
from rospy.msg import AnyMsg
from std_msgs.msg import Int32

lasttime = 0

def callback(data):
	global lasttime
	lasttime = rospy.get_rostime()

def listener():

	rospy.init_node('node_manager', anonymous=True)
	statustimeout = rospy.get_param('~status_timeout',2)
	killtimeout = rospy.get_param('~kill_timeout',4)
	subtopic = rospy.get_param('~subscribe_to_topic','chatter')
	nodename = rospy.get_param('~node_name','chatter')

	killpub = rospy.Publisher('node_manager/camera_kill',Int32,queue_size=10)

	rospy.loginfo('Subscribing to %s' % subtopic);
	rospy.loginfo('Node that will be managed: %s' % nodename);
	rospy.loginfo('Status message will timeout after: %d secs' % statustimeout);
	rospy.loginfo('Node will be killed after: %d secs' % killtimeout);
	rospy.Subscriber(subtopic, AnyMsg, callback)

	global lasttime
	lasttime = rospy.get_rostime()

	r = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		now = rospy.get_rostime()

		if (now.secs - lasttime.secs > statustimeout):
			rospy.loginfo("node_manager: timeout occurred at %i" % now.secs)
			killpub.publish(1)

			if (now.secs - lasttime.secs > killtimeout):
				lasttime = now
				nodes = os.popen("rosnode list").readlines()
				if any(nodename in s for s in nodes): 
					rospy.loginfo("node_manager: camera_node kill occurred at %i" % now.secs)
					os.system("rosnode kill " + nodename)
		else:
			nodes = os.popen("rosnode list").readlines()
			if any(nodename in s for s in nodes):
				rospy.loginfo("node_manager: camera node is there at %i" % now.secs)
				killpub.publish(0)

    		r.sleep()

if __name__ == '__main__':
	listener()
