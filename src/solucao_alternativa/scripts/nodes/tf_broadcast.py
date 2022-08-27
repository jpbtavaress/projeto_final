#!/usr/bin/env python3

import rospy
import tf2_ros
import geometry_msgs.msg
import math

# class Policia_Ladrao:
    
    # def __init__(self):

    #     rospy.init_node('mediar_orientacao', anonymous=True)
    #     self.distancia = None
    #     rospy.Subscriber('sonar_data', PointStamped, self.callback)
    #     self.objetivo_x = rospy.Publisher('objetivo_X', Float64, queue_size=10)
    #     self.objetivo_y = rospy.Publisher('objetivo_Y', Float64, queue_size=10)
        
    # def callback(self, distancia):
    #     self.distancia = distancia
    #     self.follow_nemo(child, parent, )
    
def follow_nemo(child, parent, distancia_child_to_parent, tempo):
    br = tf2_ros.TransformBroadcaster() #instanciando para publicar (boradcast)
    t = geometry_msgs.msg.TransformStamped() #instanciando a mensgame que vai ser utilizada
    #prenchendo a mensagem
    t.header.stamp = rospy.Time.now() 
    t.header.frame_id = child
    t.child_frame_id = parent

    #instanciando as datas da msg
    t.transform.translation.x = distancia_child_to_parent * math.sin(tempo)
    t.transform.translation.y = distancia_child_to_parent * math.cos(tempo)
    t.transform.translation.z = 0.0
    t.transform.rotation.x = 0
    t.transform.rotation.y = 0
    t.transform.rotation.z = 0
    t.transform.rotation.w = 1

    br.sendTransform(t)
    rate.sleep()

if __name__ == '__main__':
    rospy.init_node('perseguicao', anonymous=True) #iniciar o nó
    rate = rospy.Rate(100) #definir a velocidade das publicações
    astro = rospy.get_param ("policia_ladrao") #acessar o documento yaml que contém os parâmetros
    while not rospy.is_shutdown():
        x = rospy.Time.now().to_sec() # pegar o tempo do ros
        follow_nemo(astro["child"], astro["parent"], astro["distancia_child_to_parent"], x*astro["velocidade"])