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
        rospy.Subscriber('sonar_data', PointStamped, self.callback) #pegando as posições relativas entre os dois caminhos
        rospy.Subscriber('odom', Odometry, self.callback2) #pegando as posições relativas dos carrinhos em relação ao mundo de forma vetorial
        self.diferenca_angular = rospy.Publisher('diferenca_angular', Float64, queue_size=10)
        
    def callback(self, posicao_relativa):
        x1 = posicao_relativa.point.x #instanciando a posição que o tópico "sonar_data" nos forneceu no 1° subscriber
        y1 =  posicao_relativa.point.y

        x2=0 #definindo um vetor unitário no eixo y que servirá de referência para o angulo entre os carrinhos
        y2=-1

        if x1 > 0: #descobrindo o angulo entre os dois vetores pelo produto interno.
            teta = math.acos(x1*x2 + y1*y2 / (math.sqrt(x1**2 + y1**2) * math.sqrt( x2**2 + y2**2)))
        else:
            teta = -math.acos(x1*x2 + y1*y2 / (math.sqrt(x1**2 + y1**2) * math.sqrt( x2**2 + y2**2)))

        self.tetaObj = teta #instanciando o angulo entre a normal(eixo de referência) e o vetor do nemo e marlin
        
    def euler_from_quaternion(self, x, y, z, w): #transformar o quartenium em um ângulo (euler)
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        # https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
        # Link da origem do código
        
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
        return  yaw_z  #só retornamos a rotação ao redor de z(em radianos), já que nosso carrinho não rotaciona nas demais direções
        
    def callback2(self, posicao_absoluta): #descobre o angulo da câmera do marlin em relação ao eixo y do mundo
        x = posicao_absoluta.pose.pose.orientation.x #instanciando as infos vindas do tópico odom
        y = posicao_absoluta.pose.pose.orientation.y
        z = posicao_absoluta.pose.pose.orientation.z
        w = posicao_absoluta.pose.pose.orientation.w
        yaw_z = self.euler_from_quaternion( x, y, z, w) #guarda o angulo de rotação da função em torno de Z
        
        self.tetaCam = yaw_z
        
        #Definimos então a diferença angular entre o ângulo entre os carrinhos e o eixo y e
        #o angulo da câmera e o eixo Y. Portanto o ângulo que devemos  girar o marlin para 
        #seguir a trajetória do nemo corretamente.
        self.diferenca_angular.publish(self.tetaCam-self.tetaObj) #publicando no tópico diferença angular
        
            

if __name__ == '__main__':
    rospy.init_node('mediar_orientacao', anonymous=True)
    l = Orientation()
    rospy.spin()