#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped, Point


class ModularVelocidade():
    def __init__(self):
        self.tempo = 0
        self.auxiliar()
        
    def auxiliar(self):
        while not rospy.is_shutdown():    
            rospy.init_node('mediar_orientacao', anonymous=True)
            rospy.Subscriber('sonar_data', PointStamped, self.callback)
            self.velocidade = rospy.Publisher('objetivo', Point, queue_size=10)
            
            
    def callback(self, posicao_relativa):
        tempo2 = rospy.Time.now() - self.tempo   
        self.tempo = rospy.Time.now()
        distancia_x = posicao_relativa.point.x
        distancia_y =  posicao_relativa.point.y
        distancia_z = posicao_relativa.point.z #vai ser sempre 0
        mover = Point()

        
        if distancia_x >= 2:
            velocidade_x = distancia_x/tempo2

        elif  distancia_x <= -2:
            velocidade_x = -distancia_x/tempo2
        
        elif (distancia_x >= -2) and (distancia_x <= 2):
            velocidade_x = 0.0

        if distancia_y >= 2:
            velocidade_y = distancia_y/tempo2

        elif distancia_y <= -2:
            velocidade_y = -distancia_y/tempo2
        else: 
            velocidade_y = 0.0
        
        mover.x = velocidade_x
        mover.y = velocidade_y
        mover.z = 0.0
        self.velocidade.publish(mover)


if __name__ == '__main__':
    l = ModularVelocidade()
        # rospy.spin()