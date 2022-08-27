#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, Point #importando o tipo de mensagem que será utilizado


class Movimento:
    def __init__(self):
        rospy.init_node('move', anonymous=True) #inicializa o nó, tem que ter no programa
        rospy.Subscriber('objetivo_X', Point, self.callback)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10) #se inscreve em um tópico (o publisher publica em um tópico)
    
    def callback(self,msg):
        x_linear, y_linear, z_linear = msg.x, msg.y, msg.z  
        v = Twist()
        v.linear.x = x_linear #Declarando as variáveis de velocidade 
        v.linear.y = y_linear
        v.linear.z = z_linear
        v.angular.x = 0
        v.angular.y = 0
        v.angular.z = 0
        self.pub.publish(v)

if __name__ == '__main__':
    try:
        while not rospy.is_shutdown():
            t = Movimento()
            
    except rospy.ROSInterruptException:
        pass