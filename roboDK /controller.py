from robodk.robolink import *
from time import sleep
import logging

logging.basicConfig(filename='simulation.log',filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)


RDK = Robolink()
conveyer = RDK.Item("Conveyer")
Target_1 = RDK.Item("zero_pos")
Target_2 = RDK.Item("extreme")
inventory = RDK.Item('inventory')
print(inventory.Joints())

p1 = RDK.Item('pos1')
p2 = RDK.Item('pos2')
p3 = RDK.Item('pos3')
p4 = RDK.Item('pos4')
p5 = RDK.Item('pos5')
p6 = RDK.Item('pos6')
p7 = RDK.Item('pos7')
p8 = RDK.Item('pos8')
p9 = RDK.Item('pos9')
inventory_targets = [p5,p6]

gantry = RDK.Item("Gantry")
Target_3 = RDK.Item("zero")
Target_4 = RDK.Item("one")
Target_5 = RDK.Item("two")
Target_6 = RDK.Item("three")
Target_7 = RDK.Item("mean_l")
Target_8 = RDK.Item('extreme_l')
Target_9 = RDK.Item('mean_u')
Target_10 = RDK.Item('extreme_u')

def up():
    gantry.MoveJ(Target_4)
    sleep(2)

def down():
    gantry.MoveJ(Target_3)
    sleep(2)

def pick_upper():
    gantry.MoveJ(Target_3)
    sleep(2)
    gantry.MoveJ(Target_9)
    sleep(2)
    gantry.MoveJ(Target_10)
    sleep(2)
    gantry.MoveJ(Target_9)
    sleep(2)
    gantry.MoveJ(Target_3)
    sleep(2)

def pick_lower():
    gantry.MoveJ(Target_3)
    sleep(2)
    gantry.MoveJ(Target_7)
    sleep(2)
    gantry.MoveJ(Target_8)
    sleep(2)
    gantry.MoveJ(Target_7)
    sleep(2)
    gantry.MoveJ(Target_3)
    sleep(2)
def shift_inventory():
    inventory.MoveJ(p1)
    for i in inventory_targets:
        inventory.MoveJ(i)
        logging.info(inventory.Joints())
        print("Current Inventory Joint Pose : ",inventory.Joints())
        # sleep(1)
        pick_lower()
        # sleep(1)
        # pick_upper()


while(1):
    gantry.setSpeedJoints(10)
    inventory.setSpeedJoints(10)
    shift_inventory()




