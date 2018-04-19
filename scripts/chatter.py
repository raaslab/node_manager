#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16 

def talker():
    pub = rospy.Publisher('chatter', Int16, queue_size=10)
    rospy.init_node('chatter', anonymous=False)
    rate = rospy.Rate(10) # 10hz

    starttime = rospy.get_rostime()

    while not rospy.is_shutdown() and (rospy.get_rostime().secs - starttime.secs) < 5:
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        #pub.publish(hello_str)
        pub.publish(10)
        rate.sleep()

    rospy.spin()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
