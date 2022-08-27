#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Float64
import math

class ModularVelocidade():
    def __init__(self):

        rospy.init_node('mediar_orientacao', anonymous=True)
        rospy.Subscriber('sonar_data', PointStamped, self.callback)
        self.objetivo_x = rospy.Publisher('objetivo_X', Float64, queue_size=10)
        self.objetivo_y = rospy.Publisher('objetivo_Y', Float64, queue_size=10)

    def callback(self, posicao_relativa):
        
        distancia_x = posicao_relativa.point.x
        distancia_y =  posicao_relativa.point.y
        distancia_z = posicao_relativa.point.z #vai ser sempre 0
        
        mover_lado = Float64()
        mover_frente = Float64()
        
        if distancia_x >= 2:
            mover_lado.data = distancia_x * distancia_x

        elif  distancia_x <= -2:
            mover_lado.data = -(distancia_x * distancia_x)
        
        elif (distancia_x >= -2) and (distancia_x <= 2):
            mover_lado.data = 0.0

        if distancia_y >= 2:
            mover_frente.data = distancia_y*distancia_y

        elif distancia_y <= -2:
            mover_frente.data = -(distancia_y*distancia_y)

        else: 
            mover_frente.data = 0.0
        
        self.objetivo_x.publish(mover_lado)
        self.objetivo_y.publish(mover_frente)
        rospy.loginfo("Frente")
        rospy.loginfo(mover_frente)
        rospy.loginfo(distancia_y)
        rospy.loginfo("Lado")
        rospy.loginfo(mover_lado)
        rospy.loginfo(distancia_x)


if __name__ == '__main__':
    while not rospy.is_shutdown():
        l = ModularVelocidade()
        # rospy.spin()