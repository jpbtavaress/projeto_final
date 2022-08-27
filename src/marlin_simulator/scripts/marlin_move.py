#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist #importando o tipo de mensagem que será utilizado
from std_msgs.msg import Float64
import random

class Movimento:
    def __init__(self):
        rospy.init_node('move', anonymous=True) #inicializa o nó, tem que ter no programa
        rospy.Subscriber('objetivo_X', Float64, self.callback1)
        rospy.Subscriber('objetivo_Y', Float64, self.callback2)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10) #se inscreve em um tópico (o publisher publica em um tópico)
    
    def callback1(self,msg):
        distancia_x = msg.data
        velocidade = Twist()
        velocidade_x = 
        self.cmd_vel()

    def callback2(self, velocidade):
        self.v.linear.y = velocidade.data
        self.cmd_vel()

    def cmd_vel(self):
        rate = rospy.Rate(5)
        
        self.v.linear.z = 0.0
        self.v.angular.x = 0.0
        self.v.angular.y = 0.0
        self.v.angular.z = 0.0
        self.pub.publish(self.v)
        rate.sleep() #respeitar o rate definido anteriormente

if __name__ == '__main__':
    try:
        while not rospy.is_shutdown():
            t = Movimento()
            
    except rospy.ROSInterruptException:
        pass