#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist #importando o tipo de mensagem que será utilizado


class Movimento:
    def __init__(self):
        rospy.init_node('move', anonymous=True) #inicializa o nó, tem que ter no programa
        rospy.Subscriber('objetivo', Twist, self.callback)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10) #se inscreve em um tópico (o publisher publica em um tópico)
    
    def callback(self,msg):
        rate = rospy.Rate(100)
        
        x_linear, y_linear, z_linear, x_angular, y_angular, z_angular = msg.linear.x, msg.linear.y, msg.linear.z, msg.angular.x, msg.angular.y, msg.angular.z
  
        
        v = Twist()
        v.linear.x = x_linear #Declarando as variáveis de velocidade 
        v.linear.y = y_linear
        v.linear.z = z_linear
        v.angular.x = x_angular
        v.angular.y = y_angular
        v.angular.z = z_angular
        self.pub.publish(v)
        
        rospy.loginfo(v)
        rate.sleep()
        
    

if __name__ == '__main__':
    try:
    
        t = Movimento()
        rospy.spin()

            
    except rospy.ROSInterruptException:
        pass
