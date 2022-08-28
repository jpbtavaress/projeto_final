#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped, Twist
from math import sqrt
from std_msgs.msg import Float64


class Movement():
    def __init__(self):
        self.tempo = 0.0
        self.velocidade_angular = 0.0
        self.velocidade = 0.0 #vai ser atualizada sempre que a função acelerar rodar,
                              #ou seja, a cada vez que o sonar_data publica alguma coisa
        rospy.Subscriber('diferenca_angular', Float64, self.girar) #pegou o ângulo do tópico em que publicamos a diferença angular
        rospy.Subscriber('sonar_data', PointStamped, self.acelerar)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10) 

    def girar(self, diferenca_angular): 
        # "diferenca_angular" vem em formato de radiano (angulo em graus × π/180)
        #6 rad = 343°
        #3 rad = 171.8° ...
        
        if  abs(diferenca_angular.data) < 6 and abs(diferenca_angular.data) >= 3.0 or diferenca_angular.data < 0:
            self.velocidade_angular = 6.0
        elif (abs(diferenca_angular.data) < 3 and abs(diferenca_angular.data) >  0.1):
            self.velocidade_angular = -6.0
        else:
            self.velocidade_angular = 0.0

        mover = Twist()
        mover.linear.x = 0.0
        mover.linear.y = self.velocidade #instanciamos aqui a velocidade calculada na função "acelerar".
        #A razão de publicarmos a velocidade junto com o tópico "velocidade angular", que utiliza o
        #rate do tópico "odom" foi para não termos um atraso do carrinho em razão do rate lento
        #do "sonar_data". Dessa forma, toda hora que o carrinho recebe uma informação de mudar sua 
        #velocidade angular, publicamos novamente sua velocidade_linear (ainda que desatualizada, em razão
        # do delay da função acelerar) para que ele não fique parado e depois aumente muito sua 
        # velocidade ou parar de repente em virtude de uma desaleração do nemo.
        mover.linear.z = 0.0
        mover.angular.x = 0.0
        mover.angular.y = 0.0
        mover.angular.z = self.velocidade_angular
        # Definimos a velocidade linear nos eixos x e z como zero para que o carrinho só ande paralelo a direção da roda do carrinho
        #Defimos a velocidade angular nos eixos x e y como zero para que o carrinho muda sua direção pelo eixo z somente. (carrinho esta apoiado no chão, não faria sentido girar em torno do mesmo)
        rospy.loginfo(mover)
        rospy.loginfo(diferenca_angular.data)

        self.pub.publish(mover)
        

    def acelerar(self, posicao_relativa): #utilizamos as informações do sonar_data para calcularmos a velocidade.
        
        intervalo = rospy.Time.now().to_sec() - self.tempo 
        self.tempo = rospy.Time.now().to_sec()
        #Através desse trecho a cima, definimos o deltaT que o nemo se move em relação ao marlin
        

        distancia_x = posicao_relativa.point.x
        distancia_y =  posicao_relativa.point.y
        distancia_z = posicao_relativa.point.z 
        #Dessa forma, dividino a distância entre os dois carrinhos pelo temo intervalo de tempo
        #em que esse distanciamento ocorreu, definindo então a velocidade que o marlin deverá ter
        #para seguir a trajetória do nemo de forma eficaz.
        
        if distancia_x >= 2.5 or distancia_x <= -2.5:
            velocidade_x = -distancia_x/intervalo 
        else:
            velocidade_x = 0.0

        if distancia_y >= 2.5 or distancia_y <= -2.5:
            velocidade_y = -distancia_y/intervalo
        else: 
            velocidade_y = 0.0

            
        self.velocidade = sqrt(velocidade_x**2+velocidade_y**2) 
        # Como o carrinho so se move na direção y, paralela a orientação de suas rodas, calculamos 
        # o módulo  das velocidades em cada eixo e publicamos como uma única velocidade.

            


if __name__ == '__main__':
    rospy.init_node('mediar_velocidade', anonymous=True)
    l = Movement()
    rospy.spin()
    