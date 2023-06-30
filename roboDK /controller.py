from robodk.robolink import *
from time import sleep

RDK = Robolink()
conveyer = RDK.Item("Conveyer")
Target_1 = RDK.Item("Target 1")
Target_2 = RDK.Item("Target 2")

gantry = RDK.Item("Gantry")
Target_3 = RDK.Item("zero")
Target_4 = RDK.Item("one")
Target_5 = RDK.Item("two")
Target_6 = RDK.Item("three")
gantry.MoveJ(Target_3)
sleep(2)
gantry.MoveJ(Target_4)
sleep(2)
gantry.MoveJ(Target_3)
sleep(2)
gantry.MoveJ(Target_5)
sleep(2)
gantry.MoveJ(Target_6)
sleep(2)
gantry.MoveJ(Target_5)
sleep(2)
gantry.MoveJ(Target_3)
sleep(2)
conveyer.MoveJ(Target_1)
sleep(2)
conveyer.MoveJ(Target_2)
sleep(2)
conveyer.MoveJ(Target_1)

g
