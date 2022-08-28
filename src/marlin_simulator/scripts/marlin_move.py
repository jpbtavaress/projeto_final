#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped, Twist
from math import sqrt
from std_msgs.msg import Float64


class Movement():
    def __init__(self):
        self.tempo = 0.0
        self.velocidade_angular = 0.0
        self.velocidade = 0.0

        rospy.Subscriber('diferenca_angular', Float64, self.girar)
        rospy.Subscriber('sonar_data', PointStamped, self.acelerar)
        
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10) 
            
    def girar(self, diferenca_angular):
        
        if not abs(diferenca_angular.data) < 0.1:
            self.velocidade_angular = 6.0
        # elif not abs(diferenca_angular.data) > 6  :
        #     self.velocidade_angular = -6.0
        else:
            self.velocidade_angular = 0.0

        mover = Twist()
        mover.linear.x = 0.0
        mover.linear.y = self.velocidade
        mover.linear.z = 0.0
        mover.angular.x = 0.0
        mover.angular.y = 0.0
        mover.angular.z = self.velocidade_angular
        rospy.loginfo(mover)
        rospy.loginfo(diferenca_angular.data)

        self.pub.publish(mover)
        

    def acelerar(self, posicao_relativa):
            
            intervalo = rospy.Time.now().to_sec() - self.tempo   
            self.tempo = rospy.Time.now().to_sec()

            distancia_x = posicao_relativa.point.x
            distancia_y =  posicao_relativa.point.y
            distancia_z = posicao_relativa.point.z 
            
            if distancia_x >= 2.5 or distancia_x <= -2.5:
                velocidade_x = -distancia_x/intervalo 
            else:
                velocidade_x = 0.0

            if distancia_y >= 2.5 or distancia_y <= -2.5:
                velocidade_y = -distancia_y/intervalo
            else: 
                velocidade_y = 0.0

             
            self.velocidade = sqrt(velocidade_x**2+velocidade_y**2) 

            


if __name__ == '__main__':
    rospy.init_node('mediar_velocidade', anonymous=True)
    l = Movement()
    rospy.spin()
    