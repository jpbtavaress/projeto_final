#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped, Point


class ModularVelocidade():
    def __init__(self):
        self.tempo = 0.0
        rospy.init_node('mediar_orientacao', anonymous=True)
        rospy.Subscriber('sonar_data', PointStamped, self.callback)
        self.velocidade = rospy.Publisher('objetivo', Point, queue_size=10)
            
            
    def callback(self, posicao_relativa):
            rate = rospy.Rate(100)
            tempo2 = rospy.Time.now().to_sec() - self.tempo   
            self.tempo = rospy.Time.now().to_sec()
            distancia_x = posicao_relativa.point.x
            distancia_y =  posicao_relativa.point.y
            distancia_z = posicao_relativa.point.z #vai ser sempre 0
            
            mover = Point()
            
            if distancia_x >= 1.5 or distancia_x <= -1.5:
                velocidade_x = -distancia_x/tempo2
            else:
                velocidade_x = 0.0

            if distancia_y >= 1.5 or distancia_y <= -1.5:
                velocidade_y = -distancia_y/tempo2
            else: 
                velocidade_y = 0.0
            
            mover.x = velocidade_x
            mover.y = velocidade_y
            mover.z = 0.0
            print(mover)
            
            self.velocidade.publish(mover)
            rate.sleep()


if __name__ == '__main__':
    
    l = ModularVelocidade()
    rospy.spin()