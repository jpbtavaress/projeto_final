#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist #importando o tipo de mensagem que será utilizado
import random

class Movimento:
    def __init__(self):
        rospy.init_node('move', anonymous=True) #inicializa o nó, tem que ter no programa
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10) #se inscreve em um tópico (o publisher publica em um tópico)
        self.list = list(range(10))

    def cmd_vel(self):
        rate = rospy.Rate(5)
        while not rospy.is_shutdown():
            v = Twist()
            v.linear.x = random.choice(self.list) #Declarando as variáveis de velocidade 
            v.linear.y = random.choice(self.list)
            v.linear.z = 0
            v.angular.x = random.choice(self.list)
            v.angular.y = random.choice(self.list)
            v.angular.z = 0
            self.pub.publish(v)
            rate.sleep() #respeitar o rate definido anteriormente

if __name__ == '__main__':
    try:
        t = Movimento()
        t.cmd_vel()
    except rospy.ROSInterruptException:
        pass