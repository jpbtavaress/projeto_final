#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Float64
import math

class ModularVelocidade():
    def __init__(self):
        self.tempo = 0
        self.auxiliar()
        
    def auxiliar(self):
        while not rospy.is_shutdown():    
            rospy.init_node('mediar_orientacao', anonymous=True)
            rospy.Subscriber('sonar_data', PointStamped, self.callback)
            self.velocidade_x = rospy.Publisher('objetivo_X', Float64, queue_size=10)
            self.velocidade_y = rospy.Publisher('objetivo_Y', Float64, queue_size=10)
            
    def callback(self, posicao_relativa):
        tempo2 = rospy.Time.now() - self.tempo   
        self.tempo = rospy.Time.now()
        distancia_x = posicao_relativa.point.x
        distancia_y =  posicao_relativa.point.y
        distancia_z = posicao_relativa.point.z #vai ser sempre 0
        mover_lado = Float64()
        mover_frente = Float64()
        
        if distancia_x >= 2:
            mover_lado.data = distancia_x
            velocidade_x = distancia_x/tempo2

        elif  distancia_x <= -2:
            mover_lado.data = -(distancia_x)
            velocidade_x = distancia_x/tempo2
        
        elif (distancia_x >= -2) and (distancia_x <= 2):
            mover_lado.data = 0.0
            velocidade_x = distancia_x/tempo2

        if distancia_y >= 2:
            mover_frente.data = distancia_y
            velocidade_y = distancia_y/tempo2

        elif distancia_y <= -2:
            mover_frente.data = -(distancia_y)
            velocidade_y = distancia_y/tempo2
        else: 
            mover_frente.data = 0.0
            velocidade_y = distancia_y/tempo2
        
        self.velocidade_x.publish(velocidade_x)
        self.velocidade_y.publish(velocidade_y)


if __name__ == '__main__':
    l = ModularVelocidade()
        # rospy.spin()