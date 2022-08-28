#!/usr/bin/env python3
# teste =  [
#      {"child": "marlin",
#      "distancia_child_to_parent": 1,
#       "parent": "nemo",
#       "velocidade": 1}
# ]

# print(teste[0]["child"])
import rospy
rospy.init_node("teste", anonymous=True)
print(type(rospy.Time.now().to_sec()))