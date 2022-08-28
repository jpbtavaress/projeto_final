#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
import math


class Orientation():
    def __init__(self):
        self.tetaCam = 0
        self.tetaObj = 0
        rospy.Subscriber('sonar_data', PointStamped, self.callback)
        rospy.Subscriber('odom', Odometry, self.callback2)
        self.diferenca_angular = rospy.Publisher('diferenca_angular', Float64, queue_size=10)
        
            
    def callback2(self, posicao_absoluta):
        x = posicao_absoluta.pose.pose.orientation.x 
        y = posicao_absoluta.pose.pose.orientation.y
        z = posicao_absoluta.pose.pose.orientation.z
        w = posicao_absoluta.pose.pose.orientation.w
        yaw_z = self.euler_from_quaternion( x, y, z, w)
        
        self.tetaCam = yaw_z
        self.diferenca_angular.publish(self.tetaCam-self.tetaObj)
        

    def callback(self, posicao_relativa):
            x1 = posicao_relativa.point.x
            y1 =  posicao_relativa.point.y

            x2=0
            y2=-1

            if x1 > 0:
                teta = math.acos(x1*x2 + y1*y2 / (math.sqrt(x1**2 + y1**2) * math.sqrt( x2**2 + y2**2)))
            else:
                teta = -math.acos(x1*x2 + y1*y2 / (math.sqrt(x1**2 + y1**2) * math.sqrt( x2**2 + y2**2)))

            self.tetaObj = teta
    
    def euler_from_quaternion(self, x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        # https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
        return  yaw_z 
            

if __name__ == '__main__':
    rospy.init_node('mediar_orientacao', anonymous=True)
    l = Orientation()
    rospy.spin()